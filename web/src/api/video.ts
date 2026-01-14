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
 * 获取视频代理 URL（用于预览播放）
 */
export function getProxyUrl(originalUrl: string): string {
  return `/api/video/proxy?url=${encodeURIComponent(originalUrl)}`
}

/**
 * 获取视频下载 URL（用于下载）
 */
export function getDownloadUrl(originalUrl: string, filename?: string): string {
  const params = new URLSearchParams({ url: originalUrl })
  if (filename) {
    params.append('filename', filename)
  }
  return `/api/video/download?${params.toString()}`
}

/**
 * 健康检查
 */
export async function healthCheck(): Promise<{ status: string; version: string }> {
  const response = await api.get('/health')
  return response.data
}
