"""
视频解析服务
封装对现有 DouyinAPI 的调用，提供视频信息获取和格式化功能
"""
import os
import re
import httpx
from typing import Optional, Tuple
from loguru import logger

# 导入现有模块 (不修改原有代码)
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dy_apis.douyin_api import DouyinAPI
from builder.auth import DouyinAuth
from api.schemas.video import (
    VideoInfo, VideoQuality, AuthorInfo, Statistics, VideoParseResponse
)
from api.config import REQUEST_TIMEOUT


def _get_auth() -> DouyinAuth:
    """
    获取认证对象
    从环境变量或 .env 文件读取 Cookie
    """
    from dotenv import load_dotenv
    load_dotenv()

    cookie_str = os.getenv("COOKIE", "")
    if not cookie_str:
        raise ValueError("未配置 Cookie，请在 .env 文件中设置 COOKIE 环境变量")

    auth = DouyinAuth()
    auth.perepare_auth(cookie_str)
    return auth


def _format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小为可读字符串
    """
    if size_bytes <= 0:
        return "未知"

    units = ["B", "KB", "MB", "GB"]
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.1f} {units[unit_index]}"


async def _get_file_size(url: str) -> int:
    """
    通过 HEAD 请求获取视频文件大小
    """
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, verify=False) as client:
            # 设置必要的请求头
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.douyin.com/"
            }
            response = await client.head(url, headers=headers, follow_redirects=True)
            content_length = response.headers.get("content-length", "0")
            return int(content_length)
    except Exception as e:
        logger.warning(f"获取文件大小失败: {e}")
        return 0


def _extract_video_id(url: str) -> str:
    """
    从 URL 中提取视频 ID
    """
    if 'video' in url:
        return url.split("/")[-1].split("?")[0]
    else:
        match = re.findall(r'modal_id=(\d+)', url)
        if match:
            return match[0]
    return ""


def _get_quality_label(width: int, height: int) -> str:
    """
    根据分辨率生成清晰度标签
    """
    max_dim = max(width, height)
    if max_dim >= 1080:
        return "1080p"
    elif max_dim >= 720:
        return "720p"
    elif max_dim >= 540:
        return "540p"
    elif max_dim >= 480:
        return "480p"
    elif max_dim >= 360:
        return "360p"
    else:
        return f"{max_dim}p"


async def parse_video(url: str) -> VideoParseResponse:
    """
    解析抖音视频链接，获取视频信息和多清晰度下载地址

    :param url: 抖音视频链接
    :return: VideoParseResponse
    """
    try:
        # 获取认证
        auth = _get_auth()

        # 调用现有 API 获取视频信息
        result = DouyinAPI.get_work_info(auth, url)

        if not result or "aweme_detail" not in result:
            return VideoParseResponse(
                success=False,
                message="无法获取视频信息，请检查链接是否正确"
            )

        aweme = result["aweme_detail"]

        # 提取作者信息
        author_data = aweme.get("author", {})
        author = AuthorInfo(
            nickname=author_data.get("nickname", ""),
            avatar=author_data.get("avatar_thumb", {}).get("url_list", [""])[0],
            sec_uid=author_data.get("sec_uid", "")
        )

        # 提取统计数据
        stats_data = aweme.get("statistics", {})
        statistics = Statistics(
            digg_count=stats_data.get("digg_count", 0),
            comment_count=stats_data.get("comment_count", 0),
            share_count=stats_data.get("share_count", 0),
            collect_count=stats_data.get("collect_count", 0)
        )

        # 提取视频信息
        video_data = aweme.get("video", {})

        # 提取多清晰度视频地址
        video_urls = []
        bit_rate_list = video_data.get("bit_rate", [])

        # 用于去重
        seen_qualities = set()

        for bit_rate in bit_rate_list:
            play_addr = bit_rate.get("play_addr", {})
            url_list = play_addr.get("url_list", [])

            if not url_list:
                continue

            # 获取视频 URL (优先使用第一个)
            video_url = url_list[0]

            # 获取分辨率
            width = play_addr.get("width", 0) or bit_rate.get("width", 0)
            height = play_addr.get("height", 0) or bit_rate.get("height", 0)

            # 生成清晰度标签
            quality_label = _get_quality_label(width, height)
            gear_name = bit_rate.get("gear_name", "")

            # 去重
            quality_key = f"{quality_label}_{gear_name}"
            if quality_key in seen_qualities:
                continue
            seen_qualities.add(quality_key)

            # 获取文件大小
            file_size = await _get_file_size(video_url)

            video_urls.append(VideoQuality(
                quality=quality_label,
                gear_name=gear_name,
                width=width,
                height=height,
                file_size=file_size,
                file_size_str=_format_file_size(file_size),
                url=video_url
            ))

        # 如果没有从 bit_rate 获取到，尝试从 play_addr 获取
        if not video_urls:
            play_addr = video_data.get("play_addr", {})
            url_list = play_addr.get("url_list", [])
            if url_list:
                video_url = url_list[0]
                width = play_addr.get("width", 0)
                height = play_addr.get("height", 0)
                file_size = await _get_file_size(video_url)

                video_urls.append(VideoQuality(
                    quality=_get_quality_label(width, height),
                    gear_name="default",
                    width=width,
                    height=height,
                    file_size=file_size,
                    file_size_str=_format_file_size(file_size),
                    url=video_url
                ))

        # 按清晰度排序 (高清在前)
        video_urls.sort(key=lambda x: x.height, reverse=True)

        # 构建视频信息
        video_info = VideoInfo(
            video_id=aweme.get("aweme_id", _extract_video_id(url)),
            title=aweme.get("desc", ""),
            desc=aweme.get("desc", ""),
            author=author,
            statistics=statistics,
            cover=video_data.get("cover", {}).get("url_list", [""])[0],
            duration=video_data.get("duration", 0),
            create_time=aweme.get("create_time", 0),
            video_urls=video_urls
        )

        return VideoParseResponse(
            success=True,
            message="解析成功",
            data=video_info
        )

    except ValueError as e:
        return VideoParseResponse(
            success=False,
            message=str(e)
        )
    except Exception as e:
        logger.error(f"视频解析失败: {e}")
        return VideoParseResponse(
            success=False,
            message=f"解析失败: {str(e)}"
        )


async def proxy_video_stream(url: str):
    """
    代理视频流，用于绕过防盗链

    :param url: 原始视频 URL
    :return: 异步生成器，产出视频数据块
    """
    from api.config import VIDEO_PROXY_CHUNK_SIZE

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.douyin.com/"
    }

    async with httpx.AsyncClient(timeout=None, verify=False) as client:
        async with client.stream("GET", url, headers=headers, follow_redirects=True) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes(chunk_size=VIDEO_PROXY_CHUNK_SIZE):
                yield chunk
