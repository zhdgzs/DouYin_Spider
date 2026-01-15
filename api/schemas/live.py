"""
直播相关的 Pydantic 数据模型
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class LiveInfo(BaseModel):
    """直播间信息"""
    room_id: str = Field(default="", description="直播间ID")
    user_id: str = Field(default="", description="主播用户ID")
    room_status: str = Field(default="", description="直播状态: 2直播中 4未开播")
    room_title: str = Field(default="", description="直播间标题")
    is_living: bool = Field(default=False, description="是否正在直播")


class LiveInfoResponse(BaseModel):
    """直播间信息响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: Optional[LiveInfo] = Field(default=None, description="直播间信息")


class ProductItem(BaseModel):
    """商品项"""
    promotion_id: str = Field(default="", description="商品推广ID")
    product_id: str = Field(default="", description="商品ID")
    title: str = Field(default="", description="商品标题")
    cover: str = Field(default="", description="商品封面")
    price: float = Field(default=0, description="价格(元)")
    market_price: float = Field(default=0, description="原价(元)")
    sales: int = Field(default=0, description="销量")
    in_stock: bool = Field(default=True, description="是否有货")


class ProductListResponse(BaseModel):
    """商品列表响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[ProductItem] = Field(default_factory=list, description="商品列表")
    offset: str = Field(default="0", description="下一页偏移量")
    has_more: bool = Field(default=False, description="是否有更多")
    total: int = Field(default=0, description="商品总数")


class AllProductsResponse(BaseModel):
    """全部商品响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[ProductItem] = Field(default_factory=list, description="全部商品列表")
    total: int = Field(default=0, description="商品总数")


class ProductDetail(BaseModel):
    """商品详情"""
    promotion_id: str = Field(default="", description="商品推广ID")
    product_id: str = Field(default="", description="商品ID")
    title: str = Field(default="", description="商品标题")
    cover: str = Field(default="", description="商品封面")
    images: List[str] = Field(default_factory=list, description="商品图片列表")
    price: float = Field(default=0, description="价格(元)")
    market_price: float = Field(default=0, description="原价(元)")
    sales: int = Field(default=0, description="销量")
    description: str = Field(default="", description="商品描述")
    shop_name: str = Field(default="", description="店铺名称")


class ProductDetailResponse(BaseModel):
    """商品详情响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: Optional[ProductDetail] = Field(default=None, description="商品详情")
