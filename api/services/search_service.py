"""
搜索服务层
封装对 DouyinAPI 搜索相关方法的调用
"""
import os
import sys
from loguru import logger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from dy_apis.douyin_api import DouyinAPI
from builder.auth import DouyinAuth
from api.schemas.search import (
    SearchWorkItem, SearchWorksResponse,
    SearchUserItem, SearchUsersResponse,
    SearchLiveItem, SearchLivesResponse
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


def _extract_search_work(item: dict) -> SearchWorkItem:
    """从搜索结果中提取作品项"""
    aweme = item.get("aweme_info", {})
    if not aweme:
        return None

    # 提取封面
    cover = ""
    video_data = aweme.get("video", {})
    cover_data = video_data.get("cover", {})
    if cover_data and "url_list" in cover_data:
        cover = cover_data["url_list"][0] if cover_data["url_list"] else ""

    # 提取作者信息
    author = aweme.get("author", {})
    author_avatar = ""
    avatar_thumb = author.get("avatar_thumb", {})
    if avatar_thumb and "url_list" in avatar_thumb:
        author_avatar = avatar_thumb["url_list"][0] if avatar_thumb["url_list"] else ""

    # 提取统计数据
    stats = aweme.get("statistics", {})

    return SearchWorkItem(
        aweme_id=aweme.get("aweme_id", ""),
        desc=aweme.get("desc", ""),
        create_time=aweme.get("create_time", 0),
        cover=cover,
        duration=video_data.get("duration", 0),
        author_nickname=author.get("nickname", ""),
        author_avatar=author_avatar,
        author_sec_uid=author.get("sec_uid", ""),
        digg_count=stats.get("digg_count", 0),
        comment_count=stats.get("comment_count", 0),
        share_count=stats.get("share_count", 0),
        collect_count=stats.get("collect_count", 0)
    )


def _extract_search_user(item: dict) -> SearchUserItem:
    """从搜索结果中提取用户项"""
    user = item.get("user_info", {})
    if not user:
        return None

    # 提取头像
    avatar = ""
    avatar_thumb = user.get("avatar_thumb", {})
    if avatar_thumb and "url_list" in avatar_thumb:
        avatar = avatar_thumb["url_list"][0] if avatar_thumb["url_list"] else ""

    return SearchUserItem(
        uid=user.get("uid", ""),
        sec_uid=user.get("sec_uid", ""),
        nickname=user.get("nickname", ""),
        signature=user.get("signature", ""),
        avatar=avatar,
        follower_count=user.get("follower_count", 0),
        total_favorited=user.get("total_favorited", 0),
        aweme_count=user.get("aweme_count", 0),
        unique_id=user.get("unique_id", ""),
        custom_verify=user.get("custom_verify", "")
    )


def _extract_search_live(item: dict) -> SearchLiveItem:
    """从搜索结果中提取直播项"""
    lives = item.get("lives", {})
    if not lives:
        return None

    # 提取封面
    cover = ""
    cover_data = lives.get("cover", {})
    if cover_data and "url_list" in cover_data:
        cover = cover_data["url_list"][0] if cover_data["url_list"] else ""

    # 提取主播信息
    anchor = lives.get("owner", {})
    anchor_avatar = ""
    avatar_thumb = anchor.get("avatar_thumb", {})
    if avatar_thumb and "url_list" in avatar_thumb:
        anchor_avatar = avatar_thumb["url_list"][0] if avatar_thumb["url_list"] else ""

    return SearchLiveItem(
        room_id=str(lives.get("room_id", "")),
        title=lives.get("title", ""),
        cover=cover,
        user_count=lives.get("user_count", 0),
        anchor_nickname=anchor.get("nickname", ""),
        anchor_avatar=anchor_avatar,
        anchor_sec_uid=anchor.get("sec_uid", "")
    )


def search_works(
    keyword: str,
    offset: str = "0",
    sort_type: str = "0",
    publish_time: str = "0",
    filter_duration: str = "",
    content_type: str = ""
) -> SearchWorksResponse:
    """
    搜索作品

    :param keyword: 搜索关键词
    :param offset: 分页偏移量
    :param sort_type: 排序方式 0综合 1最多点赞 2最新发布
    :param publish_time: 发布时间 0不限 1一天内 7一周内 180半年内
    :param filter_duration: 视频时长 空不限 0-1一分钟内 1-5一到五分钟 5-10000五分钟以上
    :param content_type: 内容形式 空不限 1视频 2图文
    :return: SearchWorksResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.search_general_work(
            auth, keyword,
            sort_type=sort_type,
            publish_time=publish_time,
            offset=offset,
            filter_duration=filter_duration,
            content_type=content_type
        )

        if not result:
            return SearchWorksResponse(success=False, message="搜索失败")

        data_list = result.get("data", [])
        works = []
        for item in data_list:
            work = _extract_search_work(item)
            if work:
                works.append(work)

        return SearchWorksResponse(
            success=True,
            message="搜索成功",
            data=works,
            cursor=str(result.get("cursor", "0")),
            has_more=result.get("has_more", 0) == 1
        )
    except ValueError as e:
        return SearchWorksResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"搜索作品失败: {e}")
        return SearchWorksResponse(success=False, message=f"搜索失败: {str(e)}")


def search_users(
    keyword: str,
    offset: str = "0",
    count: str = "25",
    douyin_user_fans: str = "",
    douyin_user_type: str = ""
) -> SearchUsersResponse:
    """
    搜索用户

    :param keyword: 搜索关键词
    :param offset: 分页偏移量
    :param count: 每页数量
    :param douyin_user_fans: 粉丝数量筛选
    :param douyin_user_type: 用户类型筛选
    :return: SearchUsersResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.search_user(
            auth, keyword,
            offset=offset,
            num=count,
            douyin_user_fans=douyin_user_fans,
            douyin_user_type=douyin_user_type
        )

        if not result:
            return SearchUsersResponse(success=False, message="搜索失败")

        user_list = result.get("user_list", [])
        users = []
        for item in user_list:
            user = _extract_search_user(item)
            if user:
                users.append(user)

        return SearchUsersResponse(
            success=True,
            message="搜索成功",
            data=users,
            cursor=str(result.get("cursor", "0")),
            has_more=result.get("has_more", 0) == 1
        )
    except ValueError as e:
        return SearchUsersResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"搜索用户失败: {e}")
        return SearchUsersResponse(success=False, message=f"搜索失败: {str(e)}")


def search_lives(
    keyword: str,
    offset: str = "0",
    count: str = "25"
) -> SearchLivesResponse:
    """
    搜索直播

    :param keyword: 搜索关键词
    :param offset: 分页偏移量
    :param count: 每页数量
    :return: SearchLivesResponse
    """
    try:
        auth = _get_auth()
        result = DouyinAPI.search_live(auth, keyword, offset=offset, num=count)

        if not result:
            return SearchLivesResponse(success=False, message="搜索失败")

        data_list = result.get("data", [])
        lives = []
        for item in data_list:
            live = _extract_search_live(item)
            if live:
                lives.append(live)

        return SearchLivesResponse(
            success=True,
            message="搜索成功",
            data=lives,
            cursor=str(result.get("cursor", "0")),
            has_more=result.get("has_more", 0) == 1
        )
    except ValueError as e:
        return SearchLivesResponse(success=False, message=str(e))
    except Exception as e:
        logger.error(f"搜索直播失败: {e}")
        return SearchLivesResponse(success=False, message=f"搜索失败: {str(e)}")
