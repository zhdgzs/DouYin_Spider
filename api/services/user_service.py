"""
用户服务层
封装对 DouyinAPI 用户相关方法的调用
"""
import os
import sys
from typing import Optional
from loguru import logger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dy_apis.douyin_api import DouyinAPI
from builder.auth import DouyinAuth
from api.schemas.user import (
    UserInfo, UserInfoResponse, WorkItem, UserWorksResponse, UserAllWorksResponse
)


def _get_auth() -> DouyinAuth:
    """获取认证对象"""
    from dotenv import load_dotenv
    load_dotenv()

    cookie_str = os.getenv("COOKIE", "")
    if not cookie_str:
        raise ValueError("未配置 Cookie，请在 .env 文件中设置 COOKIE 环境变量")

    auth = DouyinAuth()
    auth.perepare_auth(cookie_str)
    return auth


def _extract_user_info(data: dict) -> UserInfo:
    """从 API 响应中提取用户信息"""
    user = data.get("user", {})

    # 提取头像
    avatar = ""
    avatar_larger = ""
    avatar_thumb = user.get("avatar_thumb", )
    avatar_larger_data = user.get("avatar_larger", {})
    if avatar_thumb and "url_list" in avatar_thumb:
        avatar = avatar_thumb["url_list"][0] if avatar_thumb["url_list"] else ""
    if avatar_larger_data and "url_list" in avatar_larger_data:
        avatar_larger = avatar_larger_data["url_list"][0] if avatar_larger_data["url_list"] else ""

    return UserInfo(
        uid=user.get("uid", ""),
        sec_uid=user.get("sec_uid", ""),
        nickname=user.get("nickname", ""),
        signature=user.get("signature", ""),
        avatar=avatar,
        avatar_larger=avatar_larger,
        follower_count=user.get("follower_count", 0),
        following_count=user.get("following_count", 0),
        total_favorited=user.get("total_favorited", 0),
        aweme_count=user.get("aweme_count", 0),
        favoriting_count=user.get("favoriting_count", 0),
        unique_id=user.get("unique_id", ""),
        short_id=user.get("short_id", ""),
        is_verified=user.get("custom_verify", "") != "",
        verification_type=user.get("verification_type", 0),
        custom_verify=user.get("custom_verify", ""),
        enterprise_verify_reason=user.get("enterprise_verify_reason", ""),
        ip_location=user.get("ip_location", "")
    )


def _extract_work_item(aweme: dict) -> WorkItem:
    """从作品数据中提取作品项"""
    # 提取封面
    cover = ""
    video_data = aweme.get("video", {})
    cover_data = video_data.get("cover", {})
    if cover_data and "url_list" in cover_data:
        cover = cover_data["url_list"][0] if cover_data["url_list"] else ""

    # 提取统计数据
    stats = aweme.get("statistics", {})

    return WorkItem(
        aweme_id=aweme.get("aweme_id", ""),
        desc=aweme.get("desc", ""),
        create_time=aweme.get("create_time", 0),
        cover=cover,
        duration=video_data.get("duration", 0),
        digg_count=stats.get("digg_count", 0),
        comment_count=stats.get("comment_count", 0),
        share_count=stats.get("share_count", 0),
        collect_count=stats.get("collect_count", 0),
        play_count=stats.get("play_count", 0)
    )


def get_user_info(url: str) -> UserInfoResponse:
    """
    获取用户信息

    :param url: 用户主页链接
    :return: UserInfoResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_user_info(auth, url)

        if not result or "user" not in result:
            return UserInfoResponse(
                success=False,
                message="无法获取用户信息，请检查链接是否正确"
            )

        user_info = _extract_user_info(result)

        return UserInfoResponse(
            success=True,
            message="获取成功",
            data=user_info
        )
    except ValueError as e:
        return UserInfoResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return UserInfoResponse(success=False, message=f"获取失败: {str(e)}")


def get_user_works(url: str, max_cursor: str = "0") -> UserWorksResponse:
    """
    获取用户作品列表（分页）

    :param url: 用户主页链接
    :param max_cursor: 分页游标
    :return: UserWorksResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_user_work_info(auth, url, max_cursor)

        if not result:
            return UserWorksResponse(
                success=False,
                message="无法获取作品列表"
            )

        aweme_list = result.get("aweme_list", [])
        works = [_extract_work_item(aweme) for aweme in aweme_list]

        return UserWorksResponse(
            success=True,
            message="获取成功",
            data=works,
            max_cursor=str(result.get("max_cursor", "0")),
            has_more=result.get("has_more", 0) == 1
        )
    except ValueError as e:
        return UserWorksResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取用户作品列表失败: {e}")
        return UserWorksResponse(success=False, message=f"获取失败: {str(e)}")


def get_user_all_works(url: str) -> UserAllWorksResponse:
    """
    获取用户全部作品

    :param url: 用户主页链接
    :return: UserAllWorksResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_user_all_work_info(auth, url)

        if not result:
            return UserAllWorksResponse(
                success=True,
                message="该用户暂无作品",
                data=[],
                total=0
            )

        works = [_extract_work_item(aweme) for aweme in result]

        return UserAllWorksResponse(
            success=True,
            message="获取成功",
            data=works,
            total=len(works)
        )
    except ValueError as e:
        return UserAllWorksResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取用户全部作品失败: {e}")
        return UserAllWorksResponse(success=False, message=f"获取失败: {str(e)}")
