"""
认证相关 API 路由
提供 Cookie 检测、二维码获取、扫码状态轮询等接口
"""
from fastapi import APIRouter, Query, Body
from loguru import logger

from api.schemas.auth import (
    AuthCheckResponse,
    QRCodeResponse,
    QRCodeData,
    QRCodeStatusResponse,
    UserInfo,
)
from api.services.auth_service import (
    check_cookie_valid,
    get_login_qrcode,
    check_qrcode_status,
)
from utils.qrcode_login import save_cookie_to_env

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.get("/check", response_model=AuthCheckResponse, summary="检测 Cookie 状态")
async def check_auth():
    """
    检测当前 Cookie 是否有效

    - 有效时返回用户基本信息（UID、昵称、头像）
    - 无效时返回错误信息
    """
    logger.info("检测 Cookie 状态")

    result = check_cookie_valid()

    if result.valid and result.user_info:
        return AuthCheckResponse(
            valid=True,
            user_info=UserInfo(
                uid=result.user_info.uid,
                nickname=result.user_info.nickname,
                avatar=result.user_info.avatar,
            )
        )
    else:
        return AuthCheckResponse(
            valid=False,
            error=result.error
        )


@router.get("/qrcode", response_model=QRCodeResponse, summary="获取登录二维码")
async def get_qrcode():
    """
    获取抖音扫码登录二维码

    返回:
    - token: 用于轮询扫码状态的 token
    - qrcode_url: 二维码图片 URL
    - qrcode_base64: 二维码图片 Base64 编码
    - expire_at: 二维码过期时间戳（约 5 分钟）
    """
    logger.info("获取登录二维码")

    result = await get_login_qrcode()

    if result.success:
        return QRCodeResponse(
            success=True,
            data=QRCodeData(
                token=result.token,
                qrcode_url=result.qrcode_url,
                qrcode_base64=result.qrcode_base64,
                expire_at=result.expire_at,
            )
        )
    else:
        logger.warning(f"获取二维码失败: {result.error}")
        return QRCodeResponse(
            success=False,
            error=result.error
        )


@router.get("/qrcode/status", response_model=QRCodeStatusResponse, summary="检查扫码状态")
async def check_status(token: str = Query(..., description="二维码 token")):
    """
    检查扫码状态

    状态码说明:
    - 1: 等待扫码
    - 2: 已扫码，等待确认
    - 3: 确认登录（登录成功）
    - 4: 访问频繁
    - 5: 二维码过期
    """
    logger.debug(f"检查扫码状态: token={token[:20]}...")

    result = await check_qrcode_status(token)

    if result.status == 3:
        logger.info("扫码登录成功")

    return QRCodeStatusResponse(
        status=result.status,
        message=result.message
    )


@router.get("/cookie", summary="获取当前 Cookie")
async def get_cookie():
    """
    获取当前保存的 Cookie 值（用于回显）

    返回:
    - cookie: 当前保存的 Cookie 字符串（脱敏处理）
    - raw_cookie: 完整的 Cookie 字符串
    """
    from utils.qrcode_login import get_cookie_from_env

    cookie_str = get_cookie_from_env()

    if cookie_str:
        # 脱敏处理：只显示前50个字符和后20个字符
        if len(cookie_str) > 100:
            masked = f"{cookie_str[:50]}...{cookie_str[-20:]}"
        else:
            masked = cookie_str

        return {
            "success": True,
            "cookie": masked,
            "raw_cookie": cookie_str,
            "length": len(cookie_str)
        }
    else:
        return {
            "success": False,
            "cookie": None,
            "raw_cookie": None,
            "error": "未找到保存的 Cookie"
        }


@router.post("/cookie", summary="手动设置 Cookie")
async def set_cookie(cookie: str = Body(..., embed=True, description="Cookie 字符串")):
    """
    手动设置 Cookie（备选方案）

    当扫码登录不可用时，可以手动从浏览器复制 Cookie 并设置。

    获取 Cookie 方法：
    1. 打开浏览器访问 https://www.douyin.com
    2. 登录账号
    3. 按 F12 打开开发者工具
    4. 切换到 Network 标签
    5. 刷新页面，找到任意请求
    6. 在 Request Headers 中找到 Cookie 字段
    7. 复制完整的 Cookie 值
    """
    logger.info("手动设置 Cookie")

    if not cookie or len(cookie) < 10:
        return {"success": False, "error": "Cookie 不能为空"}

    success, error = save_cookie_to_env(cookie)

    if success:
        # 验证 Cookie 是否有效
        result = check_cookie_valid(cookie)
        if result.valid:
            return {
                "success": True,
                "message": "Cookie 设置成功",
                "user_info": {
                    "uid": result.user_info.uid if result.user_info else "",
                    "nickname": result.user_info.nickname if result.user_info else "",
                    "avatar": result.user_info.avatar if result.user_info else "",
                }
            }
        else:
            return {
                "success": True,
                "message": "Cookie 已保存，但验证失败（可能已过期）",
                "warning": result.error
            }
    else:
        return {"success": False, "error": f"Cookie 保存失败: {error}"}
