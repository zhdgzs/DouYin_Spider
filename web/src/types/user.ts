/**
 * 用户相关类型定义
 */

export interface UserInfo {
  uid: string
  sec_uid: string
  nickname: string
  signature: string
  avatar: string
  avatar_larger: string
  follower_count: number
  following_count: number
  total_favorited: number
  aweme_count: number
  favoriting_count: number
  unique_id: string
  short_id: string
  is_verified: boolean
  verification_type: number
  custom_verify: string
  enterprise_verify_reason: string
  ip_location: string
}

export interface WorkItem {
  aweme_id: string
  desc: string
  create_time: number
  cover: string
  duration: number
  digg_count: number
  comment_count: number
  share_count: number
  collect_count: number
  play_count: number
}

export interface UserInfoResponse {
  success: boolean
  message: string
  data: UserInfo | null
}

export interface UserWorksResponse {
  success: boolean
  message: string
  data: WorkItem[]
  max_cursor: string
  has_more: boolean
}

export interface UserAllWorksResponse {
  success: boolean
  message: string
  data: WorkItem[]
  total: number
}
