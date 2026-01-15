"""
关系相关的 Pydantic 数据模型
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class RelationUser(BaseModel):
    """关系用户信息"""
    uid: str = Field(default="", description="用户ID")
    sec_uid: str = Field(default="", description="用户安全ID")
    nickname: str = Field(default="", description="昵称")
    signature: str = Field(default="", description="个性签名")
    avatar: str = Field(default="", description="头像URL")
    follower_count: int = Field(default=0, description="粉丝数")
    following_count: int = Field(default=0, description="关注数")
    aweme_count: int = Field(default=0, description="作品数")
    unique_id: str = Field(default="", description="抖音号")
    is_following: bool = Field(default=False, description="是否已关注")


class FollowerListResponse(BaseModel):
    """粉丝列表响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[RelationUser] = Field(default_factory=list, description="粉丝列表")
    max_time: str = Field(default="0", description="下一页时间戳")
    has_more: bool = Field(default=False, description="是否有更多")
    total: int = Field(default=0, description="粉丝总数")


class FollowingListResponse(BaseModel):
    """关注列表响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[RelationUser] = Field(default_factory=list, description="关注列表")
    max_time: str = Field(default="0", description="下一页时间戳")
    has_more: bool = Field(default=False, description="是否有更多")
    total: int = Field(default=0, description="关注总数")


class NoticeItem(BaseModel):
    """通知项"""
    notice_id: str = Field(default="", description="通知ID")
    notice_type: int = Field(default=0, description="通知类型")
    content: str = Field(default="", description="通知内容")
    create_time: int = Field(default=0, description="创建时间戳")
    from_user_nickname: str = Field(default="", description="来源用户昵称")
    from_user_avatar: str = Field(default="", description="来源用户头像")
    from_user_sec_uid: str = Field(default="", description="来源用户安全ID")
    aweme_id: str = Field(default="", description="相关作品ID")
    aweme_cover: str = Field(default="", description="相关作品封面")


class NoticeListResponse(BaseModel):
    """通知列表响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[NoticeItem] = Field(default_factory=list, description="通知列表")
    max_time: str = Field(default="0", description="下一页时间戳")
    has_more: bool = Field(default=False, description="是否有更多")
