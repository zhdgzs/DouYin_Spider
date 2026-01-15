"""
关系相关路由
"""
from fastapi import APIRouter, Query
from loguru import logger

from api.schemas.relation import (
    FollowerListResponse, FollowingListResponse, NoticeListResponse
)
from api.services.relation_service import (
    get_follower_list, get_following_list, get_notice_list
)

router = APIRouter(prefix="/api/relation", tags=["relation"])


@router.get(
    "/followers",
    response_model=FollowerListResponse,
    summary="获取粉丝列表",
    responses={
        200: {"description": "获取成功", "model": FollowerListResponse}
    }
)
async def api_get_follower_list(
    user_id: str = Query(..., description="用户ID"),
    sec_uid: str = Query(..., description="用户安全ID"),
    max_time: str = Query(default="0", description="分页时间戳"),
    count: str = Query(default="20", description="每页数量")
):
    """
    获取用户的粉丝列表

    - **user_id**: 用户ID（可从用户信息接口获取）
    - **sec_uid**: 用户安全ID（可从用户信息接口获取）
    - **max_time**: 分页时间戳，首次请求传 "0"
    - **count**: 每页数量

    返回粉丝列表及分页信息
    """
    if not user_id:
        return FollowerListResponse(success=False, message="请提供用户ID")

    if not sec_uid:
        return FollowerListResponse(success=False, message="请提供用户安全ID")

    return get_follower_list(user_id, sec_uid, max_time, count)


@router.get(
    "/following",
    response_model=FollowingListResponse,
    summary="获取关注列表",
    responses={
        200: {"description": "获取成功", "model": FollowingListResponse}
    }
)
async def api_get_following_list(
    user_id: str = Query(..., description="用户ID"),
    sec_uid: str = Query(..., description="用户安全ID"),
    max_time: str = Query(default="0", description="分页时间戳"),
    count: str = Query(default="20", description="每页数量")
):
    """
    获取用户的关注列表

    - **user_id**: 用户ID
    - **sec_uid**: 用户安全ID
    - **max_time**: 分页时间戳，首次请求传 "0"
    - **count**: 每页数量

    返回关注列表及分页信息
    """
    if not user_id:
        return FollowingListResponse(success=False, message="请提供用户ID")

    if not sec_uid:
        return FollowingListResponse(success=False, message="请提供用户安全ID")

    return get_following_list(user_id, sec_uid, max_time, count)


@router.get(
    "/notices",
    response_model=NoticeListResponse,
    summary="获取通知列表",
    responses={
        200: {"description": "获取成功", "model": NoticeListResponse}
    }
)
async def api_get_notice_list(
    max_time: str = Query(default="0", description="分页时间戳"),
    count: str = Query(default="20", description="每页数量"),
    notice_group: str = Query(default="700", description="消息类型: 700全部 401粉丝 601@我的 2评论 3点赞 520弹幕")
):
    """
    获取当前用户的通知列表

    - **max_time**: 分页时间戳，首次请求传 "0"
    - **count**: 每页数量
    - **notice_group**: 消息类型筛选

    返回通知列表及分页信息
    """
    return get_notice_list(max_time, count, notice_group)
