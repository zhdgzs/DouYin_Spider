"""
视频相关的 Pydantic 数据模型
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class VideoParseRequest(BaseModel):
    """视频解析请求"""
    url: str = Field(..., description="抖音视频链接")


class AuthorInfo(BaseModel):
    """作者信息"""
    nickname: str = Field(default="", description="作者昵称")
    avatar: str = Field(default="", description="头像URL")
    sec_uid: str = Field(default="", description="用户安全ID")


class Statistics(BaseModel):
    """视频统计数据"""
    digg_count: int = Field(default=0, description="点赞数")
    comment_count: int = Field(default=0, description="评论数")
    share_count: int = Field(default=0, description="分享数")
    collect_count: int = Field(default=0, description="收藏数")


class VideoQuality(BaseModel):
    """视频清晰度信息"""
    quality: str = Field(..., description="清晰度标签 (如 720p, 540p)")
    gear_name: str = Field(default="", description="清晰度档位名称")
    width: int = Field(default=0, description="视频宽度")
    height: int = Field(default=0, description="视频高度")
    file_size: int = Field(default=0, description="文件大小 (字节)")
    file_size_str: str = Field(default="", description="文件大小 (可读格式)")
    url: str = Field(..., description="视频下载地址")


class VideoInfo(BaseModel):
    """视频详细信息"""
    video_id: str = Field(..., description="视频ID")
    title: str = Field(default="", description="视频标题")
    desc: str = Field(default="", description="视频描述")
    author: AuthorInfo = Field(default_factory=AuthorInfo, description="作者信息")
    statistics: Statistics = Field(default_factory=Statistics, description="统计数据")
    cover: str = Field(default="", description="封面图URL")
    duration: int = Field(default=0, description="视频时长 (毫秒)")
    create_time: int = Field(default=0, description="创建时间戳")
    video_urls: List[VideoQuality] = Field(default_factory=list, description="多清晰度视频地址")


class VideoParseResponse(BaseModel):
    """视频解析响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: Optional[VideoInfo] = Field(default=None, description="视频信息")


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(..., description="服务状态")
    version: str = Field(..., description="API版本")


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = Field(default=False, description="是否成功")
    message: str = Field(..., description="错误消息")
