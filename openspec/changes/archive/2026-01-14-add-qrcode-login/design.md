## Context

本项目是抖音数据爬虫工具，依赖有效的抖音 Cookie 进行 API 认证。当前 Cookie 需要用户手动从浏览器复制，体验较差。本设计旨在通过扫码登录自动获取 Cookie，提升用户体验。

**利益相关者：**
- 终端用户：需要简单的认证方式
- 开发者：需要稳定的认证机制

**约束条件：**
- 依赖抖音 SSO API，可能随时变更
- 需要处理反爬风控（验证码、频率限制）
- Cookie 有效期有限，需要定期刷新

## Goals / Non-Goals

### Goals
- 提供一键扫码登录功能，自动获取有效 Cookie
- 前端自动检测 Cookie 状态，失效时主动提示
- 支持二维码过期自动刷新
- 登录成功后自动保存 Cookie 到配置文件

### Non-Goals
- 不实现 Cookie 自动续期（抖音未提供此能力）
- 不实现多账号管理（保持简单）
- 不实现手机号/密码登录（安全风险高）

## Decisions

### 1. 扫码登录 API 选择

**决策：** 使用抖音 SSO 官方扫码登录 API

**API 端点：**
- 获取二维码：`https://sso.douyin.com/get_qrcode/`
- 检查状态：`https://sso.douyin.com/check_qrconnect/`

**替代方案考虑：**
- Playwright 自动化登录：复杂度高，需要浏览器环境
- 手机号验证码登录：需要接收短信，不便于自动化

**选择理由：**
- 官方 API，稳定性较好
- 无需浏览器环境，纯 HTTP 请求
- 用户体验好，扫码即可

### 2. Cookie 存储方式

**决策：** 继续使用 `.env` 文件存储 Cookie

**理由：**
- 与现有架构一致
- 简单可靠
- 支持手动编辑

**实现细节：**
```python
# 登录成功后更新 .env 文件
def save_cookie_to_env(cookie_str: str):
    env_path = Path(__file__).parent.parent / '.env'
    # 读取现有内容
    content = env_path.read_text() if env_path.exists() else ''
    # 更新或添加 COOKIE 行
    if 'COOKIE=' in content:
        content = re.sub(r'COOKIE=.*', f'COOKIE={cookie_str}', content)
    else:
        content += f'\nCOOKIE={cookie_str}'
    env_path.write_text(content)
```

### 3. 前端轮询策略

**决策：** 使用 3 秒间隔轮询，最长 5 分钟超时

**理由：**
- 3 秒间隔平衡了响应速度和服务器压力
- 5 分钟超时与二维码有效期匹配
- 简单可靠，无需 WebSocket

**状态机：**
```
IDLE → LOADING → WAITING_SCAN → SCANNED → CONFIRMING → SUCCESS
                      ↓              ↓
                   EXPIRED       FAILED
```

### 4. Cookie 有效性检测

**决策：** 调用 `/aweme/v1/web/im/user/info/` 接口验证

**理由：**
- 轻量级接口，响应快
- 返回用户基本信息，可确认登录状态
- 失败时返回明确错误码

**实现：**
```python
async def check_cookie_valid(cookie_str: str) -> dict:
    """
    检查 Cookie 是否有效
    返回: {"valid": bool, "user_info": dict | None, "error": str | None}
    """
```

### 5. 签名参数生成

**决策：** 复用现有 `dy_util.py` 中的签名逻辑

**需要的参数：**
- `verifyFp` / `fp`：设备指纹
- `msToken`：请求令牌
- `ttwid`：追踪 ID

**生成方式：**
```python
# verifyFp 生成
def generate_verify_fp() -> str:
    # 使用现有 generate_msToken 逻辑或新实现
    pass

# ttwid 生成
def generate_ttwid() -> str:
    # 调用抖音 API 获取或本地生成
    pass
```

## API 设计

### 1. Cookie 状态检测

```
GET /api/auth/check

Response:
{
    "valid": true,
    "user_info": {
        "uid": "123456",
        "nickname": "用户昵称",
        "avatar": "https://..."
    }
}

// 或
{
    "valid": false,
    "error": "Cookie 已过期"
}
```

### 2. 获取登录二维码

```
GET /api/auth/qrcode

Response:
{
    "success": true,
    "data": {
        "token": "abc123...",
        "qrcode_url": "https://...",
        "qrcode_base64": "data:image/png;base64,...",
        "expire_at": 1704067200
    }
}
```

### 3. 检查扫码状态

```
GET /api/auth/qrcode/status?token=abc123

Response:
{
    "status": 1,  // 1=等待 2=已扫码 3=确认 4=频繁 5=过期
    "message": "等待扫码",
    "cookie": null  // status=3 时返回 Cookie
}
```

## 前端组件设计

### AuthChecker.vue

```vue
<template>
  <!-- 无 UI，仅逻辑组件 -->
</template>

<script setup>
// 页面加载时检测 Cookie
// 无效时 emit 事件触发弹窗
onMounted(async () => {
  const result = await checkAuth()
  if (!result.valid) {
    emit('auth-required')
  }
})
</script>
```

### QRCodeLogin.vue

```vue
<template>
  <el-dialog v-model="visible" title="扫码登录" width="400px">
    <div class="qrcode-container">
      <!-- 二维码图片 -->
      <img v-if="qrcodeUrl" :src="qrcodeUrl" />

      <!-- 状态遮罩 -->
      <div v-if="status === 'scanned'" class="overlay">
        <el-icon><Check /></el-icon>
        <span>扫码成功，请在手机上确认</span>
      </div>

      <div v-if="status === 'expired'" class="overlay">
        <el-button @click="refreshQrcode">刷新二维码</el-button>
      </div>
    </div>

    <div class="status-text">{{ statusText }}</div>
  </el-dialog>
</template>
```

## Risks / Trade-offs

### 风险 1：抖音 API 变更
- **风险**：抖音可能修改 SSO API 参数或签名算法
- **缓解**：模块化设计，签名逻辑独立，便于更新

### 风险 2：频率限制
- **风险**：频繁请求可能触发风控
- **缓解**：添加请求间隔限制，前端显示友好提示

### 风险 3：Cookie 有效期短
- **风险**：Cookie 可能在几小时内过期
- **缓解**：前端定期检测，过期时主动提示重新登录

### Trade-off：轮询 vs WebSocket
- **选择轮询**：实现简单，无需额外基础设施
- **代价**：略有延迟，服务器压力稍大
- **可接受**：扫码登录是低频操作

## Migration Plan

1. **Phase 1**：实现后端扫码登录 API
2. **Phase 2**：实现前端组件
3. **Phase 3**：集成到主应用
4. **Rollback**：如遇问题，用户仍可使用手动 Cookie 配置

## Open Questions

1. **是否需要支持终端二维码显示？**
   - 当前设计仅支持 Web 前端
   - 可后续添加 CLI 扫码登录支持

2. **Cookie 刷新策略？**
   - 当前设计：过期后重新扫码
   - 可考虑：定时检测 + 主动提醒

3. **多实例部署时 Cookie 同步？**
   - 当前设计：单实例，Cookie 存本地
   - 如需多实例，需考虑共享存储
