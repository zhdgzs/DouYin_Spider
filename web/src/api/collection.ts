/**
 * 收藏 API 调用模块
 */
import axios from 'axios'
import type { CollectionListResponse, CollectResponse } from '../types/collection'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

/**
 * 获取收藏夹列表
 */
export async function getCollectionList(): Promise<CollectionListResponse> {
  const response = await api.get<CollectionListResponse>('/collection/list')
  return response.data
}

/**
 * 收藏作品
 */
export async function collectAweme(
  awemeId: string,
  action: string = '1'
): Promise<CollectResponse> {
  const response = await api.post<CollectResponse>('/collection/add', {
    aweme_id: awemeId,
    action
  })
  return response.data
}

/**
 * 移动收藏
 */
export async function moveCollectAweme(
  awemeId: string,
  collectName: string,
  collectId: string
): Promise<CollectResponse> {
  const response = await api.post<CollectResponse>('/collection/move', {
    aweme_id: awemeId,
    collect_name: collectName,
    collect_id: collectId
  })
  return response.data
}

/**
 * 移除收藏
 */
export async function removeCollectAweme(
  awemeId: string,
  collectName: string,
  collectId: string
): Promise<CollectResponse> {
  const response = await api.delete<CollectResponse>('/collection/remove', {
    params: {
      aweme_id: awemeId,
      collect_name: collectName,
      collect_id: collectId
    }
  })
  return response.data
}
