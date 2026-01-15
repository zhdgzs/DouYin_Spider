/**
 * 用户 API 调用模块
 */
import axios from 'axios'
import type {
  UserInfoResponse,
  UserWorksResponse,
  UserAllWorksResponse
} from '../types/user'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000
})

/**
 * 获取用户信息
 */
export async function getUserInfo(url: string): Promise<UserInfoResponse> {
  const response = await api.get<UserInfoResponse>('/user/info', {
    params: { url }
  })
  return response.data
}

/**
 * 获取用户作品列表（分页）
 */
export async function getUserWorks(
  url: string,
  maxCursor: string = '0'
): Promise<UserWorksResponse> {
  const response = await api.get<UserWorksResponse>('/user/works', {
    params: { url, max_cursor: maxCursor }
  })
  return response.data
}

/**
 * 获取用户全部作品
 */
export async function getUserAllWorks(url: string): Promise<UserAllWorksResponse> {
  const response = await api.get<UserAllWorksResponse>('/user/works/all', {
    params: { url }
  })
  return response.data
}
