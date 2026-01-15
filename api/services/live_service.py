"""
直播服务层
封装对 DouyinAPI 直播相关方法的调用
"""
import os
import sys
from loguru import logger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dy_apis.douyin_api import DouyinAPI
from builder.auth import DouyinAuth
from api.schemas.live import (
    LiveInfo, LiveInfoResponse,
    ProductItem, ProductListResponse, AllProductsResponse,
    ProductDetail, ProductDetailResponse
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


def _extract_live_id(url: str) -> str:
    """从直播间链接提取直播间ID"""
    # https://live.douyin.com/123456789
    if "live.douyin.com" in url:
        return url.split("/")[-1].split("?")[0]
    return ""


def _extract_product_item(item: dict) -> ProductItem:
    """提取商品项"""
    # 提取封面
    cover = ""
    cover_data = item.get("cover", {})
    if cover_data and "url_list" in cover_data:
        cover = cover_data["url_list"][0] if cover_data["url_list"] else ""

    # 价格转换（分转元）
    price = item.get("price", 0) / 100 if item.get("price") else 0
    market_price = item.get("market_price", 0) / 100 if item.get("market_price") else 0

    return ProductItem(
        promotion_id=str(item.get("promotion_id", "")),
        product_id=str(item.get("product_id", "")),
        title=item.get("title", ""),
        cover=cover,
        price=price,
        market_price=market_price,
        sales=item.get("sales", 0),
        in_stock=item.get("in_stock", True)
    )


def get_live_info(url: str) -> LiveInfoResponse:
    """
    获取直播间信息

    :param url: 直播间链接
    :return: LiveInfoResponse
    """
    try:
        auth = _get_auth()
        live_id = _extract_live_id(url)

        if not live_id:
            return LiveInfoResponse(success=False, message="无法解析直播间ID")

        result = DouyinAPI.get_live_info(auth, live_id)

        if not result or result == (None, None, None):
            return LiveInfoResponse(success=False, message="无法获取直播间信息")

        live_info = LiveInfo(
            room_id=result.get("room_id", ""),
            user_id=result.get("user_id", ""),
            room_status=result.get("room_status", ""),
            room_title=result.get("room_title", ""),
            is_living=result.get("room_status") == "2"
        )

        return LiveInfoResponse(
            success=True,
            message="获取成功",
            data=live_info
        )
    except ValueError as e:
        return LiveInfoResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取直播间信息失败: {e}")
        return LiveInfoResponse(success=False, message=f"获取失败: {str(e)}")


def get_live_products(
    url: str,
    room_id: str,
    author_id: str,
    offset: str = "0"
) -> ProductListResponse:
    """
    获取直播商品列表

    :param url: 直播间链接
    :param room_id: 直播间ID
    :param author_id: 主播ID
    :param offset: 分页偏移量
    :return: ProductListResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_live_production(auth, url, room_id, author_id, offset)

        if not result:
            return ProductListResponse(success=False, message="获取商品列表失败")

        data = result.get("data", {})
        promotions = data.get("promotions", [])
        products = [_extract_product_item(p) for p in promotions]

        return ProductListResponse(
            success=True,
            message="获取成功",
            data=products,
            offset=str(data.get("offset", "0")),
            has_more=data.get("has_more", False),
            total=data.get("total", 0)
        )
    except ValueError as e:
        return ProductListResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取直播商品列表失败: {e}")
        return ProductListResponse(success=False, message=f"获取失败: {str(e)}")


def get_all_live_products(url: str, room_id: str, author_id: str) -> AllProductsResponse:
    """
    获取全部直播商品

    :param url: 直播间链接
    :param room_id: 直播间ID
    :param author_id: 主播ID
    :return: AllProductsResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_all_live_production(auth, url, room_id, author_id)

        if not result:
            return AllProductsResponse(
                success=True,
                message="该直播间暂无商品",
                data=[],
                total=0
            )

        products = [_extract_product_item(p) for p in result]

        return AllProductsResponse(
            success=True,
            message="获取成功",
            data=products,
            total=len(products)
        )
    except ValueError as e:
        return AllProductsResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取全部直播商品失败: {e}")
        return AllProductsResponse(success=False, message=f"获取失败: {str(e)}")


def get_product_detail(
    url: str,
    promotion_id: str,
    sec_author_id: str,
    room_id: str
) -> ProductDetailResponse:
    """
    获取商品详情

    :param url: 直播间链接
    :param promotion_id: 商品推广ID
    :param sec_author_id: 主播安全ID
    :param room_id: 直播间ID
    :return: ProductDetailResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_live_production_detail(
            auth, url, promotion_id, sec_author_id, room_id
        )

        if not result:
            return ProductDetailResponse(success=False, message="获取商品详情失败")

        data = result.get("data", {})
        product_data = data.get("product", {})

        # 提取图片列表
        images = []
        images_data = product_data.get("images", [])
        for img in images_data:
            if img and "url_list" in img:
                images.append(img["url_list"][0] if img["url_list"] else "")

        # 提取封面
        cover = images[0] if images else ""

        # 价格转换
        price = product_data.get("price", 0) / 100 if product_data.get("price") else 0
        market_price = product_data.get("market_price", 0) / 100 if product_data.get("market_price") else 0

        detail = ProductDetail(
            promotion_id=str(product_data.get("promotion_id", "")),
            product_id=str(product_data.get("product_id", "")),
            title=product_data.get("title", ""),
            cover=cover,
            images=images,
            price=price,
            market_price=market_price,
            sales=product_data.get("sales", 0),
            description=product_data.get("description", ""),
            shop_name=product_data.get("shop_name", "")
        )

        return ProductDetailResponse(
            success=True,
            message="获取成功",
            data=detail
        )
    except ValueError as e:
        return ProductDetailResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取商品详情失败: {e}")
        return ProductDetailResponse(success=False, message=f"获取失败: {str(e)}")
