# Spec: Live Feature API

## Overview

提供直播间信息和直播商品相关 API。

## ADDED Requirements

### Requirement: Live Info API

系统 SHALL 提供获取直播间基本信息的 API 端点。

#### Scenario: 获取直播间信息

**Given** 用户提供直播间链接或 room_id
**When** 调用 `GET /api/live/info?live_id={id}`
**Then** 返回直播间信息，包括：
- `room_id`: 直播间 ID
- `title`: 直播标题
- `cover`: 封面图
- `user`: 主播信息
- `user_count`: 在线人数
- `status`: 直播状态

---

### Requirement: Live Products API

系统 SHALL 提供获取直播间商品列表的 API 端点。

#### Scenario: 获取直播商品列表（分页）

**Given** 用户提供直播间 ID
**When** 调用 `GET /api/live/products?room_id={id}&cursor={cursor}&count={count}`
**Then** 返回商品列表

#### Scenario: 获取全部直播商品

**Given** 用户提供直播间 ID
**When** 调用 `GET /api/live/products/all?room_id={id}`
**Then** 返回该直播间的全部商品

---

### Requirement: Product Detail API

系统 SHALL 提供获取商品详情的 API 端点。

#### Scenario: 获取商品详情

**Given** 用户提供商品 ID
**When** 调用 `GET /api/live/product/detail?product_id={id}`
**Then** 返回商品详细信息，包括：
- 商品名称
- 价格
- 原价
- 销量
- 商品图片
- 商品描述

---

## API Schema

### Request

```
GET /api/live/info
Query Parameters:
  - live_id: string (required) - 直播间 ID 或链接

GET /api/live/products
Query Parameters:
  - room_id: string (required) - 直播间 ID
  - cursor: int (optional, default: 0) - 分页游标
  - count: int (optional, default: 20) - 每页数量

GET /api/live/products/all
Query Parameters:
  - room_id: string (required) - 直播间 ID

GET /api/live/product/detail
Query Parameters:
  - product_id: string (required) - 商品 ID
  - room_id: string (required) - 直播间 ID
```

### Response

```json
// Live Info Response
{
  "success": true,
  "data": {
    "room_id": "123456",
    "title": "直播标题",
    "cover": "https://...",
    "user": {
      "uid": "...",
      "nickname": "主播昵称",
      "avatar": "..."
    },
    "user_count": 10000,
    "status": 2
  }
}

// Products List Response
{
  "success": true,
  "data": {
    "products": [
      {
        "product_id": "...",
        "title": "商品名称",
        "price": 99.00,
        "origin_price": 199.00,
        "cover": "...",
        "sales": 1000
      }
    ],
    "has_more": true,
    "cursor": 1234567890
  }
}

// Product Detail Response
{
  "success": true,
  "data": {
    "product_id": "...",
    "title": "商品名称",
    "price": 99.00,
    "origin_price": 199.00,
    "images": ["...", "..."],
    "description": "商品描述",
    "sales": 1000,
    "shop": {
      "name": "店铺名称",
      "logo": "..."
    }
  }
}
```

## Related Capabilities

- `search-feature`: 搜索直播
