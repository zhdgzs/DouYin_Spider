/**
 * 搜索 API 调用模块
 */
import axios from 'axios'
import type {
  SearchWorksResponse,
  SearchUsersResponse,
  SearchLivesResponse
} from '../types/search'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

/**
 * 搜索作品
 */
export async function searchWorks(
  keyword: string,
  offset: string = '0',
  sortType: string = '0',
  publishTime: string = '0',
  filterDuration: string = '',
  contentType: string = ''
): Promise<SearchWorksResponse> {
  const response = await api.get<SearchWorksResponse>('/search/works', {
    params: {
      keyword,
      offset,
      sort_type: sortType,
      publish_time: publishTime,
      filter_duration: filterDuration,
      content_type: contentType
    }
  })
  return response.data
}

/**
 * 搜索用户
 */
export async function searchUsers(
  keyword: string,
  offset: string = '0',
  count: string = '25',
  douyinUserFans: string = '',
  douyinUserType: string = ''
): Promise<SearchUsersResponse> {
  const response = await api.get<SearchUsersResponse>('/search/users', {
    params: {
      keyword,
      offset,
      count,
      douyin_user_fans: douyinUserFans,
      douyin_user_type: douyinUserType
    }
  })
  return response.data
}

/**
 * 搜索直播
 */
export async function searchLives(
  keyword: string,
  offset: string = '0',
  count: string = '25'
): Promise<SearchLivesResponse> {
  const response = await api.get<SearchLivesResponse>('/search/lives', {
    params: { keyword, offset, count }
  })
  return response.data
}
