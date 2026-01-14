## 1. 后端核心模块

### 1.1 扫码登录服务
- [x] 1.1.1 创建 `utils/qrcode_login.py` 模块
- [x] 1.1.2 实现 `generate_verify_fp()` 生成设备指纹
- [x] 1.1.3 实现 `generate_ttwid()` 生成追踪 ID
- [x] 1.1.4 实现 `get_qrcode()` 获取登录二维码
- [x] 1.1.5 实现 `check_qrconnect()` 检查扫码状态
- [x] 1.1.6 实现 `login_redirect()` 处理登录重定向
- [x] 1.1.7 实现 `save_cookie_to_env()` 保存 Cookie 到 .env

### 1.2 Cookie 验证服务
- [x] 1.2.1 创建 `api/services/auth_service.py`
- [x] 1.2.2 实现 `check_cookie_valid()` 验证 Cookie 有效性
- [x] 1.2.3 实现 `get_current_user_info()` 获取当前用户信息

## 2. 后端 API 接口

### 2.1 认证路由
- [x] 2.1.1 创建 `api/routers/auth.py`
- [x] 2.1.2 实现 `GET /api/auth/check` Cookie 状态检测接口
- [x] 2.1.3 实现 `GET /api/auth/qrcode` 获取登录二维码接口
- [x] 2.1.4 实现 `GET /api/auth/qrcode/status` 扫码状态轮询接口
- [x] 2.1.5 在 `api/main.py` 注册认证路由

### 2.2 数据模型
- [x] 2.2.1 创建 `api/schemas/auth.py` 定义请求/响应模型
- [x] 2.2.2 定义 `AuthCheckResponse` 模型
- [x] 2.2.3 定义 `QRCodeResponse` 模型
- [x] 2.2.4 定义 `QRCodeStatusResponse` 模型

## 3. 前端组件

### 3.1 API 层
- [x] 3.1.1 创建 `web/src/api/auth.ts`
- [x] 3.1.2 实现 `checkAuth()` 检测认证状态
- [x] 3.1.3 实现 `getQRCode()` 获取二维码
- [x] 3.1.4 实现 `checkQRCodeStatus()` 检查扫码状态

### 3.2 类型定义
- [x] 3.2.1 创建 `web/src/types/auth.ts`
- [x] 3.2.2 定义 `AuthStatus` 类型
- [x] 3.2.3 定义 `QRCodeData` 类型
- [x] 3.2.4 定义 `QRCodeStatus` 类型

### 3.3 认证检测组件
- [x] 3.3.1 创建 `web/src/components/AuthChecker.vue`
- [x] 3.3.2 实现页面加载时自动检测 Cookie
- [x] 3.3.3 实现认证失败时触发事件

### 3.4 扫码登录弹窗
- [x] 3.4.1 创建 `web/src/components/QRCodeLogin.vue`
- [x] 3.4.2 实现二维码显示
- [x] 3.4.3 实现扫码状态轮询（3秒间隔）
- [x] 3.4.4 实现状态文案显示（等待/已扫码/确认中/过期）
- [x] 3.4.5 实现二维码过期自动刷新
- [x] 3.4.6 实现登录成功回调

### 3.5 主应用集成
- [x] 3.5.1 修改 `web/src/App.vue` 引入 AuthChecker
- [x] 3.5.2 添加全局认证状态管理
- [x] 3.5.3 集成 QRCodeLogin 弹窗

## 4. 测试与文档

### 4.1 测试
- [ ] 4.1.1 测试二维码获取接口
- [ ] 4.1.2 测试扫码状态轮询
- [ ] 4.1.3 测试登录成功流程
- [ ] 4.1.4 测试二维码过期刷新
- [ ] 4.1.5 测试 Cookie 保存功能

### 4.2 文档
- [ ] 4.2.1 更新 README 添加扫码登录说明
- [ ] 4.2.2 添加 API 文档注释
