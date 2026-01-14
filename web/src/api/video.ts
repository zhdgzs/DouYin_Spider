/**
 * 视频 API 调用模块
 */
import axios from 'axios'
import type { VideoParseResponse } from '../types/video'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000, // 60秒超时
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 解析视频链接
 */
export async function parseVideo(url: string): Promise<VideoParseResponse> {
  const response = await api.post<VideoParseResponse>('/video/parse', { url })
  return response.data
}

/**
 * 获取视频代理 URL
 */
export function getProxyUrl(originalUrl: string): string {
  return `/api/video/proxy?url=${encodeURIComponent(originalUrl)}`
}

/**
 * 健康检查
 */
export async function healthCheck(): Promise<{ status: string; version: string }> {
  const response = await api.get('/health')
  return response.data
}
