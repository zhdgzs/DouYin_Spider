"""
认证服务
提供 Cookie 验证和用户信息获取功能
"""
from typing import Optional
from dataclasses import dataclass
from loguru import logger

import requests

requests.packages.urllib3.disable_warnings()

from utils.qrcode_login import (
    get_cookie_from_env,
    get_qrcode,
    check_qrconnect,
    login_redirect,
    save_cookie_to_env,
    QRCodeResult,
    StatusResult,
    QRCodeStatus,
)
from builder.auth import DouyinAuth
from dy_apis.douyin_api import DouyinAPI


@dataclass
class UserInfo:
    """用户信息"""
    uid: str = ""
    nickname: str = ""
    avatar: str = ""


@dataclass
class AuthCheckResult:
    """认证检查结果"""
    valid: bool
    user_info: Optional[UserInfo] = None
    error: str = ""


def check_cookie_valid(cookie_str: Optional[str] = None) -> AuthCheckResult:
    """
    检查 Cookie 是否有效

    通过调用 DouyinAPI.get_my_uid 来验证 Cookie 有效性。

    Args:
        cookie_str: Cookie 字符串，为空则从 .env 读取

    Returns:
        AuthCheckResult: 认证检查结果
    """
    # 获取 Cookie
    if not cookie_str:
        cookie_str = get_cookie_from_env()

    if not cookie_str:
        return AuthCheckResult(valid=False, error="Cookie 不存在")

    try:
        # 使用 DouyinAuth 处理 Cookie
        auth = DouyinAuth()
        auth.perepare_auth(cookie_str)

        # 检查关键 Cookie 字段是否存在
        required_fields = ['sessionid', 's_v_web_id']
        for field in required_fields:
            if field not in auth.cookie or not auth.cookie[field]:
                return AuthCheckResult(valid=False, error=f"Cookie 缺少必要字段: {field}")

        # 使用 DouyinAPI.get_my_uid 验证 Cookie 有效性
        try:
            uid = DouyinAPI.get_my_uid(auth)
            if uid:
                user_info = UserInfo(
                    uid=str(uid),
                    nickname="",  # API 不返回昵称
                    avatar=""     # API 不返回头像
                )
                logger.info(f"Cookie 验证成功，UID: {uid}")
                return AuthCheckResult(valid=True, user_info=user_info)
            else:
                return AuthCheckResult(valid=False, error="无法获取用户 ID")
        except KeyError as e:
            logger.warning(f"Cookie 验证失败，缺少字段: {e}")
            return AuthCheckResult(valid=False, error=f"Cookie 无效，缺少必要字段")
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"Cookie 验证失败: {error_msg}")
            if "user_uid" in error_msg or "KeyError" in error_msg:
                return AuthCheckResult(valid=False, error="Cookie 无效或已过期")
            return AuthCheckResult(valid=False, error=f"验证失败: {error_msg}")

    except requests.Timeout:
        return AuthCheckResult(valid=False, error="请求超时")
    except Exception as e:
        return AuthCheckResult(valid=False, error=f"验证失败: {str(e)}")


async def get_login_qrcode() -> QRCodeResult:
    """
    获取登录二维码

    Returns:
        QRCodeResult: 二维码获取结果
    """
    return await get_qrcode()


async def check_qrcode_status(token: str) -> StatusResult:
    """
    检查扫码状态

    Args:
        token: 二维码 token

    Returns:
        StatusResult: 扫码状态结果
    """
    result = await check_qrconnect(token)

    # 登录成功时，获取并保存 Cookie
    if result.status == QRCodeStatus.CONFIRMED and result.redirect_url:
        success, cookie_str, error = login_redirect(result.redirect_url)

        if success and cookie_str:
            # 保存 Cookie 到 .env
            save_success, save_error = save_cookie_to_env(cookie_str)

            if save_success:
                result.cookie = cookie_str
                result.message = "登录成功，Cookie 已保存"
            else:
                result.message = f"登录成功，但 Cookie 保存失败: {save_error}"
        else:
            result.message = f"登录成功，但获取 Cookie 失败: {error}"

    return result
