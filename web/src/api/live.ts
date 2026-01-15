/**
 * 直播 API 调用模块
 */
import axios from 'axios'
import type {
  LiveInfoResponse,
  ProductListResponse,
  AllProductsResponse,
  ProductDetailResponse
} from '../types/live'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000
})

/**
 * 获取直播间信息
 */
export async function getLiveInfo(url: string): Promise<LiveInfoResponse> {
  const response = await api.get<LiveInfoResponse>('/live/info', {
    params: { url }
  })
  return response.data
}

/**
 * 获取直播商品列表
 */
export async function getLiveProducts(
  url: string,
  roomId: string,
  authorId: string,
  offset: string = '0'
): Promise<ProductListResponse> {
  const response = await api.get<ProductListResponse>('/live/products', {
    params: {
      url,
      room_id: roomId,
      author_id: authorId,
      offset
    }
  })
  return response.data
}

/**
 * 获取全部直播商品
 */
export async function getAllLiveProducts(
  url: string,
  roomId: string,
  authorId: string
): Promise<AllProductsResponse> {
  const response = await api.get<AllProductsResponse>('/live/products/all', {
    params: {
      url,
      room_id: roomId,
      author_id: authorId
    }
  })
  return response.data
}

/**
 * 获取商品详情
 */
export async function getProductDetail(
  url: string,
  promotionId: string,
  secAuthorId: string,
  roomId: string
): Promise<ProductDetailResponse> {
  const response = await api.get<ProductDetailResponse>('/live/product/detail', {
    params: {
      url,
      promotion_id: promotionId,
      sec_author_id: secAuthorId,
      room_id: roomId
    }
  })
  return response.data
}
