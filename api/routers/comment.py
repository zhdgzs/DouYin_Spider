"""
评论相关路由
"""
from fastapi import APIRouter, Query
from loguru import logger

from api.schemas.comment import (
    CommentListResponse, CommentRepliesResponse, AllCommentsResponse
)
from api.services.comment_service import (
    get_comment_list, get_comment_replies, get_all_comments
)

router = APIRouter(prefix="/api/comment", tags=["comment"])


@router.get(
    "/list",
    response_model=CommentListResponse,
    summary="获取一级评论",
    responses={
        200: {"description": "获取成功", "model": CommentListResponse}
    }
)
async def api_get_comment_list(
    url: str = Query(..., description="作品链接"),
    cursor: str = Query(default="0", description="分页游标")
):
    """
    获取作品的一级评论列表

    - **url**: 作品链接 (如 https://www.douyin.com/video/xxx)
    - **cursor**: 分页游标，首次请求传 "0"

    返回一级评论列表及分页信息
    """
    if not url:
        return CommentListResponse(success=False, message="请提供作品链接")

    if "douyin.com" not in url:
        return CommentListResponse(success=False, message="请提供有效的抖音作品链接")

    return get_comment_list(url, cursor)


@router.get(
    "/replies",
    response_model=CommentRepliesResponse,
    summary="获取二级评论",
    responses={
        200: {"description": "获取成功", "model": CommentRepliesResponse}
    }
)
async def api_get_comment_replies(
    aweme_id: str = Query(..., description="作品ID"),
    comment_id: str = Query(..., description="一级评论ID"),
    cursor: str = Query(default="0", description="分页游标"),
    count: str = Query(default="20", description="每页数量")
):
    """
    获取一级评论的回复列表（二级评论）

    - **aweme_id**: 作品ID
    - **comment_id**: 一级评论ID
    - **cursor**: 分页游标
    - **count**: 每页数量

    返回二级评论列表及分页信息
    """
    if not aweme_id:
        return CommentRepliesResponse(success=False, message="请提供作品ID")

    if not comment_id:
        return CommentRepliesResponse(success=False, message="请提供评论ID")

    return get_comment_replies(aweme_id, comment_id, cursor, count)


@router.get(
    "/all",
    response_model=AllCommentsResponse,
    summary="获取全部评论",
    responses={
        200: {"description": "获取成功", "model": AllCommentsResponse}
    }
)
async def api_get_all_comments(
    url: str = Query(..., description="作品链接")
):
    """
    获取作品的全部评论（包含回复）

    - **url**: 作品链接

    ⚠️ 注意：此接口会获取全部评论及其回复，评论数量较多时可能耗时较长

    返回全部评论列表（包含二级回复）
    """
    if not url:
        return AllCommentsResponse(success=False, message="请提供作品链接")

    if "douyin.com" not in url:
        return AllCommentsResponse(success=False, message="请提供有效的抖音作品链接")

    return get_all_comments(url)
