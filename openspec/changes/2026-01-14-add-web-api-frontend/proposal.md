# Proposal: 2026-01-14-add-web-api-frontend

## Summary

将抖音爬虫项目的全部核心功能通过 FastAPI 暴露为 Web API，并构建完整的 Vue3 前端界面，实现可视化操作。

## Background

当前项目已实现：
- **视频解析 API** (`/api/video/parse`, `/api/video/proxy`, `/api/video/download`)
- **认证管理 API** (`/api/auth/check`, `/api/auth/qrcode`, `/api/auth/cookie`)
- **前端界面**：视频解析工具（输入链接 → 解析 → 预览/下载）

项目 `DouyinAPI` 类中还有大量功能尚未暴露为 Web API：
- 用户信息与作品列表
- 关键词搜索（作品/用户/直播）
- 评论获取（一级/二级）
- 直播间信息与商品
- 收藏夹管理
- 粉丝/关注列表
- 通知列表
- 推荐 Feed

## Goals

1. **完整 API 覆盖**：将 `DouyinAPI` 的所有方法封装为 RESTful API
2. **统一前端入口**：构建多页面/多 Tab 的 Web 界面
3. **用户体验优化**：支持批量操作、数据导出、实时预览
4. **可扩展架构**：模块化设计，便于后续功能扩展

## Non-Goals

- 不实现用户账号系统（继续使用 Cookie 认证）
- 不实现数据持久化存储（仅提供导出功能）
- 不实现直播 WebSocket 实时监听的 Web 界面（保留 CLI 方式）

## Proposed Solution

### 新增 API 模块

| 模块 | 路由前缀 | 功能 |
|------|----------|------|
| 用户 | `/api/user` | 用户信息、作品列表 |
| 搜索 | `/api/search` | 作品/用户/直播搜索 |
| 评论 | `/api/comment` | 一级/二级评论获取 |
| 直播 | `/api/live` | 直播间信息、商品列表 |
| 收藏 | `/api/collection` | 收藏夹管理 |
| 关系 | `/api/relation` | 粉丝/关注列表 |

### 前端页面规划

| 页面 | 功能描述 |
|------|----------|
| 首页 | 视频解析（已有） |
| 用户分析 | 输入用户链接 → 展示用户信息 + 作品列表 |
| 搜索中心 | 关键词搜索作品/用户/直播 |
| 评论分析 | 输入视频链接 → 展示评论列表 |
| 直播信息 | 输入直播间链接 → 展示直播信息 + 商品 |
| 我的收藏 | 管理收藏夹 |
| 关系网络 | 查看粉丝/关注列表 |

## Impact

- **代码变更**：新增约 10 个 API 路由文件、6 个前端页面组件
- **依赖变更**：无新增依赖
- **兼容性**：完全向后兼容，不影响现有功能

## Alternatives Considered

1. **GraphQL API**：灵活但增加复杂度，RESTful 更适合当前场景
2. **独立前端项目**：增加部署复杂度，保持单体更简单

## Open Questions

1. 是否需要添加请求频率限制？
2. 是否需要支持批量导出为 Excel？
3. 直播商品是否需要支持价格监控？

## References

- 现有 API 实现：`api/routers/video.py`, `api/routers/auth.py`
- DouyinAPI 类：`dy_apis/douyin_api.py`
- 前端实现：`web/src/`
