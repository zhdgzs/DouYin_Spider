"""
直播相关路由
"""
from fastapi import APIRouter, Query
from loguru import logger

from api.schemas.live import (
    LiveInfoResponse, ProductListResponse, AllProductsResponse, ProductDetailResponse
)
from api.services.live_service import (
    get_live_info, get_live_products, get_all_live_products, get_product_detail
)

router = APIRouter(prefix="/api/live", tags=["live"])


@router.get(
    "/info",
    response_model=LiveInfoResponse,
    summary="获取直播间信息",
    responses={
        200: {"description": "获取成功", "model": LiveInfoResponse}
    }
)
async def api_get_live_info(
    url: str = Query(..., description="直播间链接")
):
    """
    获取抖音直播间信息

    - **url**: 直播间链接 (如 https://live.douyin.com/123456789)

    返回直播间ID、主播ID、直播状态等信息
    """
    if not url:
        return LiveInfoResponse(success=False, message="请提供直播间链接")

    if "live.douyin.com" not in url:
        return LiveInfoResponse(success=False, message="请提供有效的抖音直播间链接")

    return get_live_info(url)


@router.get(
    "/products",
    response_model=ProductListResponse,
    summary="获取直播商品列表",
    responses={
        200: {"description": "获取成功", "model": ProductListResponse}
    }
)
async def api_get_live_products(
    url: str = Query(..., description="直播间链接"),
    room_id: str = Query(..., description="直播间ID"),
    author_id: str = Query(..., description="主播ID"),
    offset: str = Query(default="0", description="分页偏移量")
):
    """
    获取直播间商品列表（分页）

    - **url**: 直播间链接
    - **room_id**: 直播间ID（可从 /api/live/info 获取）
    - **author_id**: 主播ID（可从 /api/live/info 获取）
    - **offset**: 分页偏移量

    返回商品列表及分页信息
    """
    if not url:
        return ProductListResponse(success=False, message="请提供直播间链接")

    if not room_id:
        return ProductListResponse(success=False, message="请提供直播间ID")

    if not author_id:
        return ProductListResponse(success=False, message="请提供主播ID")

    return get_live_products(url, room_id, author_id, offset)


@router.get(
    "/products/all",
    response_model=AllProductsResponse,
    summary="获取全部直播商品",
    responses={
        200: {"description": "获取成功", "model": AllProductsResponse}
    }
)
async def api_get_all_live_products(
    url: str = Query(..., description="直播间链接"),
    room_id: str = Query(..., description="直播间ID"),
    author_id: str = Query(..., description="主播ID")
):
    """
    获取直播间全部商品

    - **url**: 直播间链接
    - **room_id**: 直播间ID
    - **author_id**: 主播ID

    ⚠️ 注意：此接口会获取全部商品，商品数量较多时可能耗时较长

    返回全部商品列表
    """
    if not url:
        return AllProductsResponse(success=False, message="请提供直播间链接")

    if not room_id:
        return AllProductsResponse(success=False, message="请提供直播间ID")

    if not author_id:
        return AllProductsResponse(success=False, message="请提供主播ID")

    return get_all_live_products(url, room_id, author_id)


@router.get(
    "/product/detail",
    response_model=ProductDetailResponse,
    summary="获取商品详情",
    responses={
        200: {"description": "获取成功", "model": ProductDetailResponse}
    }
)
async def api_get_product_detail(
    url: str = Query(..., description="直播间链接"),
    promotion_id: str = Query(..., description="商品推广ID"),
    sec_author_id: str = Query(..., description="主播安全ID"),
    room_id: str = Query(..., description="直播间ID")
):
    """
    获取直播商品详情

    - **url**: 直播间链接
    - **promotion_id**: 商品推广ID（从商品列表获取）
    - **sec_author_id**: 主播安全ID
    - **room_id**: 直播间ID

    返回商品详细信息
    """
    if not url:
        return ProductDetailResponse(success=False, message="请提供直播间链接")

    if not promotion_id:
        return ProductDetailResponse(success=False, message="请提供商品推广ID")

    if not sec_author_id:
        return ProductDetailResponse(success=False, message="请提供主播安全ID")

    if not room_id:
        return ProductDetailResponse(success=False, message="请提供直播间ID")

    return get_product_detail(url, promotion_id, sec_author_id, room_id)
