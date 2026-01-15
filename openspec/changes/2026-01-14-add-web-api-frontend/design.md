# Design: Web API & Frontend Architecture

## Overview

本设计文档描述抖音爬虫项目的 Web API 和前端架构扩展方案。

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Vue3 + Element Plus)           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ 视频解析 │ │ 用户分析 │ │ 搜索中心 │ │ 评论分析 │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│  │ 直播信息 │ │ 我的收藏 │ │ 关系网络 │                        │
│  └──────────┘ └──────────┘ └──────────┘                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    API Routers                           │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐            │    │
│  │  │ video  │ │  auth  │ │  user  │ │ search │            │    │
│  │  └────────┘ └────────┘ └────────┘ └────────┘            │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐            │    │
│  │  │comment │ │  live  │ │collect │ │relation│            │    │
│  │  └────────┘ └────────┘ └────────┘ └────────┘            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Services Layer                        │    │
│  │  (业务逻辑封装，调用 DouyinAPI)                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Schemas Layer                         │    │
│  │  (Pydantic 数据模型，请求/响应验证)                      │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Core Layer (Existing)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ DouyinAPI   │  │  Builder    │  │   Utils     │              │
│  │ (dy_apis/)  │  │ (builder/)  │  │  (utils/)   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

## Backend Design

### Directory Structure

```
api/
├── main.py                 # FastAPI 应用入口
├── config.py               # 配置
├── routers/                # 路由层
│   ├── video.py            # 视频相关 (已有)
│   ├── auth.py             # 认证相关 (已有)
│   ├── user.py             # 用户相关 (新增)
│   ├── search.py           # 搜索相关 (新增)
│   ├── comment.py          # 评论相关 (新增)
│   ├── live.py             # 直播相关 (新增)
│   ├── collection.py       # 收藏相关 (新增)
│   └── relation.py         # 关系相关 (新增)
├── services/               # 服务层
│   ├── video_service.py    # (已有)
│   ├── auth_service.py     # (已有)
│   ├── user_service.py     # (新增)
│   ├── search_service.py   # (新增)
│   ├── comment_service.py  # (新增)
│   ├── live_service.py     # (新增)
│   ├── collection_service.py # (新增)
│   └── relation_service.py # (新增)
└── schemas/                # 数据模型
    ├── video.py            # (已有)
    ├── auth.py             # (已有)
    ├── user.py             # (新增)
    ├── search.py           # (新增)
    ├── comment.py          # (新增)
    ├── live.py             # (新增)
    ├── collection.py       # (新增)
    └── relation.py         # (新增)
```

### API Endpoints Design

#### 1. User Module (`/api/user`)

| Method | Endpoint | Description | DouyinAPI Method |
|--------|----------|-------------|------------------|
| GET | `/info` | 获取用户信息 | `get_user_info` |
| GET | `/works` | 获取用户作品列表 | `get_user_work_info` |
| GET | `/works/all` | 获取用户全部作品 | `get_user_all_work_info` |

#### 2. Search Module (`/api/search`)

| Method | Endpoint | Description | DouyinAPI Method |
|--------|----------|-------------|------------------|
| GET | `/works` | 搜索作品 | `search_general_work` |
| GET | `/users` | 搜索用户 | `search_user` |
| GET | `/lives` | 搜索直播 | `search_live` |

#### 3. Comment Module (`/api/comment`)

| Method | Endpoint | Description | DouyinAPI Method |
|--------|----------|-------------|------------------|
| GET | `/list` | 获取一级评论 | `get_work_out_comment` |
| GET | `/replies` | 获取二级评论 | `get_work_inner_comment` |
| GET | `/all` | 获取全部评论 | `get_work_all_comment` |

#### 4. Live Module (`/api/live`)

| Method | Endpoint | Description | DouyinAPI Method |
|--------|----------|-------------|------------------|
| GET | `/info` | 获取直播间信息 | `get_live_info` |
| GET | `/products` | 获取直播商品 | `get_live_production` |
| GET | `/products/all` | 获取全部商品 | `get_all_live_production` |
| GET | `/product/detail` | 获取商品详情 | `get_live_production_detail` |

#### 5. Collection Module (`/api/collection`)

| Method | Endpoint | Description | DouyinAPI Method |
|--------|----------|-------------|------------------|
| GET | `/list` | 获取收藏夹列表 | `get_collect_list` |
| POST | `/add` | 添加到收藏 | `collect_aweme` |
| POST | `/move` | 移动收藏 | `move_collect_aweme` |
| DELETE | `/remove` | 移除收藏 | `remove_collect_aweme` |

#### 6. Relation Module (`/api/relation`)

| Method | Endpoint | Description | DouyinAPI Method |
|--------|----------|-------------|------------------|
| GET | `/followers` | 获取粉丝列表 | `get_user_follower_list` |
| GET | `/following` | 获取关注列表 | `get_user_following_list` |
| GET | `/notices` | 获取通知列表 | `get_notice_list` |

## Frontend Design

### Directory Structure

```
web/src/
├── main.ts                 # 入口
├── App.vue                 # 根组件
├── router/                 # 路由配置 (新增)
│   └── index.ts
├── views/                  # 页面组件 (新增)
│   ├── HomeView.vue        # 首页（视频解析）
│   ├── UserView.vue        # 用户分析
│   ├── SearchView.vue      # 搜索中心
│   ├── CommentView.vue     # 评论分析
│   ├── LiveView.vue        # 直播信息
│   ├── CollectionView.vue  # 我的收藏
│   └── RelationView.vue    # 关系网络
├── components/             # 通用组件
│   ├── layout/             # 布局组件 (新增)
│   │   ├── AppHeader.vue
│   │   ├── AppSidebar.vue
│   │   └── AppFooter.vue
│   ├── user/               # 用户相关组件 (新增)
│   │   ├── UserCard.vue
│   │   └── WorkList.vue
│   ├── search/             # 搜索相关组件 (新增)
│   │   ├── SearchBar.vue
│   │   └── ResultList.vue
│   └── ...                 # 现有组件
├── api/                    # API 调用
│   ├── video.ts            # (已有)
│   ├── auth.ts             # (已有)
│   ├── user.ts             # (新增)
│   ├── search.ts           # (新增)
│   ├── comment.ts          # (新增)
│   ├── live.ts             # (新增)
│   ├── collection.ts       # (新增)
│   └── relation.ts         # (新增)
└── types/                  # 类型定义
    ├── video.ts            # (已有)
    ├── auth.ts             # (已有)
    └── ...                 # (新增)
```

### UI/UX Design Principles

1. **一致性**：所有页面使用统一的布局和交互模式
2. **响应式**：支持桌面和移动端
3. **渐进式加载**：大数据列表使用虚拟滚动
4. **错误处理**：统一的错误提示和重试机制
5. **导出功能**：支持 Excel/JSON 导出

### Navigation Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Logo    [首页] [用户] [搜索] [评论] [直播] [收藏] [关系]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                      Page Content                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Input → Frontend Component → API Call → FastAPI Router
                                                    │
                                                    ▼
                                            Service Layer
                                                    │
                                                    ▼
                                            DouyinAPI Method
                                                    │
                                                    ▼
                                            Douyin Server
                                                    │
                                                    ▼
                                            Response Data
                                                    │
                                                    ▼
                                            Schema Validation
                                                    │
                                                    ▼
                                            Frontend Display
```

## Error Handling Strategy

### Backend

```python
# 统一错误响应格式
class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
    detail: Optional[str] = None

# 全局异常处理
@app.exception_handler(DouyinAPIError)
async def douyin_api_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="DOUYIN_API_ERROR",
            message=str(exc)
        ).dict()
    )
```

### Frontend

```typescript
// 统一错误处理
async function apiCall<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn()
  } catch (error) {
    if (error.response?.status === 401) {
      // Cookie 失效，提示重新登录
      showCookieManager()
    } else {
      ElMessage.error(error.message || '请求失败')
    }
    throw error
  }
}
```

## Security Considerations

1. **Cookie 安全**：Cookie 仅存储在服务端 `.env` 文件
2. **CORS 配置**：限制允许的来源
3. **请求频率**：考虑添加速率限制
4. **输入验证**：所有输入通过 Pydantic 验证

## Performance Considerations

1. **分页加载**：大数据列表使用游标分页
2. **缓存策略**：考虑添加 Redis 缓存热点数据
3. **并发控制**：限制同时进行的爬取任务数
4. **前端优化**：使用虚拟滚动、懒加载

## Trade-offs

| 决策 | 优点 | 缺点 |
|------|------|------|
| 单体架构 | 部署简单，开发效率高 | 扩展性受限 |
| RESTful API | 简单直观，易于理解 | 某些场景不如 GraphQL 灵活 |
| Vue3 + Element Plus | 生态成熟，组件丰富 | 包体积较大 |
| 无数据库 | 简化部署，无状态 | 无法持久化用户数据 |
