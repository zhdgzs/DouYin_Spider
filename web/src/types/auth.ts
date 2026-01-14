/**
 * 认证相关类型定义
 */

// 用户信息
export interface UserInfo {
  uid: string
  nickname: string
  avatar: string
}

// 认证状态
export interface AuthStatus {
  valid: boolean
  user_info: UserInfo | null
  error: string | null
}

// 二维码数据
export interface QRCodeData {
  token: string
  qrcode_url: string
  qrcode_base64: string
  expire_at: number
}

// 二维码响应
export interface QRCodeResponse {
  success: boolean
  data: QRCodeData | null
  error: string | null
}

// 扫码状态
export interface QRCodeStatusResponse {
  status: QRCodeStatusCode
  message: string
}

// 扫码状态码
export enum QRCodeStatusCode {
  WAITING = 1,      // 等待扫码
  SCANNED = 2,      // 已扫码，等待确认
  CONFIRMED = 3,    // 确认登录
  RATE_LIMITED = 4, // 访问频繁
  EXPIRED = 5       // 二维码过期
}
