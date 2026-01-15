"""
搜索相关的 Pydantic 数据模型
"""
from typing import List, Optional
from pydantic import BaseModel, Field


# 搜索作品相关
class SearchWorkItem(BaseModel):
    """搜索作品项"""
    aweme_id: str = Field(default="", description="作品ID")
    desc: str = Field(default="", description="作品描述")
    create_time: int = Field(default=0, description="创建时间戳")
    cover: str = Field(default="", description="封面URL")
    duration: int = Field(default=0, description="时长(毫秒)")
    author_nickname: str = Field(default="", description="作者昵称")
    author_avatar: str = Field(default="", description="作者头像")
    author_sec_uid: str = Field(default="", description="作者安全ID")
    digg_count: int = Field(default=0, description="点赞数")
    comment_count: int = Field(default=0, description="评论数")
    share_count: int = Field(default=0, description="分享数")
    collect_count: int = Field(default=0, description="收藏数")


class SearchWorksResponse(BaseModel):
    """搜索作品响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[SearchWorkItem] = Field(default_factory=list, description="作品列表")
    cursor: str = Field(default="0", description="下一页游标")
    has_more: bool = Field(default=False, description="是否有更多")


# 搜索用户相关
class SearchUserItem(BaseModel):
    """搜索用户项"""
    uid: str = Field(default="", description="用户ID")
    sec_uid: str = Field(default="", description="用户安全ID")
    nickname: str = Field(default="", description="昵称")
    signature: str = Field(default="", description="个性签名")
    avatar: str = Field(default="", description="头像URL")
    follower_count: int = Field(default=0, description="粉丝数")
    total_favorited: int = Field(default=0, description="获赞数")
    aweme_count: int = Field(default=0, description="作品数")
    unique_id: str = Field(default="", description="抖音号")
    custom_verify: str = Field(default="", description="认证信息")


class SearchUsersResponse(BaseModel):
    """搜索用户响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[SearchUserItem] = Field(default_factory=list, description="用户列表")
    cursor: str = Field(default="0", description="下一页游标")
    has_more: bool = Field(default=False, description="是否有更多")


# 搜索直播相关
class SearchLiveItem(BaseModel):
    """搜索直播项"""
    room_id: str = Field(default="", description="直播间ID")
    title: str = Field(default="", description="直播标题")
    cover: str = Field(default="", description="封面URL")
    user_count: int = Field(default=0, description="观看人数")
    anchor_nickname: str = Field(default="", description="主播昵称")
    anchor_avatar: str = Field(default="", description="主播头像")
    anchor_sec_uid: str = Field(default="", description="主播安全ID")


class SearchLivesResponse(BaseModel):
    """搜索直播响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[SearchLiveItem] = Field(default_factory=list, description="直播列表")
    cursor: str = Field(default="0", description="下一页游标")
    has_more: bool = Field(default=False, description="是否有更多")
