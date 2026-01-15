# Spec: Comment Feature API

## Overview

提供视频评论获取 API，支持一级评论和二级评论（回复）。

## ADDED Requirements

### Requirement: Comment List API

系统 SHALL 提供获取视频一级评论的 API 端点。

#### Scenario: 获取一级评论列表

**Given** 用户提供有效的视频链接或 aweme_id
**When** 调用 `GET /api/comment/list?aweme_id={id}&cursor={cursor}&count={count}`
**Then** 返回一级评论列表，包括：
- 评论内容
- 评论者信息
- 点赞数
- 回复数
- 评论时间

#### Scenario: 获取全部一级评论

**Given** 用户提供有效的视频链接
**When** 调用 `GET /api/comment/list/all?aweme_id={id}`
**Then** 返回该视频的全部一级评论

---

### Requirement: Comment Replies API

系统 SHALL 提供获取评论回复（二级评论）的 API 端点。

#### Scenario: 获取评论回复

**Given** 用户提供评论 ID
**When** 调用 `GET /api/comment/replies?comment_id={id}&cursor={cursor}&count={count}`
**Then** 返回该评论的回复列表

#### Scenario: 获取全部回复

**Given** 用户提供评论 ID
**When** 调用 `GET /api/comment/replies/all?comment_id={id}`
**Then** 返回该评论的全部回复

---

### Requirement: All Comments API

系统 SHALL 提供获取视频全部评论（含回复）的 API 端点。

#### Scenario: 获取全部评论（含回复）

**Given** 用户提供有效的视频链接
**When** 调用 `GET /api/comment/all?aweme_id={id}`
**Then** 返回该视频的全部评论，包括一级评论和对应的二级回复

---

## API Schema

### Request

```
GET /api/comment/list
Query Parameters:
  - aweme_id: string (required) - 视频 ID
  - cursor: int (optional, default: 0) - 分页游标
  - count: int (optional, default: 20) - 每页数量

GET /api/comment/replies
Query Parameters:
  - comment_id: string (required) - 评论 ID
  - aweme_id: string (required) - 视频 ID
  - cursor: int (optional, default: 0) - 分页游标
  - count: int (optional, default: 20) - 每页数量

GET /api/comment/all
Query Parameters:
  - aweme_id: string (required) - 视频 ID
```

### Response

```json
// Comment List Response
{
  "success": true,
  "data": {
    "comments": [
      {
        "cid": "评论ID",
        "text": "评论内容",
        "user": {
          "uid": "...",
          "nickname": "...",
          "avatar": "..."
        },
        "digg_count": 100,
        "reply_count": 5,
        "create_time": 1234567890
      }
    ],
    "has_more": true,
    "cursor": 1234567890,
    "total": 500
  }
}

// All Comments Response (with replies)
{
  "success": true,
  "data": {
    "comments": [
      {
        "cid": "...",
        "text": "...",
        "user": {...},
        "replies": [
          {
            "cid": "...",
            "text": "...",
            "user": {...}
          }
        ]
      }
    ],
    "total_comments": 500,
    "total_replies": 1200
  }
}
```

## Related Capabilities

- `video-parse`: 视频解析（获取 aweme_id）
