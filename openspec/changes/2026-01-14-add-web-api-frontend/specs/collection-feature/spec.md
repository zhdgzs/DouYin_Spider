# Spec: Collection Feature API

## Overview

提供收藏夹管理相关 API，包括查看、添加、移动、删除收藏。

## ADDED Requirements

### Requirement: Collection List API

系统 SHALL 提供获取收藏夹列表的 API 端点。

#### Scenario: 获取收藏夹列表

**Given** 用户已登录（Cookie 有效）
**When** 调用 `GET /api/collection/list`
**Then** 返回用户的收藏夹列表

---

### Requirement: Add to Collection API

系统 SHALL 提供添加作品到收藏夹的 API 端点。

#### Scenario: 添加作品到收藏

**Given** 用户提供作品 ID 和收藏夹 ID
**When** 调用 `POST /api/collection/add`
**Then** 将作品添加到指定收藏夹

---

### Requirement: Move Collection API

系统 SHALL 提供移动收藏作品的 API 端点。

#### Scenario: 移动收藏到其他收藏夹

**Given** 用户提供作品 ID、源收藏夹 ID、目标收藏夹 ID
**When** 调用 `POST /api/collection/move`
**Then** 将作品从源收藏夹移动到目标收藏夹

---

### Requirement: Remove from Collection API

系统 SHALL 提供从收藏夹移除作品的 API 端点。

#### Scenario: 从收藏夹移除作品

**Given** 用户提供作品 ID 和收藏夹 ID
**When** 调用 `DELETE /api/collection/remove`
**Then** 将作品从收藏夹中移除

---

## API Schema

### Request

```
GET /api/collection/list
Query Parameters:
  - cursor: int (optional, default: 0) - 分页游标
  - count: int (optional, default: 20) - 每页数量

POST /api/collection/add
Body:
  {
    "aweme_id": "作品ID",
    "collect_id": "收藏夹ID"
  }

POST /api/collection/move
Body:
  {
    "aweme_id": "作品ID",
    "from_collect_id": "源收藏夹ID",
    "to_collect_id": "目标收藏夹ID"
  }

DELETE /api/collection/remove
Body:
  {
    "aweme_id": "作品ID",
    "collect_id": "收藏夹ID"
  }
```

### Response

```json
// Collection List Response
{
  "success": true,
  "data": {
    "collections": [
      {
        "collect_id": "...",
        "name": "收藏夹名称",
        "cover": "...",
        "count": 50
      }
    ],
    "has_more": false,
    "cursor": 0
  }
}

// Add/Move/Remove Response
{
  "success": true,
  "message": "操作成功"
}
```

## Related Capabilities

- `video-parse`: 视频解析（获取 aweme_id）
- `user-management`: 用户管理
