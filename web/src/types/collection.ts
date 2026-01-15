/**
 * 收藏相关类型定义
 */

export interface CollectionFolder {
  collect_id: string
  name: string
  cover: string
  video_count: number
  create_time: number
}

export interface CollectionListResponse {
  success: boolean
  message: string
  data: CollectionFolder[]
}

export interface CollectResponse {
  success: boolean
  message: string
}
