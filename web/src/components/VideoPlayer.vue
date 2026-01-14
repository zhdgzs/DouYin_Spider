<template>
  <div class="video-player" v-if="videoUrl">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>视频预览</span>
          <span class="quality-tag" v-if="currentQuality">{{ currentQuality }}</span>
        </div>
      </template>

      <div class="player-container">
        <video
          ref="videoRef"
          :src="proxyUrl"
          controls
          preload="metadata"
          @error="handleError"
          @loadeddata="handleLoaded"
        >
          您的浏览器不支持视频播放
        </video>

        <div class="loading-overlay" v-if="loading">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>加载中...</span>
        </div>

        <div class="error-overlay" v-if="error">
          <el-icon><WarningFilled /></el-icon>
          <span>{{ error }}</span>
          <el-button size="small" @click="retry">重试</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { Loading, WarningFilled } from '@element-plus/icons-vue'
import { getProxyUrl } from '../api/video'

const props = defineProps<{
  videoUrl: string
  currentQuality?: string
}>()

const videoRef = ref<HTMLVideoElement | null>(null)
const loading = ref(false)
const error = ref('')
const currentTime = ref(0)

// 使用代理 URL 绕过防盗链
const proxyUrl = computed(() => {
  if (!props.videoUrl) return ''
  return getProxyUrl(props.videoUrl)
})

// 监听视频 URL 变化，切换视频源
watch(() => props.videoUrl, async (newUrl, oldUrl) => {
  if (newUrl && newUrl !== oldUrl) {
    // 保存当前播放位置
    if (videoRef.value) {
      currentTime.value = videoRef.value.currentTime
    }

    loading.value = true
    error.value = ''

    await nextTick()

    // 恢复播放位置
    if (videoRef.value && currentTime.value > 0) {
      videoRef.value.currentTime = currentTime.value
    }
  }
})

function handleLoaded() {
  loading.value = false
  // 恢复播放位置
  if (videoRef.value && currentTime.value > 0) {
    videoRef.value.currentTime = currentTime.value
  }
}

function handleError() {
  loading.value = false
  error.value = '视频加载失败，请尝试其他清晰度或直接下载'
}

function retry() {
  error.value = ''
  loading.value = true
  if (videoRef.value) {
    videoRef.value.load()
  }
}
</script>

<style scoped>
.video-player {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: bold;
}

.quality-tag {
  font-size: 12px;
  padding: 2px 8px;
  background: #409eff;
  color: white;
  border-radius: 4px;
  font-weight: normal;
}

.player-container {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

video {
  width: 100%;
  max-height: 500px;
  display: block;
}

.loading-overlay,
.error-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
}

.loading-overlay .el-icon {
  font-size: 32px;
}

.error-overlay .el-icon {
  font-size: 32px;
  color: #f56c6c;
}
</style>
