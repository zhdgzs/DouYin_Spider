## ADDED Requirements

### Requirement: Cookie 状态检测

系统 SHALL 提供 Cookie 有效性检测功能，在用户访问前端页面时自动验证当前 Cookie 是否有效。

#### Scenario: Cookie 有效
- **WHEN** 用户访问前端页面
- **AND** 系统中存在有效的 Cookie
- **THEN** 系统返回认证成功状态
- **AND** 返回当前登录用户的基本信息（UID、昵称、头像）

#### Scenario: Cookie 无效或不存在
- **WHEN** 用户访问前端页面
- **AND** 系统中不存在 Cookie 或 Cookie 已过期
- **THEN** 系统返回认证失败状态
- **AND** 前端自动弹出扫码登录弹窗

---

### Requirement: 二维码获取

系统 SHALL 提供登录二维码获取功能，调用抖音 SSO API 生成扫码登录二维码。

#### Scenario: 成功获取二维码
- **WHEN** 用户请求获取登录二维码
- **THEN** 系统调用 `https://sso.douyin.com/get_qrcode/` 接口
- **AND** 返回二维码 URL 和登录 token
- **AND** 返回二维码图片的 Base64 编码
- **AND** 返回二维码过期时间（约 5 分钟）

#### Scenario: 获取二维码失败
- **WHEN** 用户请求获取登录二维码
- **AND** 抖音 SSO API 返回错误
- **THEN** 系统返回错误信息
- **AND** 前端显示友好的错误提示

---

### Requirement: 扫码状态轮询

系统 SHALL 提供扫码状态轮询功能，实时检测用户扫码进度。

#### Scenario: 等待扫码
- **WHEN** 前端以 3 秒间隔轮询扫码状态
- **AND** 用户尚未扫码
- **THEN** 系统返回状态码 1（等待扫码）
- **AND** 前端显示"请使用抖音 App 扫描二维码"

#### Scenario: 已扫码等待确认
- **WHEN** 用户已扫描二维码
- **AND** 尚未在手机上确认登录
- **THEN** 系统返回状态码 2（已扫码）
- **AND** 前端显示"扫码成功，请在手机上确认登录"

#### Scenario: 确认登录成功
- **WHEN** 用户在手机上确认登录
- **THEN** 系统返回状态码 3（确认登录）
- **AND** 系统获取登录 Cookie
- **AND** 系统自动保存 Cookie 到 `.env` 文件
- **AND** 前端关闭弹窗并刷新认证状态

#### Scenario: 访问频繁
- **WHEN** 请求频率过高触发风控
- **THEN** 系统返回状态码 4（访问频繁）
- **AND** 前端显示"请求过于频繁，请稍后重试"

#### Scenario: 二维码过期
- **WHEN** 二维码超过有效期（约 5 分钟）
- **THEN** 系统返回状态码 5（二维码过期）
- **AND** 前端自动刷新二维码

---

### Requirement: Cookie 自动保存

系统 SHALL 在登录成功后自动将 Cookie 保存到配置文件。

#### Scenario: 保存 Cookie 到 .env
- **WHEN** 用户扫码登录成功
- **AND** 系统获取到有效的 Cookie
- **THEN** 系统将 Cookie 写入项目根目录的 `.env` 文件
- **AND** 如果 `.env` 文件中已存在 `COOKIE=` 行，则更新该行
- **AND** 如果不存在，则追加新行

#### Scenario: 保存失败处理
- **WHEN** Cookie 保存过程中发生错误（如权限问题）
- **THEN** 系统记录错误日志
- **AND** 返回错误信息给前端
- **AND** 前端显示"Cookie 保存失败，请检查文件权限"

---

### Requirement: 前端扫码登录弹窗

系统 SHALL 提供友好的扫码登录弹窗界面。

#### Scenario: 显示二维码弹窗
- **WHEN** 系统检测到 Cookie 无效
- **THEN** 前端自动弹出扫码登录弹窗
- **AND** 弹窗中央显示登录二维码
- **AND** 弹窗下方显示当前扫码状态文案

#### Scenario: 状态实时更新
- **WHEN** 扫码状态发生变化
- **THEN** 弹窗实时更新状态显示
- **AND** 已扫码时显示绿色勾选图标
- **AND** 过期时显示刷新按钮

#### Scenario: 登录成功关闭弹窗
- **WHEN** 用户登录成功
- **THEN** 弹窗自动关闭
- **AND** 显示登录成功提示
- **AND** 页面刷新认证状态

---

### Requirement: API 接口规范

系统 SHALL 提供以下 RESTful API 接口。

#### Scenario: GET /api/auth/check
- **WHEN** 客户端请求 `GET /api/auth/check`
- **THEN** 系统返回 JSON 格式响应
- **AND** 响应包含 `valid` 布尔字段表示 Cookie 是否有效
- **AND** 有效时包含 `user_info` 对象（uid, nickname, avatar）
- **AND** 无效时包含 `error` 字符串说明原因

#### Scenario: GET /api/auth/qrcode
- **WHEN** 客户端请求 `GET /api/auth/qrcode`
- **THEN** 系统返回 JSON 格式响应
- **AND** 响应包含 `success` 布尔字段
- **AND** 成功时 `data` 包含 `token`, `qrcode_url`, `qrcode_base64`, `expire_at`

#### Scenario: GET /api/auth/qrcode/status
- **WHEN** 客户端请求 `GET /api/auth/qrcode/status?token=xxx`
- **THEN** 系统返回 JSON 格式响应
- **AND** 响应包含 `status` 数字字段（1-5）
- **AND** 响应包含 `message` 字符串字段
- **AND** 状态为 3 时包含 `cookie` 字段（仅用于内部处理，不暴露给前端）
