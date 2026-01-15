"""
用户相关路由
"""
from fastapi import APIRouter, Query
from loguru import logger

from api.schemas.user import (
    UserInfoResponse, UserWorksResponse, UserAllWorksResponse
)
from api.services.user_service import (
    get_user_info, get_user_works, get_user_all_works
)

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get(
    "/info",
    response_model=UserInfoResponse,
    summary="获取用户信息",
    responses={
        200: {"description": "获取成功", "model": UserInfoResponse}
    }
)
async def api_get_user_info(
    url: str = Query(..., description="用户主页链接")
):
    """
    获取抖音用户信息

    - **url**: 用户主页链接 (如 https://www.douyin.com/user/xxx)

    返回用户的基本信息、粉丝数、关注数、作品数等
    """
    if not url:
        return UserInfoResponse(success=False, message="请提供用户主页链接")

    if "douyin.com" not in url:
        return UserInfoResponse(success=False, message="请提供有效的抖音用户主页链接")

    return get_user_info(url)


@router.get(
    "/works",
    response_model=UserWorksResponse,
    summary="获取用户作品列表",
    responses={
        200: {"description": "获取成功", "model": UserWorksResponse}
    }
)
async def api_get_user_works(
    url: str = Query(..., description="用户主页链接"),
    max_cursor: str = Query(default="0", description="分页游标")
):
    """
    获取抖音用户作品列表（分页）

    - **url**: 用户主页链接
    - **max_cursor**: 分页游标，首次请求传 "0"，后续请求传返回的 max_cursor

    返回作品列表及分页信息
    """
    if not url:
        return UserWorksResponse(success=False, message="请提供用户主页链接")

    if "douyin.com" not in url:
        return UserWorksResponse(success=False, message="请提供有效的抖音用户主页链接")

    return get_user_works(url, max_cursor)


@router.get(
    "/works/all",
    response_model=UserAllWorksResponse,
    summary="获取用户全部作品",
    responses={
        200: {"description": "获取成功", "model": UserAllWorksResponse}
    }
)
async def api_get_user_all_works(
    url: str = Query(..., description="用户主页链接")
):
    """
    获取抖音用户全部作品

    - **url**: 用户主页链接

    ⚠️ 注意：此接口会获取用户的全部作品，作品数量较多时可能耗时较长

    返回用户的全部作品列表
    """
    if not url:
        return UserAllWorksResponse(success=False, message="请提供用户主页链接")

    if "douyin.com" not in url:
        return UserAllWorksResponse(success=False, message="请提供有效的抖音用户主页链接")

    return get_user_all_works(url)
