"""
关系服务层
封装对 DouyinAPI 关系相关方法的调用
"""
import os
import sys
from loguru import logger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dy_apis.douyin_api import DouyinAPI
from builder.auth import DouyinAuth
from api.schemas.relation import (
    RelationUser, FollowerListResponse, FollowingListResponse,
    NoticeItem, NoticeListResponse
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


def _extract_relation_user(user_data: dict) -> RelationUser:
    """提取关系用户信息"""
    # 提取头像
    avatar = ""
    avatar_thumb = user_data.get("avatar_thumb", {})
    if avatar_thumb and "url_list" in avatar_thumb:
        avatar = avatar_thumb["url_list"][0] if avatar_thumb["url_list"] else ""

    return RelationUser(
        uid=user_data.get("uid", ""),
        sec_uid=user_data.get("sec_uid", ""),
        nickname=user_data.get("nickname", ""),
        signature=user_data.get("signature", ""),
        avatar=avatar,
        follower_count=user_data.get("follower_count", 0),
        following_count=user_data.get("following_count", 0),
        aweme_count=user_data.get("aweme_count", 0),
        unique_id=user_data.get("unique_id", ""),
        is_following=user_data.get("follow_status", 0) == 1
    )


def _extract_notice_item(notice: dict) -> NoticeItem:
    """提取通知项"""
    # 提取来源用户信息
    from_user = notice.get("from_user", {})
    from_user_avatar = ""
    avatar_thumb = from_user.get("avatar_thumb", {})
    if avatar_thumb and "url_list" in avatar_thumb:
        from_user_avatar = avatar_thumb["url_list"][0] if avatar_thumb["url_list"] else ""

    # 提取作品封面
    aweme_cover = ""
    aweme = notice.get("aweme", {})
    if aweme:
        video = aweme.get("video", {})
        cover = video.get("cover", {})
        if cover and "url_list" in cover:
            aweme_cover = cover["url_list"][0] if cover["url_list"] else ""

    return NoticeItem(
        notice_id=str(notice.get("notice_id", "")),
        notice_type=notice.get("notice_type", 0),
        content=notice.get("content", ""),
        create_time=notice.get("create_time", 0),
        from_user_nickname=from_user.get("nickname", ""),
        from_user_avatar=from_user_avatar,
        from_user_sec_uid=from_user.get("sec_uid", ""),
        aweme_id=aweme.get("aweme_id", "") if aweme else "",
        aweme_cover=aweme_cover
    )


def get_follower_list(
    user_id: str,
    sec_uid: str,
    max_time: str = "0",
    count: str = "20"
) -> FollowerListResponse:
    """
    获取粉丝列表

    :param user_id: 用户ID
    :param sec_uid: 用户安全ID
    :param max_time: 分页时间戳
    :param count: 每页数量
    :return: FollowerListResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_user_follower_list(
            auth, user_id, sec_uid, max_time=max_time, count=count
        )

        if not result:
            return FollowerListResponse(success=False, message="获取粉丝列表失败")

        followers_data = result.get("followers", [])
        followers = [_extract_relation_user(u) for u in followers_data]

        return FollowerListResponse(
            success=True,
            message="获取成功",
            data=followers,
            max_time=str(result.get("max_time", "0")),
            has_more=result.get("has_more", False),
            total=result.get("total", 0)
        )
    except ValueError as e:
        return FollowerListResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取粉丝列表失败: {e}")
        return FollowerListResponse(success=False, message=f"获取失败: {str(e)}")


def get_following_list(
    user_id: str,
    sec_uid: str,
    max_time: str = "0",
    count: str = "20"
) -> FollowingListResponse:
    """
    获取关注列表

    :param user_id: 用户ID
    :param sec_uid: 用户安全ID
    :param max_time: 分页时间戳
    :param count: 每页数量
    :return: FollowingListResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_user_following_list(
            auth, user_id, sec_uid, max_time=max_time, count=count
        )

        if not result:
            return FollowingListResponse(success=False, message="获取关注列表失败")

        followings_data = result.get("followings", [])
        followings = [_extract_relation_user(u) for u in followings_data]

        return FollowingListResponse(
            success=True,
            message="获取成功",
            data=followings,
            max_time=str(result.get("max_time", "0")),
            has_more=result.get("has_more", False),
            total=result.get("total", 0)
        )
    except ValueError as e:
        return FollowingListResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取关注列表失败: {e}")
        return FollowingListResponse(success=False, message=f"获取失败: {str(e)}")


def get_notice_list(
    max_time: str = "0",
    count: str = "20",
    notice_group: str = "700"
) -> NoticeListResponse:
    """
    获取通知列表

    :param max_time: 分页时间戳
    :param count: 每页数量
    :param notice_group: 消息类型 700全部 401粉丝 601@我的 2评论 3点赞 520弹幕
    :return: NoticeListResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_notice_list(
            auth, max_time=max_time, count=count, notice_group=notice_group
        )

        if not result:
            return NoticeListResponse(success=False, message="获取通知列表失败")

        notices_data = result.get("notice_list", [])
        notices = [_extract_notice_item(n) for n in notices_data]

        return NoticeListResponse(
            success=True,
            message="获取成功",
            data=notices,
            max_time=str(result.get("max_time", "0")),
            has_more=result.get("has_more", False)
        )
    except ValueError as e:
        return NoticeListResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取通知列表失败: {e}")
        return NoticeListResponse(success=False, message=f"获取失败: {str(e)}")
