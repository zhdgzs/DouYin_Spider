<template>
  <div class="app-container">
    <!-- 认证检测（静默检测，不强制弹框） -->
    <AuthChecker
      @auth-success="handleAuthSuccess"
      @auth-required="handleAuthRequired"
    />

    <!-- Cookie 管理弹窗 -->
    <CookieManager
      v-model="showCookieManager"
      @cookie-updated="handleCookieUpdated"
    />

    <el-container>
      <el-header>
        <div class="header-content">
          <h1>🎵 抖音视频解析工具</h1>
          <!-- 用户信息/Cookie 状态 -->
          <div class="header-right">
            <template v-if="userInfo">
              <div class="user-info" @click="showCookieManager = true">
                <el-avatar v-if="userInfo.avatar" :src="userInfo.avatar" :size="32" />
                <el-avatar v-else :size="32" icon="User" />
                <span class="nickname">{{ userInfo.nickname || `UID: ${userInfo.uid}` }}</span>
              </div>
            </template>
            <template v-else>
              <el-button
                :type="cookieInvalid ? 'danger' : 'primary'"
                text
                @click="showCookieManager = true"
              >
                <el-icon v-if="cookieInvalid" style="margin-right: 4px"><Warning /></el-icon>
                {{ cookieInvalid ? 'Cookie 无效' : 'Cookie 管理' }}
              </el-button>
            </template>
          </div>
        </div>
      </el-header>

      <el-main>
        <div class="main-content">
          <!-- Cookie 无效提示（非阻塞） -->
          <el-alert
            v-if="cookieInvalid && !userInfo"
            title="Cookie 无效或未设置"
            description="部分功能可能受限，点击右上角「Cookie 管理」更新 Cookie"
            type="warning"
            show-icon
            :closable="true"
            @close="cookieInvalid = false"
            style="margin-bottom: 24px"
          />

          <!-- 链接输入 -->
          <VideoInput :loading="loading" @parse="handleParse" />

          <!-- 错误提示 -->
          <el-alert
            v-if="errorMessage"
            :title="errorMessage"
            type="error"
            show-icon
            closable
            @close="errorMessage = ''"
            style="margin-bottom: 24px"
          />

          <!-- 视频信息 -->
          <VideoInfo :info="videoInfo" />

          <!-- 清晰度列表 -->
          <QualityList
            :qualities="videoInfo?.video_urls || []"
            @select="handleQualitySelect"
          />

          <!-- 视频预览 -->
          <VideoPlayer
            :video-url="selectedVideoUrl"
            :current-quality="selectedQuality?.quality"
          />
        </div>
      </el-main>

      <el-footer>
        <div class="footer-content">
          <span>仅供学习研究使用，请遵守相关法律法规</span>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Warning, User } from '@element-plus/icons-vue'
import VideoInput from './components/VideoInput.vue'
import VideoInfo from './components/VideoInfo.vue'
import QualityList from './components/QualityList.vue'
import VideoPlayer from './components/VideoPlayer.vue'
import AuthChecker from './components/AuthChecker.vue'
import CookieManager from './components/CookieManager.vue'
import { parseVideo } from './api/video'
import type { VideoInfo as VideoInfoType, VideoQuality } from './types/video'
import type { UserInfo } from './types/auth'

const loading = ref(false)
const errorMessage = ref('')
const videoInfo = ref<VideoInfoType | null>(null)
const selectedQuality = ref<VideoQuality | null>(null)
const selectedVideoUrl = ref('')

// 认证状态
const showCookieManager = ref(false)
const userInfo = ref<UserInfo | null>(null)
const cookieInvalid = ref(false)

// 认证成功
function handleAuthSuccess(info: UserInfo) {
  userInfo.value = info
  cookieInvalid.value = false
}

// 需要认证（不自动弹框，只标记状态）
function handleAuthRequired() {
  cookieInvalid.value = true
  // 不再自动弹出登录框
  // showCookieManager.value = true
}

// Cookie 更新后刷新认证状态
function handleCookieUpdated() {
  // 刷新页面以重新检测认证状态
  window.location.reload()
}

async function handleParse(url: string) {
  loading.value = true
  errorMessage.value = ''
  videoInfo.value = null
  selectedQuality.value = null
  selectedVideoUrl.value = ''

  try {
    const response = await parseVideo(url)

    if (response.success && response.data) {
      videoInfo.value = response.data
      ElMessage.success('解析成功')
    } else {
      errorMessage.value = response.message || '解析失败'
    }
  } catch (err: unknown) {
    const error = err as Error
    errorMessage.value = error.message || '网络请求失败，请检查后端服务是否启动'
  } finally {
    loading.value = false
  }
}

function handleQualitySelect(quality: VideoQuality) {
  selectedQuality.value = quality
  selectedVideoUrl.value = quality.url
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 900px;
  padding: 0 24px;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 20px;
  transition: background-color 0.2s;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-info .nickname {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.el-main {
  padding: 24px;
}

.main-content {
  max-width: 900px;
  margin: 0 auto;
}

.el-footer {
  background: #f5f7fa;
  text-align: center;
  color: #909399;
  font-size: 13px;
  padding: 20px;
}
</style>
