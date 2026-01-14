"""
认证相关的 Pydantic 数据模型
"""
from typing import Optional
from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    """用户信息"""
    uid: str = Field(default="", description="用户 ID")
    nickname: str = Field(default="", description="用户昵称")
    avatar: str = Field(default="", description="头像 URL")


class AuthCheckResponse(BaseModel):
    """Cookie 状态检测响应"""
    valid: bool = Field(..., description="Cookie 是否有效")
    user_info: Optional[UserInfo] = Field(default=None, description="用户信息")
    error: Optional[str] = Field(default=None, description="错误信息")


class QRCodeData(BaseModel):
    """二维码数据"""
    token: str = Field(..., description="二维码 token")
    qrcode_url: str = Field(default="", description="二维码图片 URL")
    qrcode_base64: str = Field(default="", description="二维码图片 Base64")
    expire_at: int = Field(..., description="过期时间戳")


class QRCodeResponse(BaseModel):
    """获取二维码响应"""
    success: bool = Field(..., description="是否成功")
    data: Optional[QRCodeData] = Field(default=None, description="二维码数据")
    error: Optional[str] = Field(default=None, description="错误信息")


class QRCodeStatusResponse(BaseModel):
    """扫码状态响应"""
    status: int = Field(..., description="状态码 (1=等待 2=已扫码 3=确认 4=频繁 5=过期)")
    message: str = Field(..., description="状态消息")
