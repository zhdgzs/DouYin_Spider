# Spec: User Management API

## Overview

用户信息获取和作品列表 API 规格。

## ADDED Requirements

### Requirement: User Info API

系统 SHALL 提供获取抖音用户基本信息的 API 端点。

#### Scenario: 通过用户链接获取用户信息

**Given** 用户提供有效的抖音用户主页链接
**When** 调用 `GET /api/user/info?url={user_url}`
**Then** 返回用户基本信息，包括：
- `uid`: 用户 ID
- `sec_uid`: 安全用户 ID
- `nickname`: 昵称
- `signature`: 签名
- `avatar`: 头像 URL
- `follower_count`: 粉丝数
- `following_count`: 关注数
- `aweme_count`: 作品数
- `favoriting_count`: 喜欢数

#### Scenario: 用户链接无效

**Given** 用户提供无效的链接
**When** 调用 `GET /api/user/info?url={invalid_url}`
**Then** 返回错误响应 `{ success: false, message: "无效的用户链接" }`

---

### Requirement: User Works List API

系统 SHALL 提供获取用户作品列表的 API 端点，支持分页。

#### Scenario: 获取用户作品列表（分页）

**Given** 用户提供有效的用户链接
**When** 调用 `GET /api/user/works?url={user_url}&cursor={cursor}&count={count}`
**Then** 返回作品列表，包括：
- `works`: 作品数组
- `has_more`: 是否有更多
- `cursor`: 下一页游标

#### Scenario: 获取用户全部作品

**Given** 用户提供有效的用户链接
**When** 调用 `GET /api/user/works/all?url={user_url}`
**Then** 返回该用户的全部作品列表

---

## API Schema

### Request

```
GET /api/user/info
Query Parameters:
  - url: string (required) - 用户主页链接

GET /api/user/works
Query Parameters:
  - url: string (required) - 用户主页链接
  - cursor: int (optional, default: 0) - 分页游标
  - count: int (optional, default: 20) - 每页数量

GET /api/user/works/all
Query Parameters:
  - url: string (required) - 用户主页链接
```

### Response

```json
// User Info Response
{
  "success": true,
  "data": {
    "uid": "123456",
    "sec_uid": "MS4wLjAB...",
    "nickname": "用户昵称",
    "signature": "个性签名",
    "avatar": "https://...",
    "follower_count": 10000,
    "following_count": 100,
    "aweme_count": 50,
    "favoriting_count": 200
  }
}

// Works List Response
{
  "success": true,
  "data": {
    "works": [...],
    "has_more": true,
    "cursor": 1234567890
  }
}
```

## Related Capabilities

- `video-parse`: 视频解析（已有）
- `search-feature`: 搜索功能
