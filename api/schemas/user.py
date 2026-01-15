"""
用户相关的 Pydantic 数据模型
"""
from typing import List, Optional, Any
from pydantic import BaseModel, Field


class UserInfoRequest(BaseModel):
    """用户信息请求"""
    url: str = Field(..., description="用户主页链接")


class UserWorksRequest(BaseModel):
    """用户作品列表请求"""
    url: str = Field(..., description="用户主页链接")
    max_cursor: str = Field(default="0", description="分页游标")


class UserInfo(BaseModel):
    """用户详细信息"""
    uid: str = Field(default="", description="用户ID")
    sec_uid: str = Field(default="", description="用户安全ID")
    nickname: str = Field(default="", description="昵称")
    signature: str = Field(default="", description="个性签名")
    avatar: str = Field(default="", description="头像URL")
    avatar_larger: str = Field(default="", description="大头像URL")
    follower_count: int = Field(default=0, description="粉丝数")
    following_count: int = Field(default=0, description="关注数")
    total_favorited: int = Field(default=0, description="获赞数")
    aweme_count: int = Field(default=0, description="作品数")
    favoriting_count: int = Field(default=0, description="喜欢数")
    unique_id: str = Field(default="", description="抖音号")
    short_id: str = Field(default="", description="短ID")
    is_verified: bool = Field(default=False, description="是否认证")
    verification_type: int = Field(default=0, description="认证类型")
    custom_verify: str = Field(default="", description="认证信息")
    enterprise_verify_reason: str = Field(default="", description="企业认证信息")
    ip_location: str = Field(default="", description="IP属地")


class UserInfoResponse(BaseModel):
    """用户信息响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: Optional[UserInfo] = Field(default=None, description="用户信息")


class WorkItem(BaseModel):
    """作品项"""
    aweme_id: str = Field(default="", description="作品ID")
    desc: str = Field(default="", description="作品描述")
    create_time: int = Field(default=0, description="创建时间戳")
    cover: str = Field(default="", description="封面URL")
    duration: int = Field(default=0, description="时长(毫秒)")
    digg_count: int = Field(default=0, description="点赞数")
    comment_count: int = Field(default=0, description="评论数")
    share_count: int = Field(default=0, description="分享数")
    collect_count: int = Field(default=0, description="收藏数")
    play_count: int = Field(default=0, description="播放数")


class UserWorksResponse(BaseModel):
    """用户作品列表响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[WorkItem] = Field(default_factory=list, description="作品列表")
    max_cursor: str = Field(default="0", description="下一页游标")
    has_more: bool = Field(default=False, description="是否有更多")


class UserAllWorksResponse(BaseModel):
    """用户全部作品响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[WorkItem] = Field(default_factory=list, description="全部作品列表")
    total: int = Field(default=0, description="作品总数")
