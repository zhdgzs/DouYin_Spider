<template>
  <el-dialog
    v-model="visible"
    title="登录"
    width="450px"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    @close="handleClose"
  >
    <!-- 标签页切换 -->
    <el-tabs v-model="activeTab">
      <el-tab-pane label="扫码登录" name="qrcode">
        <div class="qrcode-container">
          <!-- 加载状态 -->
          <div v-if="loading" class="loading-wrapper">
            <el-icon class="is-loading" :size="48"><Loading /></el-icon>
            <p>正在获取二维码...</p>
          </div>

          <!-- 二维码显示 -->
          <div v-else-if="qrcodeBase64" class="qrcode-wrapper">
            <img :src="qrcodeBase64" alt="登录二维码" class="qrcode-image" />

            <!-- 已扫码遮罩 -->
            <div v-if="status === QRCodeStatusCode.SCANNED" class="overlay scanned">
              <el-icon :size="48" color="#67c23a"><CircleCheck /></el-icon>
              <span>扫码成功</span>
            </div>

            <!-- 过期遮罩 -->
            <div v-if="status === QRCodeStatusCode.EXPIRED" class="overlay expired">
              <el-button type="primary" @click="refreshQrcode">
                <el-icon><Refresh /></el-icon>
                刷新二维码
              </el-button>
            </div>
          </div>

          <!-- 错误状态 -->
          <div v-else-if="errorMessage" class="error-wrapper">
            <el-icon :size="48" color="#f56c6c"><CircleClose /></el-icon>
            <p>{{ errorMessage }}</p>
            <el-button type="primary" @click="refreshQrcode">重试</el-button>
          </div>
        </div>

        <!-- 状态文案 -->
        <div class="status-text">
          <el-icon v-if="status === QRCodeStatusCode.WAITING" class="is-loading"><Loading /></el-icon>
          <span>{{ statusText }}</span>
        </div>

        <!-- 提示信息 -->
        <div class="tips">
          <p>请使用抖音 App 扫描二维码登录</p>
          <p class="sub-tip">如果扫码登录不可用，请切换到"手动输入"标签</p>
        </div>
      </el-tab-pane>

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
    </el-tabs>
  </el-dialog>
</template>

<script setup lang="ts">
/**
 * 扫码登录弹窗组件
 */
import { ref, computed, watch, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading, CircleCheck, CircleClose, Refresh } from '@element-plus/icons-vue'
import { getQRCode, checkQRCodeStatus, setCookie } from '../api/auth'
import { QRCodeStatusCode } from '../types/auth'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'login-success'): void
}>()

// 状态
const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const activeTab = ref('qrcode')
const loading = ref(false)
const qrcodeBase64 = ref('')
const token = ref('')
const status = ref<QRCodeStatusCode>(QRCodeStatusCode.WAITING)
const errorMessage = ref('')

// 手动输入
const manualCookie = ref('')
const submitting = ref(false)

// 轮询定时器
let pollTimer: ReturnType<typeof setInterval> | null = null

// 状态文案
const statusText = computed(() => {
  switch (status.value) {
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

// 获取二维码
async function fetchQRCode() {
  loading.value = true
  errorMessage.value = ''
  qrcodeBase64.value = ''
  status.value = QRCodeStatusCode.WAITING

  try {
    const result = await getQRCode()

    if (result.success && result.data) {
      qrcodeBase64.value = result.data.qrcode_base64
      token.value = result.data.token
      startPolling()
    } else {
      errorMessage.value = result.error || '获取二维码失败'
    }
  } catch (err: unknown) {
    const error = err as Error
    errorMessage.value = error.message || '网络请求失败'
  } finally {
    loading.value = false
  }
}

// 刷新二维码
function refreshQrcode() {
  stopPolling()
  fetchQRCode()
}

// 开始轮询
function startPolling() {
  stopPolling()

  pollTimer = setInterval(async () => {
    if (!token.value) return

    try {
      const result = await checkQRCodeStatus(token.value)
      status.value = result.status

      // 登录成功
      if (result.status === QRCodeStatusCode.CONFIRMED) {
        stopPolling()
        ElMessage.success('登录成功！')
        emit('login-success')
        visible.value = false
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
      // 轮询失败不中断，继续重试
      console.error('轮询状态失败:', err)
    }
  }, 3000) // 3 秒间隔
}

// 停止轮询
function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

// 提交手动 Cookie
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
      emit('login-success')
      visible.value = false
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

// 关闭弹窗
function handleClose() {
  stopPolling()
  manualCookie.value = ''
}

// 监听弹窗显示
watch(visible, (val) => {
  if (val && activeTab.value === 'qrcode') {
    fetchQRCode()
  } else {
    stopPolling()
  }
})

// 监听标签切换
watch(activeTab, (val) => {
  if (val === 'qrcode' && visible.value && !qrcodeBase64.value) {
    fetchQRCode()
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
.qrcode-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 260px;
}

.loading-wrapper,
.error-wrapper {
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

.status-text {
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
</style>
