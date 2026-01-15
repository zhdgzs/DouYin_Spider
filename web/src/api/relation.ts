/**
 * 关系 API 调用模块
 */
import axios from 'axios'
import type {
  FollowerListResponse,
  FollowingListResponse,
  NoticeListResponse
} from '../types/relation'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

/**
 * 获取粉丝列表
 */
export async function getFollowerList(
  userId: string,
  secUid: string,
  maxTime: string = '0',
  count: string = '20'
): Promise<FollowerListResponse> {
  const response = await api.get<FollowerListResponse>('/relation/followers', {
    params: {
      user_id: userId,
      sec_uid: secUid,
      max_time: maxTime,
      count
    }
  })
  return response.data
}

/**
 * 获取关注列表
 */
export async function getFollowingList(
  userId: string,
  secUid: string,
  maxTime: string = '0',
  count: string = '20'
): Promise<FollowingListResponse> {
  const response = await api.get<FollowingListResponse>('/relation/following', {
    params: {
      user_id: userId,
      sec_uid: secUid,
      max_time: maxTime,
      count
    }
  })
  return response.data
}

/**
 * 获取通知列表
 */
export async function getNoticeList(
  maxTime: string = '0',
  count: string = '20',
  noticeGroup: string = '700'
): Promise<NoticeListResponse> {
  const response = await api.get<NoticeListResponse>('/relation/notices', {
    params: {
      max_time: maxTime,
      count,
      notice_group: noticeGroup
    }
  })
  return response.data
}
