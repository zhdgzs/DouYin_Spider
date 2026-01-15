# Tasks: Web API & Frontend Implementation

## Phase 1: Backend API Foundation (Priority: High)

### 1.1 User Module
- [x] 创建 `api/schemas/user.py` - 用户相关数据模型
- [x] 创建 `api/services/user_service.py` - 用户服务层
- [x] 创建 `api/routers/user.py` - 用户 API 路由
  - [x] `GET /api/user/info` - 获取用户信息
  - [x] `GET /api/user/works` - 获取用户作品列表（分页）
  - [x] `GET /api/user/works/all` - 获取用户全部作品
- [x] 在 `api/main.py` 注册用户路由
- [x] 测试用户 API 端点

### 1.2 Search Module
- [x] 创建 `api/schemas/search.py` - 搜索相关数据模型
- [x] 创建 `api/services/search_service.py` - 搜索服务层
- [x] 创建 `api/routers/search.py` - 搜索 API 路由
  - [x] `GET /api/search/works` - 搜索作品
  - [x] `GET /api/search/users` - 搜索用户
  - [x] `GET /api/search/lives` - 搜索直播
- [x] 在 `api/main.py` 注册搜索路由
- [x] 测试搜索 API 端点

### 1.3 Comment Module
- [x] 创建 `api/schemas/comment.py` - 评论相关数据模型
- [x] 创建 `api/services/comment_service.py` - 评论服务层
- [x] 创建 `api/routers/comment.py` - 评论 API 路由
  - [x] `GET /api/comment/list` - 获取一级评论
  - [x] `GET /api/comment/replies` - 获取二级评论
  - [x] `GET /api/comment/all` - 获取全部评论
- [x] 在 `api/main.py` 注册评论路由
- [x] 测试评论 API 端点

### 1.4 Live Module
- [x] 创建 `api/schemas/live.py` - 直播相关数据模型
- [x] 创建 `api/services/live_service.py` - 直播服务层
- [x] 创建 `api/routers/live.py` - 直播 API 路由
  - [x] `GET /api/live/info` - 获取直播间信息
  - [x] `GET /api/live/products` - 获取直播商品列表
  - [x] `GET /api/live/products/all` - 获取全部商品
  - [x] `GET /api/live/product/detail` - 获取商品详情
- [x] 在 `api/main.py` 注册直播路由
- [x] 测试直播 API 端点

### 1.5 Collection Module
- [x] 创建 `api/schemas/collection.py` - 收藏相关数据模型
- [x] 创建 `api/services/collection_service.py` - 收藏服务层
- [x] 创建 `api/routers/collection.py` - 收藏 API 路由
  - [x] `GET /api/collection/list` - 获取收藏夹列表
  - [x] `POST /api/collection/add` - 添加到收藏
  - [x] `POST /api/collection/move` - 移动收藏
  - [x] `DELETE /api/collection/remove` - 移除收藏
- [x] 在 `api/main.py` 注册收藏路由
- [x] 测试收藏 API 端点

### 1.6 Relation Module
- [x] 创建 `api/schemas/relation.py` - 关系相关数据模型
- [x] 创建 `api/services/relation_service.py` - 关系服务层
- [x] 创建 `api/routers/relation.py` - 关系 API 路由
  - [x] `GET /api/relation/followers` - 获取粉丝列表
  - [x] `GET /api/relation/following` - 获取关注列表
  - [x] `GET /api/relation/notices` - 获取通知列表
- [x] 在 `api/main.py` 注册关系路由
- [x] 测试关系 API 端点

---

## Phase 2: Frontend Infrastructure (Priority: High)

### 2.1 Router Setup
- [x] 安装 vue-router: `npm install vue-router@4`
- [x] 创建 `web/src/router/index.ts` - 路由配置
- [x] 更新 `web/src/main.ts` - 注册路由
- [x] 更新 `web/src/App.vue` - 添加 `<router-view>`

### 2.2 Layout Components
- [x] 创建 `web/src/components/layout/AppHeader.vue` - 顶部导航
- [x] 创建 `web/src/components/layout/AppSidebar.vue` - 侧边栏（可选）
- [x] 创建 `web/src/components/layout/AppFooter.vue` - 页脚
- [x] 创建 `web/src/components/layout/MainLayout.vue` - 主布局

### 2.3 API Layer
- [x] 创建 `web/src/api/user.ts` - 用户 API
- [x] 创建 `web/src/api/search.ts` - 搜索 API
- [x] 创建 `web/src/api/comment.ts` - 评论 API
- [x] 创建 `web/src/api/live.ts` - 直播 API
- [x] 创建 `web/src/api/collection.ts` - 收藏 API
- [x] 创建 `web/src/api/relation.ts` - 关系 API

### 2.4 Type Definitions
- [x] 创建 `web/src/types/user.ts` - 用户类型
- [x] 创建 `web/src/types/search.ts` - 搜索类型
- [x] 创建 `web/src/types/comment.ts` - 评论类型
- [x] 创建 `web/src/types/live.ts` - 直播类型
- [x] 创建 `web/src/types/collection.ts` - 收藏类型
- [x] 创建 `web/src/types/relation.ts` - 关系类型

---

## Phase 3: Frontend Pages (Priority: Medium)

### 3.1 Home Page (Refactor)
- [x] 将现有视频解析功能迁移到 `web/src/views/HomeView.vue`
- [x] 适配新的布局结构

### 3.2 User Analysis Page
- [x] 创建 `web/src/views/UserView.vue` - 用户分析页面
- [x] 创建 `web/src/components/user/UserCard.vue` - 用户信息卡片（内联实现）
- [x] 创建 `web/src/components/user/WorkList.vue` - 作品列表组件（内联实现）
- [x] 实现用户链接输入 → 信息展示 → 作品列表

### 3.3 Search Center Page
- [x] 创建 `web/src/views/SearchView.vue` - 搜索中心页面
- [x] 创建 `web/src/components/search/SearchBar.vue` - 搜索栏（内联实现）
- [x] 创建 `web/src/components/search/WorkResult.vue` - 作品搜索结果（内联实现）
- [x] 创建 `web/src/components/search/UserResult.vue` - 用户搜索结果（内联实现）
- [x] 创建 `web/src/components/search/LiveResult.vue` - 直播搜索结果（内联实现）
- [x] 实现 Tab 切换搜索类型

### 3.4 Comment Analysis Page
- [x] 创建 `web/src/views/CommentView.vue` - 评论分析页面
- [x] 创建 `web/src/components/comment/CommentList.vue` - 评论列表（内联实现）
- [x] 创建 `web/src/components/comment/CommentItem.vue` - 评论项（内联实现）
- [x] 实现评论树形展示（一级 + 二级）

### 3.5 Live Info Page
- [x] 创建 `web/src/views/LiveView.vue` - 直播信息页面
- [x] 创建 `web/src/components/live/LiveCard.vue` - 直播间信息卡片（内联实现）
- [x] 创建 `web/src/components/live/ProductList.vue` - 商品列表（内联实现）
- [x] 创建 `web/src/components/live/ProductCard.vue` - 商品卡片（内联实现）

### 3.6 Collection Page
- [x] 创建 `web/src/views/CollectionView.vue` - 收藏管理页面
- [x] 创建 `web/src/components/collection/FolderList.vue` - 收藏夹列表（内联实现）
- [x] 创建 `web/src/components/collection/CollectedItem.vue` - 收藏项（内联实现）

### 3.7 Relation Page
- [x] 创建 `web/src/views/RelationView.vue` - 关系网络页面
- [x] 创建 `web/src/components/relation/UserList.vue` - 用户列表（内联实现）
- [x] 创建 `web/src/components/relation/UserItem.vue` - 用户项（内联实现）
- [x] 实现粉丝/关注 Tab 切换

---

## Phase 4: Enhancement (Priority: Low)

### 4.1 Export Feature
- [ ] 实现作品列表导出为 Excel
- [ ] 实现评论导出为 Excel
- [ ] 实现用户列表导出为 Excel

### 4.2 Batch Operations
- [ ] 实现批量下载作品
- [ ] 实现批量收藏/取消收藏

### 4.3 UI/UX Improvements
- [ ] 添加加载骨架屏
- [ ] 添加虚拟滚动（大列表）
- [ ] 添加暗色主题支持
- [ ] 优化移动端适配

### 4.4 Error Handling
- [ ] 统一错误提示组件
- [ ] 添加请求重试机制
- [ ] 添加网络状态检测

---

## Dependencies

```
Phase 1 (Backend) ─┬─► Phase 2 (Frontend Infra) ─► Phase 3 (Pages)
                   │
                   └─► Phase 4 (Enhancement)
```

## Estimated Effort

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1 | 30 | 2-3 days |
| Phase 2 | 15 | 1 day |
| Phase 3 | 25 | 2-3 days |
| Phase 4 | 12 | 1-2 days |
| **Total** | **82** | **6-9 days** |

## Validation Criteria

- [x] 所有 API 端点通过 Swagger UI 测试
- [x] 前端所有页面可正常访问
- [x] 数据流完整：输入 → API → 展示
- [x] 错误处理正常工作
- [ ] 响应式布局在移动端正常显示
