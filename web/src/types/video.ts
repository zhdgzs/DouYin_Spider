/**
 * 视频相关类型定义
 */

// 作者信息
export interface AuthorInfo {
  nickname: string
  avatar: string
  sec_uid: string
}

// 统计数据
export interface Statistics {
  digg_count: number
  comment_count: number
  share_count: number
  collect_count: number
}

// 视频清晰度信息
export interface VideoQuality {
  quality: string
  gear_name: string
  width: number
  height: number
  file_size: number
  file_size_str: string
  url: string
}

// 视频详细信息
export interface VideoInfo {
  video_id: string
  title: string
  desc: string
  author: AuthorInfo
  statistics: Statistics
  cover: string
  duration: number
  create_time: number
  video_urls: VideoQuality[]
}

// 视频解析响应
export interface VideoParseResponse {
  success: boolean
  message: string
  data: VideoInfo | null
}

// 视频解析请求
export interface VideoParseRequest {
  url: string
}
