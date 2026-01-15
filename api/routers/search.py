"""
搜索相关路由
"""
from fastapi import APIRouter, Query
from loguru import logger

from api.schemas.search import (
    SearchWorksResponse, SearchUsersResponse, SearchLivesResponse
)
from api.services.search_service import (
    search_works, search_users, search_lives
)

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get(
    "/works",
    response_model=SearchWorksResponse,
    summary="搜索作品",
    responses={
        200: {"description": "搜索成功", "model": SearchWorksResponse}
    }
)
async def api_search_works(
    keyword: str = Query(..., description="搜索关键词"),
    offset: str = Query(default="0", description="分页偏移量"),
    sort_type: str = Query(default="0", description="排序方式: 0综合 1最多点赞 2最新发布"),
    publish_time: str = Query(default="0", description="发布时间: 0不限 1一天内 7一周内 180半年内"),
    filter_duration: str = Query(default="", description="视频时长: 空不限 0-1一分钟内 1-5一到五分钟 5-10000五分钟以上"),
    content_type: str = Query(default="", description="内容形式: 空不限 1视频 2图文")
):
    """
    搜索抖音作品

    - **keyword**: 搜索关键词
    - **offset**: 分页偏移量，首次请求传 "0"
    - **sort_type**: 排序方式
    - **publish_time**: 发布时间筛选
    - **filter_duration**: 视频时长筛选
    - **content_type**: 内容形式筛选

    返回作品搜索结果列表
    """
    if not keyword:
        return SearchWorksResponse(success=False, message="请提供搜索关键词")

    return search_works(
        keyword, offset, sort_type, publish_time, filter_duration, content_type
    )


@router.get(
    "/users",
    response_model=SearchUsersResponse,
    summary="搜索用户",
    responses={
        200: {"description": "搜索成功", "model": SearchUsersResponse}
    }
)
async def api_search_users(
    keyword: str = Query(..., description="搜索关键词"),
    offset: str = Query(default="0", description="分页偏移量"),
    count: str = Query(default="25", description="每页数量"),
    douyin_user_fans: str = Query(default="", description="粉丝数量: 空不限 0_1k千以下 1k_1w千到万 1w_10w万到十万 10w_100w十万到百万 100w_百万以上"),
    douyin_user_type: str = Query(default="", description="用户类型: 空不限 common_user普通用户 enterprise_user企业用户 personal_user个人认证用户")
):
    """
    搜索抖音用户

    - **keyword**: 搜索关键词
    - **offset**: 分页偏移量
    - **count**: 每页数量
    - **douyin_user_fans**: 粉丝数量筛选
    - **douyin_user_type**: 用户类型筛选

    返回用户搜索结果列表
    """
    if not keyword:
        return SearchUsersResponse(success=False, message="请提供搜索关键词")

    return search_users(keyword, offset, count, douyin_user_fans, douyin_user_type)


@router.get(
    "/lives",
    response_model=SearchLivesResponse,
    summary="搜索直播",
    responses={
        200: {"description": "搜索成功", "model": SearchLivesResponse}
    }
)
async def api_search_lives(
    keyword: str = Query(..., description="搜索关键词"),
    offset: str = Query(default="0", description="分页偏移量"),
    count: str = Query(default="25", description="每页数量")
):
    """
    搜索抖音直播

    - **keyword**: 搜索关键词
    - **offset**: 分页偏移量
    - **count**: 每页数量

    返回直播搜索结果列表
    """
    if not keyword:
        return SearchLivesResponse(success=False, message="请提供搜索关键词")

    return search_lives(keyword, offset, count)
