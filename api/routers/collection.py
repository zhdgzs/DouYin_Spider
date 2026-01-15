"""
收藏相关路由
"""
from fastapi import APIRouter, Query, Body
from loguru import logger

from api.schemas.collection import (
    CollectionListResponse, CollectResponse,
    CollectRequest, MoveCollectRequest, RemoveCollectRequest
)
from api.services.collection_service import (
    get_collection_list, collect_aweme, move_collect_aweme, remove_collect_aweme
)

router = APIRouter(prefix="/api/collection", tags=["collection"])


@router.get(
    "/list",
    response_model=CollectionListResponse,
    summary="获取收藏夹列表",
    responses={
        200: {"description": "获取成功", "model": CollectionListResponse}
    }
)
async def api_get_collection_list():
    """
    获取当前用户的收藏夹列表

    返回所有收藏夹的信息
    """
    return get_collection_list()


@router.post(
    "/add",
    response_model=CollectResponse,
    summary="收藏作品",
    responses={
        200: {"description": "操作成功", "model": CollectResponse}
    }
)
async def api_collect_aweme(request: CollectRequest):
    """
    收藏或取消收藏作品

    - **aweme_id**: 作品ID
    - **action**: 操作类型，1为收藏，0为取消收藏

    返回操作结果
    """
    if not request.aweme_id:
        return CollectResponse(success=False, message="请提供作品ID")

    return collect_aweme(request.aweme_id, request.action)


@router.post(
    "/move",
    response_model=CollectResponse,
    summary="移动收藏",
    responses={
        200: {"description": "操作成功", "model": CollectResponse}
    }
)
async def api_move_collect_aweme(request: MoveCollectRequest):
    """
    移动作品到指定收藏夹

    - **aweme_id**: 作品ID
    - **collect_name**: 目标收藏夹名称
    - **collect_id**: 目标收藏夹ID

    ⚠️ 注意：作品需要先被收藏才能移动

    返回操作结果
    """
    if not request.aweme_id:
        return CollectResponse(success=False, message="请提供作品ID")

    if not request.collect_name:
        return CollectResponse(success=False, message="请提供收藏夹名称")

    if not request.collect_id:
        return CollectResponse(success=False, message="请提供收藏夹ID")

    return move_collect_aweme(request.aweme_id, request.collect_name, request.collect_id)


@router.delete(
    "/remove",
    response_model=CollectResponse,
    summary="移除收藏",
    responses={
        200: {"description": "操作成功", "model": CollectResponse}
    }
)
async def api_remove_collect_aweme(
    aweme_id: str = Query(..., description="作品ID"),
    collect_name: str = Query(..., description="收藏夹名称"),
    collect_id: str = Query(..., description="收藏夹ID")
):
    """
    从收藏夹移除作品

    - **aweme_id**: 作品ID
    - **collect_name**: 收藏夹名称
    - **collect_id**: 收藏夹ID

    返回操作结果
    """
    if not aweme_id:
        return CollectResponse(success=False, message="请提供作品ID")

    if not collect_name:
        return CollectResponse(success=False, message="请提供收藏夹名称")

    if not collect_id:
        return CollectResponse(success=False, message="请提供收藏夹ID")

    return remove_collect_aweme(aweme_id, collect_name, collect_id)
