# Spec: Search Feature API

## Overview

提供作品、用户、直播的关键词搜索 API。

## ADDED Requirements

### Requirement: Work Search API

系统 SHALL 提供关键词搜索作品的 API 端点。

#### Scenario: 搜索作品

**Given** 用户提供搜索关键词
**When** 调用 `GET /api/search/works?keyword={keyword}&count={count}&sort_type={sort}&publish_time={time}`
**Then** 返回匹配的作品列表

#### Scenario: 搜索作品带筛选条件

**Given** 用户提供关键词和筛选条件
**When** 调用搜索 API 并指定排序方式、发布时间、视频时长等
**Then** 返回符合筛选条件的作品列表

---

### Requirement: User Search API

系统 SHALL 提供关键词搜索用户的 API 端点。

#### Scenario: 搜索用户

**Given** 用户提供搜索关键词
**When** 调用 `GET /api/search/users?keyword={keyword}&count={count}`
**Then** 返回匹配的用户列表

---

### Requirement: Live Search API

系统 SHALL 提供关键词搜索直播的 API 端点。

#### Scenario: 搜索直播

**Given** 用户提供搜索关键词
**When** 调用 `GET /api/search/lives?keyword={keyword}&count={count}`
**Then** 返回匹配的直播间列表

---

## API Schema

### Request

```
GET /api/search/works
Query Parameters:
  - keyword: string (required) - 搜索关键词
  - count: int (optional, default: 20) - 返回数量
  - sort_type: string (optional) - 排序方式 (0: 综合, 1: 最多点赞, 2: 最新发布)
  - publish_time: string (optional) - 发布时间 (0: 不限, 1: 一天内, 7: 一周内, 180: 半年内)
  - filter_duration: string (optional) - 视频时长
  - content_type: string (optional) - 内容形式 (0: 不限, 1: 视频, 2: 图文)

GET /api/search/users
Query Parameters:
  - keyword: string (required) - 搜索关键词
  - count: int (optional, default: 20) - 返回数量

GET /api/search/lives
Query Parameters:
  - keyword: string (required) - 搜索关键词
  - count: int (optional, default: 20) - 返回数量
```

### Response

```json
// Works Search Response
{
  "success": true,
  "data": {
    "works": [
      {
        "aweme_id": "...",
        "title": "...",
        "cover": "...",
        "author": {...},
        "statistics": {...}
      }
    ],
    "total": 100
  }
}

// Users Search Response
{
  "success": true,
  "data": {
    "users": [
      {
        "uid": "...",
        "nickname": "...",
        "avatar": "...",
        "signature": "...",
        "follower_count": 10000
      }
    ],
    "total": 50
  }
}

// Lives Search Response
{
  "success": true,
  "data": {
    "lives": [
      {
        "room_id": "...",
        "title": "...",
        "cover": "...",
        "user": {...},
        "user_count": 1000
      }
    ],
    "total": 20
  }
}
```

## Related Capabilities

- `user-management`: 用户管理
- `live-feature`: 直播功能
