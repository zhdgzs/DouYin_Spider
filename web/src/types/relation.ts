/**
 * 关系相关类型定义
 */

export interface RelationUser {
  uid: string
  sec_uid: string
  nickname: string
  signature: string
  avatar: string
  follower_count: number
  following_count: number
  aweme_count: number
  unique_id: string
  is_following: boolean
}

export interface NoticeItem {
  notice_id: string
  notice_type: number
  content: string
  create_time: number
  from_user_nickname: string
  from_user_avatar: string
  from_user_sec_uid: string
  aweme_id: string
  aweme_cover: string
}

export interface FollowerListResponse {
  success: boolean
  message: string
  data: RelationUser[]
  max_time: string
  has_more: boolean
  total: number
}

export interface FollowingListResponse {
  success: boolean
  message: string
  data: RelationUser[]
  max_time: string
  has_more: boolean
  total: number
}

export interface NoticeListResponse {
  success: boolean
  message: string
  data: NoticeItem[]
  max_time: string
  has_more: boolean
}
