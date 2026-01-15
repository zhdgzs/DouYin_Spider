/**
 * 评论 API 调用模块
 */
import axios from 'axios'
import type {
  CommentListResponse,
  CommentRepliesResponse,
  AllCommentsResponse
} from '../types/comment'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000
})

/**
 * 获取一级评论列表
 */
export async function getCommentList(
  url: string,
  cursor: string = '0'
): Promise<CommentListResponse> {
  const response = await api.get<CommentListResponse>('/comment/list', {
    params: { url, cursor }
  })
  return response.data
}

/**
 * 获取二级评论（回复）
 */
export async function getCommentReplies(
  awemeId: string,
  commentId: string,
  cursor: string = '0',
  count: string = '20'
): Promise<CommentRepliesResponse> {
  const response = await api.get<CommentRepliesResponse>('/comment/replies', {
    params: {
      aweme_id: awemeId,
      comment_id: commentId,
      cursor,
      count
    }
  })
  return response.data
}

/**
 * 获取全部评论
 */
export async function getAllComments(url: string): Promise<AllCommentsResponse> {
  const response = await api.get<AllCommentsResponse>('/comment/all', {
    params: { url }
  })
  return response.data
}
