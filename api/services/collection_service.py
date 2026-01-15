"""
收藏服务层
封装对 DouyinAPI 收藏相关方法的调用
"""
import os
import sys
from loguru import logger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dy_apis.douyin_api import DouyinAPI
from builder.auth import DouyinAuth
from api.schemas.collection import (
    CollectionFolder, CollectionListResponse, CollectResponse
)


def _get_auth() -> DouyinAuth:
    """获取认证对象"""
    from dotenv import load_dotenv
    load_dotenv()

    cookie_str = os.getenv("COOKIE", "")
    if not cookie_str:
        raise ValueError("未配置 Cookie，请在 .env 文件中设置 COOKIE 环境变量")

    auth = DouyinAuth()
    auth.perepare_auth(cookie_str)
    return auth


def _extract_collection_folder(item: dict) -> CollectionFolder:
    """提取收藏夹信息"""
    # 提取封面
    cover = ""
    cover_data = item.get("cover", {})
    if cover_data and "url_list" in cover_data:
        cover = cover_data["url_list"][0] if cover_data["url_list"] else ""

    return CollectionFolder(
        collect_id=str(item.get("collects_id", "")),
        name=item.get("collects_name", ""),
        cover=cover,
        video_count=item.get("video_count", 0),
        create_time=item.get("create_time", 0)
    )


def get_collection_list() -> CollectionListResponse:
    """
    获取收藏夹列表

    :return: CollectionListResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_collect_list(auth)

        if not result:
            return CollectionListResponse(success=False, message="获取收藏夹列表失败")

        collects_list = result.get("collects_list", [])
        folders = [_extract_collection_folder(c) for c in collects_list]

        return CollectionListResponse(
            success=True,
            message="获取成功",
            data=folders
        )
    except ValueError as e:
        return CollectionListResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取收藏夹列表失败: {e}")
        return CollectionListResponse(success=False, message=f"获取失败: {str(e)}")


def collect_aweme(aweme_id: str, action: str = "1") -> CollectResponse:
    """
    收藏或取消收藏作品

    :param aweme_id: 作品ID
    :param action: 1收藏 0取消收藏
    :return: CollectResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.collect_aweme(auth, aweme_id, action)

        if not result:
            return CollectResponse(success=False, message="操作失败")

        status_code = result.get("status_code", -1)
        if status_code == 0:
            action_text = "收藏" if action == "1" else "取消收藏"
            return CollectResponse(success=True, message=f"{action_text}成功")
        else:
            return CollectResponse(
                success=False,
                message=result.get("status_msg", "操作失败")
            )
    except ValueError as e:
        return CollectResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"收藏操作失败: {e}")
        return CollectResponse(success=False, message=f"操作失败: {str(e)}")


def move_collect_aweme(
    aweme_id: str,
    collect_name: str,
    collect_id: str
) -> CollectResponse:
    """
    移动作品到指定收藏夹

    :param aweme_id: 作品ID
    :param collect_name: 目标收藏夹名称
    :param collect_id: 目标收藏夹ID
    :return: CollectResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.move_collect_aweme(auth, aweme_id, collect_name, collect_id)

        if not result:
            return CollectResponse(success=False, message="移动失败")

        status_code = result.get("status_code", -1)
        if status_code == 0:
            return CollectResponse(success=True, message="移动成功")
        else:
            return CollectResponse(
                success=False,
                message=result.get("status_msg", "移动失败")
            )
    except ValueError as e:
        return CollectResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"移动收藏失败: {e}")
        return CollectResponse(success=False, message=f"移动失败: {str(e)}")


def remove_collect_aweme(
    aweme_id: str,
    collect_name: str,
    collect_id: str
) -> CollectResponse:
    """
    从收藏夹移除作品

    :param aweme_id: 作品ID
    :param collect_name: 收藏夹名称
    :param collect_id: 收藏夹ID
    :return: CollectResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.remove_collect_aweme(auth, aweme_id, collect_name, collect_id)

        if not result:
            return CollectResponse(success=False, message="移除失败")

        status_code = result.get("status_code", -1)
        if status_code == 0:
            return CollectResponse(success=True, message="移除成功")
        else:
            return CollectResponse(
                success=False,
                message=result.get("status_msg", "移除失败")
            )
    except ValueError as e:
        return CollectResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"移除收藏失败: {e}")
        return CollectResponse(success=False, message=f"移除失败: {str(e)}")
