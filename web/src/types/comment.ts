/**
 * 评论相关类型定义
 */

export interface CommentUser {
  uid: string
  sec_uid: string
  nickname: string
  avatar: string
}

export interface CommentItem {
  cid: string
  aweme_id: string
  text: string
  create_time: number
  digg_count: number
  reply_comment_total: number
  user: CommentUser
  ip_label: string
}

export interface CommentWithReplies extends CommentItem {
  replies: CommentItem[]
}

export interface CommentListResponse {
  success: boolean
  message: string
  data: CommentItem[]
  cursor: string
  has_more: boolean
  total: number
}

export interface CommentRepliesResponse {
  success: boolean
  message: string
  data: CommentItem[]
  cursor: string
  has_more: boolean
}

export interface AllCommentsResponse {
  success: boolean
  message: string
  data: CommentWithReplies[]
  total: number
}
