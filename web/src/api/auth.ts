/**
 * 认证 API 调用模块
 */
import axios from 'axios'
import type { AuthStatus, QRCodeResponse, QRCodeStatusResponse } from '../types/auth'

const api = axios.create({
  baseURL: '/api/auth',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 检测认证状态
 */
export async function checkAuth(): Promise<AuthStatus> {
  const response = await api.get<AuthStatus>('/check')
  return response.data
}

/**
 * 获取登录二维码
 */
export async function getQRCode(): Promise<QRCodeResponse> {
  const response = await api.get<QRCodeResponse>('/qrcode')
  return response.data
}

/**
 * 检查扫码状态
 */
export async function checkQRCodeStatus(token: string): Promise<QRCodeStatusResponse> {
  const response = await api.get<QRCodeStatusResponse>('/qrcode/status', {
    params: { token }
  })
  return response.data
}

/**
 * 获取当前保存的 Cookie
 */
export async function getCookie(): Promise<{
  success: boolean
  cookie: string | null
  raw_cookie: string | null
  length?: number
  error?: string
}> {
  const response = await api.get('/cookie')
  return response.data
}

/**
 * 手动设置 Cookie
 */
export async function setCookie(cookie: string): Promise<{
  success: boolean
  message?: string
  error?: string
  warning?: string
  user_info?: {
    uid: string
    nickname: string
    avatar: string
  }
}> {
  const response = await api.post('/cookie', { cookie })
  return response.data
}
