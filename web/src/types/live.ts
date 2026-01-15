/**
 * 直播相关类型定义
 */

export interface LiveInfo {
  room_id: string
  user_id: string
  room_status: string
  room_title: string
  is_living: boolean
}

export interface ProductItem {
  promotion_id: string
  product_id: string
  title: string
  cover: string
  price: number
  market_price: number
  sales: number
  in_stock: boolean
}

export interface ProductDetail {
  promotion_id: string
  product_id: string
  title: string
  cover: string
  images: string[]
  price: number
  market_price: number
  sales: number
  description: string
  shop_name: string
}

export interface LiveInfoResponse {
  success: boolean
  message: string
  data: LiveInfo | null
}

export interface ProductListResponse {
  success: boolean
  message: string
  data: ProductItem[]
  offset: string
  has_more: boolean
  total: number
}

export interface AllProductsResponse {
  success: boolean
  message: string
  data: ProductItem[]
  total: number
}

export interface ProductDetailResponse {
  success: boolean
  message: string
  data: ProductDetail | null
}
