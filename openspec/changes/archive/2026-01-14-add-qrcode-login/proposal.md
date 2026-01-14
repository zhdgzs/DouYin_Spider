# Change: 添加扫码登录功能

## Why

当前项目存在以下认证痛点：

1. **Cookie 获取门槛高**：用户需要手动打开浏览器 F12，找到网络请求，复制 Cookie 到 `.env` 文件
2. **Cookie 过期无感知**：Cookie 失效后 API 调用会静默失败，用户难以定位问题
3. **用户体验差**：非技术用户难以完成 Cookie 配置流程

添加扫码登录功能可以：
- 一键获取有效 Cookie，无需手动操作浏览器
- 前端自动检测 Cookie 状态，失效时主动提示
- 提供友好的二维码弹窗，扫码即可完成登录

## What Changes

### 后端 (Python/FastAPI)

- **ADDED** 扫码登录服务模块 (`utils/qrcode_login.py`)
  - 调用抖音 SSO API 获取二维码
  - 轮询检查扫码状态
  - 登录成功后自动保存 Cookie 到 `.env`

- **ADDED** Cookie 验证 API (`/api/auth/check`)
  - 检测当前 Cookie 是否存在且有效
  - 返回认证状态和用户基本信息

- **ADDED** 二维码获取 API (`/api/auth/qrcode`)
  - 生成登录二维码 URL 和 token
  - 返回二维码图片 Base64 或 URL

- **ADDED** 扫码状态轮询 API (`/api/auth/qrcode/status`)
  - 检查二维码扫码状态
  - 登录成功后返回新 Cookie

### 前端 (Vue 3)

- **ADDED** Cookie 状态检测组件 (`AuthChecker.vue`)
  - 页面加载时自动检测 Cookie 状态
  - 无效时触发二维码弹窗

- **ADDED** 扫码登录弹窗组件 (`QRCodeLogin.vue`)
  - 显示登录二维码
  - 实时显示扫码状态（等待扫码/已扫码/确认中/已过期）
  - 支持二维码过期自动刷新

- **MODIFIED** App.vue
  - 集成 AuthChecker 组件
  - 全局认证状态管理

## Impact

- Affected specs: 新增 `qrcode-auth` capability
- Affected code:
  - 新增 `utils/qrcode_login.py`（扫码登录核心逻辑）
  - 新增 `api/routers/auth.py`（认证相关 API）
  - 新增 `api/services/auth_service.py`（认证服务）
  - 新增 `web/src/components/AuthChecker.vue`
  - 新增 `web/src/components/QRCodeLogin.vue`
  - 新增 `web/src/api/auth.ts`
  - 修改 `web/src/App.vue`（集成认证检测）
  - 修改 `api/main.py`（注册认证路由）

- **不影响现有代码**:
  - 原有 Cookie 手动配置方式仍然有效
  - 现有 API 接口保持不变
  - 命令行工具 `main.py` 不受影响

## 技术方案概述

### 抖音 SSO 扫码登录流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   前端页面   │     │  后端 API   │     │  抖音 SSO   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ 1. 检测 Cookie    │                   │
       │──────────────────>│                   │
       │                   │                   │
       │ 2. Cookie 无效    │                   │
       │<──────────────────│                   │
       │                   │                   │
       │ 3. 请求二维码     │                   │
       │──────────────────>│ 4. get_qrcode    │
       │                   │──────────────────>│
       │                   │                   │
       │                   │ 5. qrcode_url +  │
       │                   │    token         │
       │                   │<──────────────────│
       │ 6. 显示二维码     │                   │
       │<──────────────────│                   │
       │                   │                   │
       │ 7. 轮询状态       │                   │
       │──────────────────>│ 8. check_qrconnect│
       │                   │──────────────────>│
       │                   │                   │
       │                   │ 9. status        │
       │                   │<──────────────────│
       │ 10. 状态更新      │                   │
       │<──────────────────│                   │
       │                   │                   │
       │     [用户扫码确认后]                   │
       │                   │                   │
       │                   │ 11. redirect_url │
       │                   │    + cookies     │
       │                   │<──────────────────│
       │                   │                   │
       │                   │ 12. 保存 Cookie  │
       │                   │    到 .env       │
       │                   │                   │
       │ 13. 登录成功      │                   │
       │<──────────────────│                   │
       │                   │                   │
```

### 扫码状态码

| 状态码 | 含义 | 前端处理 |
|-------|------|---------|
| 1 | 等待扫码 | 显示"请使用抖音 App 扫码" |
| 2 | 已扫码，等待确认 | 显示"扫码成功，请在手机上确认" |
| 3 | 确认登录 | 获取 Cookie，关闭弹窗 |
| 4 | 访问频繁 | 显示错误，建议稍后重试 |
| 5 | 二维码过期 | 自动刷新二维码 |

## 依赖说明

### Python 依赖（新增）
```
qrcode[pil]>=7.0  # 二维码生成（可选，用于终端显示）
```

### 前端依赖（已有）
- Element Plus（弹窗、加载状态）
- Axios（API 请求）

## 安全考虑

1. **Cookie 存储**：Cookie 仅保存在服务端 `.env` 文件，不暴露给前端
2. **API 限流**：二维码获取接口添加频率限制，防止滥用
3. **Token 有效期**：二维码 token 有效期约 5 分钟，过期自动刷新
4. **HTTPS 建议**：生产环境建议使用 HTTPS 保护 Cookie 传输
