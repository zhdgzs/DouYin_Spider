"""
视频相关路由
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from loguru import logger

from api.schemas.video import (
    VideoParseRequest, VideoParseResponse, HealthResponse, ErrorResponse
)
from api.services.video_service import parse_video, proxy_video_stream
from api.config import API_VERSION

router = APIRouter(prefix="/api", tags=["video"])


@router.get("/health", response_model=HealthResponse, summary="健康检查")
async def health_check():
    """
    健康检查接口，用于监控服务状态
    """
    return HealthResponse(status="ok", version=API_VERSION)


@router.post(
    "/video/parse",
    response_model=VideoParseResponse,
    summary="解析视频链接",
    responses={
        200: {"description": "解析成功", "model": VideoParseResponse},
        400: {"description": "请求参数错误", "model": ErrorResponse},
        500: {"description": "服务器内部错误", "model": ErrorResponse}
    }
)
async def parse_video_url(request: VideoParseRequest):
    """
    解析抖音视频链接，获取视频信息和多清晰度下载地址

    - **url**: 抖音视频链接 (支持多种格式)

    返回视频的基本信息、作者信息、统计数据以及多个清晰度的下载地址（含文件大小）
    """
    if not request.url:
        return VideoParseResponse(success=False, message="请提供视频链接")

    # 简单验证 URL 格式
    if "douyin.com" not in request.url and "iesdouyin.com" not in request.url:
        return VideoParseResponse(success=False, message="请提供有效的抖音视频链接")

    result = await parse_video(request.url)
    return result


@router.get(
    "/video/proxy",
    summary="视频代理",
    responses={
        200: {"description": "视频流"},
        400: {"description": "请求参数错误"},
        500: {"description": "代理失败"}
    }
)
async def proxy_video(url: str = Query(..., description="原始视频URL")):
    """
    视频代理接口，用于绕过防盗链限制进行视频预览

    - **url**: 原始视频 URL

    返回视频流，可直接用于 HTML5 video 标签播放
    """
    if not url:
        raise HTTPException(status_code=400, detail="请提供视频URL")

    try:
        return StreamingResponse(
            proxy_video_stream(url),
            media_type="video/mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Cache-Control": "no-cache"
            }
        )
    except Exception as e:
        logger.error(f"视频代理失败: {e}")
        raise HTTPException(status_code=500, detail=f"视频代理失败: {str(e)}")
