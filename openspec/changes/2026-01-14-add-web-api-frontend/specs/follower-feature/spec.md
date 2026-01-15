# Spec: Follower Feature API

## Overview

提供粉丝列表、关注列表和通知列表相关 API。

## ADDED Requirements

### Requirement: Follower List API

系统 SHALL 提供获取用户粉丝列表的 API 端点。

#### Scenario: 获取粉丝列表（分页）

**Given** 用户提供目标用户的 sec_uid
**When** 调用 `GET /api/relation/followers?sec_uid={id}&cursor={cursor}&count={count}`
**Then** 返回粉丝列表

#### Scenario: 获取指定数量的粉丝

**Given** 用户提供目标用户的 sec_uid 和需要的数量
**When** 调用 `GET /api/relation/followers/some?sec_uid={id}&count={count}`
**Then** 返回指定数量的粉丝列表

---

### Requirement: Following List API

系统 SHALL 提供获取用户关注列表的 API 端点。

#### Scenario: 获取关注列表（分页）

**Given** 用户提供目标用户的 sec_uid
**When** 调用 `GET /api/relation/following?sec_uid={id}&cursor={cursor}&count={count}`
**Then** 返回关注列表

#### Scenario: 获取指定数量的关注

**Given** 用户提供目标用户的 sec_uid 和需要的数量
**When** 调用 `GET /api/relation/following/some?sec_uid={id}&count={count}`
**Then** 返回指定数量的关注列表

---

### Requirement: Notice List API

系统 SHALL 提供获取通知列表的 API 端点。

#### Scenario: 获取通知列表

**Given** 用户已登录（Cookie 有效）
**When** 调用 `GET /api/relation/notices?cursor={cursor}&count={count}`
**Then** 返回通知列表

---

## API Schema

### Request

```
GET /api/relation/followers
Query Parameters:
  - sec_uid: string (required) - 用户安全 ID
  - cursor: int (optional, default: 0) - 分页游标
  - count: int (optional, default: 20) - 每页数量

GET /api/relation/following
Query Parameters:
  - sec_uid: string (required) - 用户安全 ID
  - cursor: int (optional, default: 0) - 分页游标
  - count: int (optional, default: 20) - 每页数量

GET /api/relation/notices
Query Parameters:
  - cursor: int (optional, default: 0) - 分页游标
  - count: int (optional, default: 20) - 每页数量
```

### Response

```json
// Follower/Following List Response
{
  "success": true,
  "data": {
    "users": [
      {
        "uid": "...",
        "sec_uid": "...",
        "nickname": "用户昵称",
        "avatar": "...",
        "signature": "个性签名",
        "follower_count": 10000,
        "following_count": 100
      }
    ],
    "has_more": true,
    "cursor": 1234567890,
    "total": 5000
  }
}

// Notice List Response
{
  "success": true,
  "data": {
    "notices": [
      {
        "notice_id": "...",
        "type": "like",
        "content": "xxx 赞了你的作品",
        "user": {...},
        "aweme": {...},
        "create_time": 1234567890
      }
    ],
    "has_more": true,
    "cursor": 1234567890
  }
}
```

## Related Capabilities

- `user-management`: 用户管理
