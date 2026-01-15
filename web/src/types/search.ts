/**
 * 搜索相关类型定义
 */

export interface SearchWorkItem {
  aweme_id: string
  desc: string
  create_time: number
  cover: string
  duration: number
  author_nickname: string
  author_avatar: string
  author_sec_uid: string
  digg_count: number
  comment_count: number
  share_count: number
  collect_count: number
}

export interface SearchUserItem {
  uid: string
  sec_uid: string
  nickname: string
  signature: string
  avatar: string
  follower_count: number
  total_favorited: number
  aweme_count: number
  unique_id: string
  custom_verify: string
}

export interface SearchLiveItem {
  room_id: string
  title: string
  cover: string
  user_count: number
  anchor_nickname: string
  anchor_avatar: string
  anchor_sec_uid: string
}

export interface SearchWorksResponse {
  success: boolean
  message: string
  data: SearchWorkItem[]
  cursor: string
  has_more: boolean
}

export interface SearchUsersResponse {
  success: boolean
  message: string
  data: SearchUserItem[]
  cursor: string
  has_more: boolean
}

export interface SearchLivesResponse {
  success: boolean
  message: string
  data: SearchLiveItem[]
  cursor: string
  has_more: boolean
}
