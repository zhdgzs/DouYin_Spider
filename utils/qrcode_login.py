"""
抖音扫码登录模块
通过 Playwright 实现扫码登录获取 Cookie
"""
import re
import time
import asyncio
import base64
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import IntEnum

import requests

requests.packages.urllib3.disable_warnings()


class QRCodeStatus(IntEnum):
    """扫码状态码"""
    WAITING = 1       # 等待扫码
    SCANNED = 2       # 已扫码，等待确认
    CONFIRMED = 3     # 确认登录
    RATE_LIMITED = 4  # 访问频繁
    EXPIRED = 5       # 二维码过期


@dataclass
class QRCodeResult:
    """二维码获取结果"""
    success: bool
    token: str = ""
    qrcode_url: str = ""
    qrcode_base64: str = ""
    expire_at: int = 0
    error: str = ""


@dataclass
class StatusResult:
    """扫码状态结果"""
    status: QRCodeStatus
    message: str
    cookie: str = ""
    redirect_url: str = ""


# 常量
SSO_BASE_URL = "https://sso.douyin.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# 全局状态存储（用于 Playwright 方式）
_qrcode_state = {
    "token": "",
    "qrcode_base64": "",
    "status": QRCodeStatus.WAITING,
    "cookie": "",
    "page": None,
    "browser": None,
}


def generate_verify_fp(length: int = 16) -> str:
    """
    生成设备指纹 verifyFp
    """
    import random
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    timestamp = str(int(time.time() * 1000))
    random_str = ''.join(random.choice(chars) for _ in range(length))
    return f"verify_{timestamp}_{random_str}"


def generate_device_id() -> str:
    """
    生成设备 ID
    """
    import random
    return ''.join(str(random.randint(0, 9)) for _ in range(19))


def get_ttwid() -> Optional[str]:
    """
    获取 ttwid
    """
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        response = requests.get(
            "https://www.douyin.com/",
            headers=headers,
            verify=False,
            timeout=10
        )
        return response.cookies.get("ttwid")
    except Exception:
        return None


async def get_qrcode_playwright() -> QRCodeResult:
    """
    使用 Playwright 获取登录二维码

    Returns:
        QRCodeResult: 包含二维码信息
    """
    try:
        from playwright.async_api import async_playwright

        global _qrcode_state

        # 启动浏览器
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )

        context = await browser.new_context(
            user_agent=USER_AGENT,
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        # 保存引用
        _qrcode_state["browser"] = browser
        _qrcode_state["page"] = page
        _qrcode_state["playwright"] = playwright

        # 访问登录页面（使用 domcontentloaded 避免等待所有网络请求）
        await page.goto("https://www.douyin.com/", wait_until="domcontentloaded", timeout=60000)

        # 等待页面基本加载
        await asyncio.sleep(3)

        # 点击登录按钮（尝试多种选择器）
        login_clicked = False
        login_selectors = [
            'button:has-text("登录")',
            '[class*="login"]',
            'text="登录"',
            '[data-e2e="login-button"]',
        ]
        for selector in login_selectors:
            try:
                login_btn = await page.wait_for_selector(selector, timeout=3000)
                if login_btn:
                    await login_btn.click()
                    login_clicked = True
                    await asyncio.sleep(2)
                    break
            except Exception:
                continue

        if not login_clicked:
            # 尝试直接访问登录页面
            await page.goto("https://www.douyin.com/passport/web/login/", wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(2)

        # 等待二维码出现（尝试多种选择器）
        qrcode_selectors = [
            'img[src*="qrcode"]',
            'img[src*="qr"]',
            '[class*="qrcode"] img',
            'canvas[class*="qr"]',
        ]

        qrcode_element = None
        for selector in qrcode_selectors:
            try:
                qrcode_element = await page.wait_for_selector(selector, timeout=5000)
                if qrcode_element:
                    break
            except Exception:
                continue

        if qrcode_element:
            qrcode_url = await qrcode_element.get_attribute('src') or ""

            # 截图二维码
            try:
                screenshot = await qrcode_element.screenshot()
                qrcode_base64 = f"data:image/png;base64,{base64.b64encode(screenshot).decode()}"
            except Exception:
                # 如果元素截图失败，尝试区域截图
                qrcode_box = await qrcode_element.bounding_box()
                if qrcode_box:
                    screenshot = await page.screenshot(clip=qrcode_box)
                    qrcode_base64 = f"data:image/png;base64,{base64.b64encode(screenshot).decode()}"
                else:
                    await cleanup_playwright()
                    return QRCodeResult(success=False, error="无法截取二维码图片")

            _qrcode_state["qrcode_base64"] = qrcode_base64
            _qrcode_state["token"] = str(int(time.time() * 1000))
            _qrcode_state["status"] = QRCodeStatus.WAITING

            return QRCodeResult(
                success=True,
                token=_qrcode_state["token"],
                qrcode_url=qrcode_url,
                qrcode_base64=qrcode_base64,
                expire_at=int(time.time()) + 300
            )
        else:
            await cleanup_playwright()
            return QRCodeResult(success=False, error="未找到登录二维码，请使用手动输入 Cookie 方式")

    except ImportError:
        return QRCodeResult(success=False, error="请安装 playwright: pip install playwright && playwright install chromium")
    except Exception as e:
        await cleanup_playwright()
        return QRCodeResult(success=False, error=str(e))


async def check_qrconnect_playwright(token: str) -> StatusResult:
    """
    使用 Playwright 检查扫码状态

    Args:
        token: 二维码 token

    Returns:
        StatusResult: 扫码状态结果
    """
    global _qrcode_state

    if not _qrcode_state.get("page"):
        return StatusResult(status=QRCodeStatus.EXPIRED, message="会话已过期，请刷新二维码")

    page = _qrcode_state["page"]

    try:
        # 检查是否已登录成功（URL 变化或出现用户头像）
        current_url = page.url

        # 检查是否有用户头像（登录成功标志）
        try:
            avatar = await page.query_selector('[class*="avatar"]')
            if avatar and "passport" not in current_url:
                # 登录成功，获取 Cookie
                cookies = await page.context.cookies()
                cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

                _qrcode_state["cookie"] = cookie_str
                _qrcode_state["status"] = QRCodeStatus.CONFIRMED

                # 保存 Cookie
                save_success, save_error = save_cookie_to_env(cookie_str)

                await cleanup_playwright()

                if save_success:
                    return StatusResult(
                        status=QRCodeStatus.CONFIRMED,
                        message="登录成功，Cookie 已保存",
                        cookie=cookie_str
                    )
                else:
                    return StatusResult(
                        status=QRCodeStatus.CONFIRMED,
                        message=f"登录成功，但 Cookie 保存失败: {save_error}",
                        cookie=cookie_str
                    )
        except Exception:
            pass

        # 检查二维码是否过期
        try:
            expired_text = await page.query_selector('text="二维码已过期"')
            if expired_text:
                _qrcode_state["status"] = QRCodeStatus.EXPIRED
                return StatusResult(status=QRCodeStatus.EXPIRED, message="二维码已过期")
        except Exception:
            pass

        # 检查是否已扫码
        try:
            scanned_text = await page.query_selector('text="扫码成功"')
            if scanned_text:
                _qrcode_state["status"] = QRCodeStatus.SCANNED
                return StatusResult(status=QRCodeStatus.SCANNED, message="扫码成功，请在手机上确认")
        except Exception:
            pass

        return StatusResult(status=QRCodeStatus.WAITING, message="等待扫码")

    except Exception as e:
        return StatusResult(status=QRCodeStatus.WAITING, message=f"检查状态失败: {str(e)}")


async def cleanup_playwright():
    """清理 Playwright 资源"""
    global _qrcode_state

    try:
        if _qrcode_state.get("browser"):
            await _qrcode_state["browser"].close()
    except Exception:
        pass

    try:
        if _qrcode_state.get("playwright"):
            await _qrcode_state["playwright"].stop()
    except Exception:
        pass

    _qrcode_state["page"] = None
    _qrcode_state["browser"] = None
    _qrcode_state["playwright"] = None


async def get_qrcode() -> QRCodeResult:
    """
    获取登录二维码（异步）

    Returns:
        QRCodeResult: 包含二维码 URL、token、base64 图片等信息
    """
    try:
        return await get_qrcode_playwright()
    except Exception as e:
        return QRCodeResult(success=False, error=str(e))


async def check_qrconnect(token: str) -> StatusResult:
    """
    检查扫码状态（异步）

    Args:
        token: 二维码 token

    Returns:
        StatusResult: 扫码状态结果
    """
    try:
        return await check_qrconnect_playwright(token)
    except Exception as e:
        return StatusResult(status=QRCodeStatus.WAITING, message=f"检查状态失败: {str(e)}")


def login_redirect(redirect_url: str) -> Tuple[bool, str, str]:
    """
    处理登录重定向，获取 Cookie

    Args:
        redirect_url: 登录成功后的重定向 URL

    Returns:
        Tuple[bool, str, str]: (成功标志, Cookie 字符串, 错误信息)
    """
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        # 跟随重定向获取 Cookie
        session = requests.Session()
        response = session.get(
            redirect_url,
            headers=headers,
            verify=False,
            timeout=15,
            allow_redirects=True
        )

        # 收集所有 Cookie
        cookies = session.cookies.get_dict()

        if cookies:
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            return True, cookie_str, ""
        else:
            return False, "", "未获取到 Cookie"

    except Exception as e:
        return False, "", str(e)


def save_cookie_to_env(cookie_str: str) -> Tuple[bool, str]:
    """
    保存 Cookie 到 .env 文件

    Args:
        cookie_str: Cookie 字符串

    Returns:
        Tuple[bool, str]: (成功标志, 错误信息)
    """
    try:
        # 项目根目录
        env_path = Path(__file__).parent.parent / ".env"

        # 读取现有内容
        content = ""
        if env_path.exists():
            content = env_path.read_text(encoding="utf-8")

        # 更新或添加 COOKIE 行
        cookie_line = f'COOKIE="{cookie_str}"'

        if "COOKIE=" in content:
            # 替换现有 COOKIE 行
            content = re.sub(r'COOKIE=.*', cookie_line, content)
        else:
            # 追加新行
            if content and not content.endswith("\n"):
                content += "\n"
            content += cookie_line + "\n"

        env_path.write_text(content, encoding="utf-8")
        return True, ""

    except PermissionError:
        return False, "没有写入权限，请检查文件权限"
    except Exception as e:
        return False, str(e)


def get_cookie_from_env() -> Optional[str]:
    """
    从 .env 文件读取 Cookie

    Returns:
        Optional[str]: Cookie 字符串，不存在则返回 None
    """
    try:
        env_path = Path(__file__).parent.parent / ".env"

        if not env_path.exists():
            return None

        content = env_path.read_text(encoding="utf-8")

        # 匹配 COOKIE= 行
        match = re.search(r'COOKIE=["\']?([^"\'\n]+)["\']?', content)
        if match:
            return match.group(1)

        return None

    except Exception:
        return None
