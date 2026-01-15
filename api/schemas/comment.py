"""
评论相关的 Pydantic 数据模型
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class CommentUser(BaseModel):
    """评论用户信息"""
    uid: str = Field(default="", description="用户ID")
    sec_uid: str = Field(default="", description="用户安全ID")
    nickname: str = Field(default="", description="昵称")
    avatar: str = Field(default="", description="头像URL")


class CommentItem(BaseModel):
    """评论项"""
    cid: str = Field(default="", description="评论ID")
    aweme_id: str = Field(default="", description="作品ID")
    text: str = Field(default="", description="评论内容")
    create_time: int = Field(default=0, description="创建时间戳")
    digg_count: int = Field(default=0, description="点赞数")
    reply_comment_total: int = Field(default=0, description="回复数")
    user: CommentUser = Field(default_factory=CommentUser, description="评论用户")
    ip_label: str = Field(default="", description="IP属地")


class CommentWithReplies(BaseModel):
    """带回复的评论项"""
    cid: str = Field(default="", description="评论ID")
    aweme_id: str = Field(default="", description="作品ID")
    text: str = Field(default="", description="评论内容")
    create_time: int = Field(default=0, description="创建时间戳")
    digg_count: int = Field(default=0, description="点赞数")
    reply_comment_total: int = Field(default=0, description="回复数")
    user: CommentUser = Field(default_factory=CommentUser, description="评论用户")
    ip_label: str = Field(default="", description="IP属地")
    replies: List[CommentItem] = Field(default_factory=list, description="回复列表")


class CommentListResponse(BaseModel):
    """评论列表响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[CommentItem] = Field(default_factory=list, description="评论列表")
    cursor: str = Field(default="0", description="下一页游标")
    has_more: bool = Field(default=False, description="是否有更多")
    total: int = Field(default=0, description="评论总数")


class CommentRepliesResponse(BaseModel):
    """评论回复响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[CommentItem] = Field(default_factory=list, description="回复列表")
    cursor: str = Field(default="0", description="下一页游标")
    has_more: bool = Field(default=False, description="是否有更多")


class AllCommentsResponse(BaseModel):
    """全部评论响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: List[CommentWithReplies] = Field(default_factory=list, description="全部评论列表")
    total: int = Field(default=0, description="一级评论总数")
