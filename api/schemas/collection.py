"""
收藏相关的 Pydantic 数据模型
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class CollectionFolder(BaseModel):
    """收藏夹"""
    collect_id: str = Field(default="", description="收藏夹ID")
    name: str = Field(default="", description="收藏夹名称")
    cover: str = Field(default="", description="封面URL")
    video_count: int = Field(default=0, description="视频数量")
    create_time: int = Field(default=0, description="创建时间戳")


class CollectionListResponse(BaseModel):
    """收藏夹列表响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[CollectionFolder] = Field(default_factory=list, description="收藏夹列表")


class CollectRequest(BaseModel):
    """收藏请求"""
    aweme_id: str = Field(..., description="作品ID")
    action: str = Field(default="1", description="操作: 1收藏 0取消收藏")


class MoveCollectRequest(BaseModel):
    """移动收藏请求"""
    aweme_id: str = Field(..., description="作品ID")
    collect_name: str = Field(..., description="目标收藏夹名称")
    collect_id: str = Field(..., description="目标收藏夹ID")


class RemoveCollectRequest(BaseModel):
    """移除收藏请求"""
    aweme_id: str = Field(..., description="作品ID")
    collect_name: str = Field(..., description="收藏夹名称")
    collect_id: str = Field(..., description="收藏夹ID")


class CollectResponse(BaseModel):
    """收藏操作响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
