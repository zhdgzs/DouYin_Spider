<template>
  <el-dialog
    v-model="visible"
    title="Cookie 管理"
    width="500px"
    :close-on-click-modal="true"
    :close-on-press-escape="true"
    @open="handleOpen"
    @close="handleClose"
  >
    <!-- 标签页切换 -->
    <el-tabs v-model="activeTab">
      <!-- Cookie 状态 Tab -->
      <el-tab-pane label="Cookie 状态" name="status">
        <div class="status-container">
          <!-- 加载状态 -->
          <div v-if="checkingStatus" class="loading-wrapper">
            <el-icon class="is-loading" :size="32"><Loading /></el-icon>
            <p>正在检测 Cookie 状态...</p>
          </div>

          <!-- Cookie 状态展示 -->
          <template v-else>
            <!-- 有效状态 -->
            <div v-if="cookieValid" class="status-card valid">
              <div class="status-header">
                <el-icon :size="24" color="#67c23a"><CircleCheck /></el-icon>
                <span class="status-title">Cookie 有效</span>
              </div>
              <div v-if="userInfo" class="user-info-card">
                <el-avatar v-if="userInfo.avatar" :src="userInfo.avatar" :size="48" />
                <el-avatar v-else :size="48" icon="User" />
                <div class="user-details">
                  <span class="nickname">{{ userInfo.nickname || '抖音用户' }}</span>
                  <span class="uid">UID: {{ userInfo.uid }}</span>
                </div>
              </div>
            </div>

            <!-- 无效状态 -->
            <div v-else class="status-card invalid">
              <div class="status-header">
                <el-icon :size="24" color="#f56c6c"><CircleClose /></el-icon>
                <span class="status-title">Cookie 无效或不存在</span>
              </div>
              <p class="status-message">{{ statusError || '请切换到其他标签页更新 Cookie' }}</p>
            </div>

            <!-- Cookie 值展示 -->
            <div v-if="currentCookie" class="cookie-display">
              <div class="cookie-header">
                <span>当前 Cookie</span>
                <el-button type="primary" link size="small" @click="copyCookie">
                  <el-icon><CopyDocument /></el-icon>
                  复制
                </el-button>
              </div>
              <div class="cookie-value">
                <code>{{ currentCookie }}</code>
              </div>
              <div class="cookie-meta">
                <span>长度: {{ cookieLength }} 字符</span>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="action-buttons">
              <el-button @click="recheckStatus" :loading="checkingStatus">
                <el-icon><Refresh /></el-icon>
                重新检测
              </el-button>
            </div>
          </template>
        </div>
      </el-tab-pane>

      <!-- 手动输入 Tab -->
      <el-tab-pane label="手动输入" name="manual">
        <div class="manual-container">
          <el-alert
            title="获取 Cookie 方法"
            type="info"
            :closable="false"
            style="margin-bottom: 16px"
          >
            <ol class="cookie-steps">
              <li>打开浏览器访问 <a href="https://www.douyin.com" target="_blank">www.douyin.com</a></li>
              <li>登录你的抖音账号</li>
              <li>按 F12 打开开发者工具</li>
              <li>切换到 Network（网络）标签</li>
              <li>刷新页面，点击任意请求</li>
              <li>在 Request Headers 中找到 Cookie</li>
              <li>复制完整的 Cookie 值粘贴到下方</li>
            </ol>
          </el-alert>

          <el-input
            v-model="manualCookie"
            type="textarea"
            :rows="5"
            placeholder="请粘贴 Cookie 值..."
            style="margin-bottom: 16px"
          />

          <el-button
            type="primary"
            :loading="submitting"
            :disabled="!manualCookie.trim()"
            @click="submitCookie"
            style="width: 100%"
          >
            保存 Cookie
          </el-button>
        </div>
      </el-tab-pane>

      <!-- 扫码登录 Tab -->
      <el-tab-pane label="扫码登录" name="qrcode">
        <div class="qrcode-container">
          <!-- 加载状态 -->
          <div v-if="qrcodeLoading" class="loading-wrapper">
            <el-icon class="is-loading" :size="48"><Loading /></el-icon>
            <p>正在获取二维码...</p>
          </div>

          <!-- 二维码显示 -->
          <div v-else-if="qrcodeBase64" class="qrcode-wrapper">
            <img :src="qrcodeBase64" alt="登录二维码" class="qrcode-image" />

            <!-- 已扫码遮罩 -->
            <div v-if="qrcodeStatus === QRCodeStatusCode.SCANNED" class="overlay scanned">
              <el-icon :size="48" color="#67c23a"><CircleCheck /></el-icon>
              <span>扫码成功</span>
            </div>

            <!-- 过期遮罩 -->
            <div v-if="qrcodeStatus === QRCodeStatusCode.EXPIRED" class="overlay expired">
              <el-button type="primary" @click="refreshQrcode">
                <el-icon><Refresh /></el-icon>
                刷新二维码
              </el-button>
            </div>
          </div>

          <!-- 错误状态 -->
          <div v-else-if="qrcodeError" class="error-wrapper">
            <el-icon :size="48" color="#f56c6c"><CircleClose /></el-icon>
            <p>{{ qrcodeError }}</p>
            <el-button type="primary" @click="refreshQrcode">重试</el-button>
          </div>

          <!-- 未开始状态 -->
          <div v-else class="start-wrapper">
            <el-button type="primary" @click="fetchQRCode">
              <el-icon><VideoCamera /></el-icon>
              获取二维码
            </el-button>
          </div>
        </div>

        <!-- 状态文案 -->
        <div v-if="qrcodeBase64" class="qrcode-status-text">
          <el-icon v-if="qrcodeStatus === QRCodeStatusCode.WAITING" class="is-loading"><Loading /></el-icon>
          <span>{{ qrcodeStatusText }}</span>
        </div>

        <!-- 提示信息 -->
        <div class="tips">
          <p>请使用抖音 App 扫描二维码登录</p>
          <p class="sub-tip">如果扫码登录不可用，请切换到"手动输入"标签</p>
        </div>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
</template>

<script setup lang="ts">
/**
 * Cookie 管理弹窗组件
 * 提供 Cookie 状态查看、手动输入、扫码登录三种方式
 */
import { ref, computed, watch, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading, CircleCheck, CircleClose, Refresh, CopyDocument, VideoCamera, User } from '@element-plus/icons-vue'
import { checkAuth, getCookie, setCookie, getQRCode, checkQRCodeStatus } from '../api/auth'
import { QRCodeStatusCode } from '../types/auth'
import type { UserInfo } from '../types/auth'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'cookie-updated'): void
}>()

// 弹窗可见性
const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// 当前激活的 Tab
const activeTab = ref('status')

// ========== Cookie 状态相关 ==========
const checkingStatus = ref(false)
const cookieValid = ref(false)
const userInfo = ref<UserInfo | null>(null)
const statusError = ref('')
const currentCookie = ref('')
const cookieLength = ref(0)

// ========== 手动输入相关 ==========
const manualCookie = ref('')
const submitting = ref(false)

// ========== 扫码登录相关 ==========
const qrcodeLoading = ref(false)
const qrcodeBase64 = ref('')
const qrcodeToken = ref('')
const qrcodeStatus = ref<QRCodeStatusCode>(QRCodeStatusCode.WAITING)
const qrcodeError = ref('')
let pollTimer: ReturnType<typeof setInterval> | null = null

// 扫码状态文案
const qrcodeStatusText = computed(() => {
  switch (qrcodeStatus.value) {
    case QRCodeStatusCode.WAITING:
      return '等待扫码...'
    case QRCodeStatusCode.SCANNED:
      return '扫码成功，请在手机上确认登录'
    case QRCodeStatusCode.CONFIRMED:
      return '登录成功！'
    case QRCodeStatusCode.RATE_LIMITED:
      return '请求过于频繁，请稍后重试'
    case QRCodeStatusCode.EXPIRED:
      return '二维码已过期，请刷新'
    default:
      return ''
  }
})

// ========== Cookie 状态检测 ==========
async function checkCookieStatus() {
  checkingStatus.value = true
  statusError.value = ''

  try {
    // 并行获取 Cookie 值和验证状态
    const [cookieResult, authResult] = await Promise.all([
      getCookie(),
      checkAuth()
    ])

    // 更新 Cookie 显示
    if (cookieResult.success && cookieResult.cookie) {
      currentCookie.value = cookieResult.cookie
      cookieLength.value = cookieResult.length || 0
    } else {
      currentCookie.value = ''
      cookieLength.value = 0
    }

    // 更新验证状态
    if (authResult.valid && authResult.user_info) {
      cookieValid.value = true
      userInfo.value = authResult.user_info
    } else {
      cookieValid.value = false
      userInfo.value = null
      statusError.value = authResult.error || 'Cookie 无效或已过期'
    }
  } catch (err: unknown) {
    const error = err as Error
    cookieValid.value = false
    statusError.value = error.message || '检测失败'
  } finally {
    checkingStatus.value = false
  }
}

// 重新检测
function recheckStatus() {
  checkCookieStatus()
}

// 复制 Cookie
async function copyCookie() {
  try {
    const result = await getCookie()
    if (result.success && result.raw_cookie) {
      await navigator.clipboard.writeText(result.raw_cookie)
      ElMessage.success('Cookie 已复制到剪贴板')
    } else {
      ElMessage.warning('没有可复制的 Cookie')
    }
  } catch {
    ElMessage.error('复制失败')
  }
}

// ========== 手动输入 ==========
async function submitCookie() {
  if (!manualCookie.value.trim()) {
    ElMessage.warning('请输入 Cookie')
    return
  }

  submitting.value = true

  try {
    const result = await setCookie(manualCookie.value.trim())

    if (result.success) {
      if (result.warning) {
        ElMessage.warning(result.warning)
      } else {
        ElMessage.success(result.message || 'Cookie 设置成功')
      }
      manualCookie.value = ''
      // 切换到状态 Tab 并刷新
      activeTab.value = 'status'
      await checkCookieStatus()
      emit('cookie-updated')
    } else {
      ElMessage.error(result.error || '设置失败')
    }
  } catch (err: unknown) {
    const error = err as Error
    ElMessage.error(error.message || '网络请求失败')
  } finally {
    submitting.value = false
  }
}

// ========== 扫码登录 ==========
async function fetchQRCode() {
  qrcodeLoading.value = true
  qrcodeError.value = ''
  qrcodeBase64.value = ''
  qrcodeStatus.value = QRCodeStatusCode.WAITING

  try {
    const result = await getQRCode()

    if (result.success && result.data) {
      qrcodeBase64.value = result.data.qrcode_base64
      qrcodeToken.value = result.data.token
      startPolling()
    } else {
      qrcodeError.value = result.error || '获取二维码失败'
    }
  } catch (err: unknown) {
    const error = err as Error
    qrcodeError.value = error.message || '网络请求失败'
  } finally {
    qrcodeLoading.value = false
  }
}

function refreshQrcode() {
  stopPolling()
  fetchQRCode()
}

function startPolling() {
  stopPolling()

  pollTimer = setInterval(async () => {
    if (!qrcodeToken.value) return

    try {
      const result = await checkQRCodeStatus(qrcodeToken.value)
      qrcodeStatus.value = result.status

      // 登录成功
      if (result.status === QRCodeStatusCode.CONFIRMED) {
        stopPolling()
        ElMessage.success('登录成功！')
        // 切换到状态 Tab 并刷新
        activeTab.value = 'status'
        await checkCookieStatus()
        emit('cookie-updated')
      }

      // 二维码过期
      if (result.status === QRCodeStatusCode.EXPIRED) {
        stopPolling()
      }

      // 访问频繁
      if (result.status === QRCodeStatusCode.RATE_LIMITED) {
        stopPolling()
        ElMessage.warning('请求过于频繁，请稍后重试')
      }
    } catch (err) {
      console.error('轮询状态失败:', err)
    }
  }, 3000)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

// ========== 生命周期 ==========
function handleOpen() {
  // 打开弹窗时检测 Cookie 状态
  checkCookieStatus()
}

function handleClose() {
  stopPolling()
  manualCookie.value = ''
  qrcodeBase64.value = ''
  qrcodeError.value = ''
}

// 监听 Tab 切换
watch(activeTab, (val) => {
  if (val === 'qrcode') {
    // 切换到扫码 Tab 时不自动获取二维码，让用户手动点击
    stopPolling()
  } else if (val === 'status') {
    stopPolling()
  } else if (val === 'manual') {
    stopPolling()
  }
})

// 组件卸载时清理
onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.status-container {
  min-height: 200px;
}

.loading-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  min-height: 200px;
  color: #909399;
}

.status-card {
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.status-card.valid {
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
}

.status-card.invalid {
  background: #fef0f0;
  border: 1px solid #fde2e2;
}

.status-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.status-title {
  font-size: 16px;
  font-weight: 500;
}

.status-card.valid .status-title {
  color: #67c23a;
}

.status-card.invalid .status-title {
  color: #f56c6c;
}

.status-message {
  color: #909399;
  font-size: 14px;
  margin: 0;
}

.user-info-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 8px;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-details .nickname {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.user-details .uid {
  font-size: 12px;
  color: #909399;
}

.cookie-display {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.cookie-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}

.cookie-value {
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 8px;
  font-size: 12px;
  word-break: break-all;
  max-height: 80px;
  overflow-y: auto;
}

.cookie-value code {
  color: #606266;
}

.cookie-meta {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.action-buttons {
  display: flex;
  justify-content: center;
}

/* 手动输入样式 */
.manual-container {
  padding: 8px 0;
}

.cookie-steps {
  margin: 8px 0 0 0;
  padding-left: 20px;
  font-size: 12px;
  line-height: 1.8;
}

.cookie-steps a {
  color: #409eff;
  text-decoration: none;
}

.cookie-steps a:hover {
  text-decoration: underline;
}

/* 扫码登录样式 */
.qrcode-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 260px;
}

.error-wrapper,
.start-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: #909399;
}

.qrcode-wrapper {
  position: relative;
  width: 220px;
  height: 220px;
}

.qrcode-image {
  width: 100%;
  height: 100%;
  border: 1px solid #ebeef5;
  border-radius: 8px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 12px;
  border-radius: 8px;
}

.overlay.scanned {
  background: rgba(255, 255, 255, 0.95);
  color: #67c23a;
  font-size: 16px;
  font-weight: 500;
}

.overlay.expired {
  background: rgba(0, 0, 0, 0.7);
}

.qrcode-status-text {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  font-size: 14px;
  color: #606266;
}

.tips {
  text-align: center;
  margin-top: 12px;
  font-size: 12px;
  color: #909399;
}

.tips p {
  margin: 4px 0;
}

.tips .sub-tip {
  color: #c0c4cc;
}
</style>
