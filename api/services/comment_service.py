"""
评论服务层
封装对 DouyinAPI 评论相关方法的调用
"""
import os
import sys
from loguru import logger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dy_apis.douyin_api import DouyinAPI
from builder.auth import DouyinAuth
from api.schemas.comment import (
    CommentUser, CommentItem, CommentWithReplies,
    CommentListResponse, CommentRepliesResponse, AllCommentsResponse
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


def _extract_comment_user(user_data: dict) -> CommentUser:
    """提取评论用户信息"""
    avatar = ""
    avatar_thumb = user_data.get("avatar_thumb", {})
    if avatar_thumb and "url_list" in avatar_thumb:
        avatar = avatar_thumb["url_list"][0] if avatar_thumb["url_list"] else ""

    return CommentUser(
        uid=user_data.get("uid", ""),
        sec_uid=user_data.get("sec_uid", ""),
        nickname=user_data.get("nickname", ""),
        avatar=avatar
    )


def _extract_comment_item(comment: dict) -> CommentItem:
    """提取评论项"""
    user_data = comment.get("user", {})
    user = _extract_comment_user(user_data)

    return CommentItem(
        cid=comment.get("cid", ""),
        aweme_id=comment.get("aweme_id", ""),
        text=comment.get("text", ""),
        create_time=comment.get("create_time", 0),
        digg_count=comment.get("digg_count", 0),
        reply_comment_total=comment.get("reply_comment_total", 0),
        user=user,
        ip_label=comment.get("ip_label", "")
    )


def _extract_comment_with_replies(comment: dict) -> CommentWithReplies:
    """提取带回复的评论项"""
    user_data = comment.get("user", {})
    user = _extract_comment_user(user_data)

    # 提取回复列表
    replies = []
    reply_list = comment.get("reply_comment", [])
    for reply in reply_list:
        replies.append(_extract_comment_item(reply))

    return CommentWithReplies(
        cid=comment.get("cid", ""),
        aweme_id=comment.get("aweme_id", ""),
        text=comment.get("text", ""),
        create_time=comment.get("create_time", 0),
        digg_count=comment.get("digg_count", 0),
        reply_comment_total=comment.get("reply_comment_total", 0),
        user=user,
        ip_label=comment.get("ip_label", ""),
        replies=replies
    )


def get_comment_list(url: str, cursor: str = "0") -> CommentListResponse:
    """
    获取一级评论列表

    :param url: 作品链接
    :param cursor: 分页游标
    :return: CommentListResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_work_out_comment(auth, url, cursor=cursor)

        if not result:
            return CommentListResponse(success=False, message="获取评论失败")

        comments_data = result.get("comments", [])
        comments = [_extract_comment_item(c) for c in comments_data]

        return CommentListResponse(
            success=True,
            message="获取成功",
            data=comments,
            cursor=str(result.get("cursor", "0")),
            has_more=result.get("has_more", 0) == 1,
            total=result.get("total", 0)
        )
    except ValueError as e:
        return CommentListResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取评论列表失败: {e}")
        return CommentListResponse(success=False, message=f"获取失败: {str(e)}")


def get_comment_replies(
    aweme_id: str,
    comment_id: str,
    cursor: str = "0",
    count: str = "20"
) -> CommentRepliesResponse:
    """
    获取二级评论（回复）

    :param aweme_id: 作品ID
    :param comment_id: 一级评论ID
    :param cursor: 分页游标
    :param count: 每页数量
    :return: CommentRepliesResponse
    """
    try:
        auth = _get_auth()

        # 构造评论对象供 API 使用
        comment = {
            "aweme_id": aweme_id,
            "cid": comment_id
        }

        result = DouyinAPI.get_work_inner_comment(auth, comment, cursor=cursor, count=count)

        if not result:
            return CommentRepliesResponse(success=False, message="获取回复失败")

        comments_data = result.get("comments", [])
        replies = [_extract_comment_item(c) for c in comments_data]

        return CommentRepliesResponse(
            success=True,
            message="获取成功",
            data=replies,
            cursor=str(result.get("cursor", "0")),
            has_more=result.get("has_more", 0) == 1
        )
    except ValueError as e:
        return CommentRepliesResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取评论回复失败: {e}")
        return CommentRepliesResponse(success=False, message=f"获取失败: {str(e)}")


def get_all_comments(url: str) -> AllCommentsResponse:
    """
    获取全部评论（包含回复）

    :param url: 作品链接
    :return: AllCommentsResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.get_work_all_comment(auth, url)

        if not result:
            return AllCommentsResponse(
                success=True,
                message="该作品暂无评论",
                data=[],
                total=0
            )

        comments = [_extract_comment_with_replies(c) for c in result]

        return AllCommentsResponse(
            success=True,
            message="获取成功",
            data=comments,
            total=len(comments)
        )
    except ValueError as e:
        return AllCommentsResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"获取全部评论失败: {e}")
        return AllCommentsResponse(success=False, message=f"获取失败: {str(e)}")
