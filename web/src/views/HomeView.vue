<template>
  <div class="home-view">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>🎵 视频解析</span>
          <span class="subtitle">输入抖音视频链接，获取无水印视频</span>
        </div>
      </template>

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

      <!-- 视频预览与清晰度选择 -->
      <VideoPreviewPanel
        :qualities="videoInfo?.video_urls || []"
        :video-title="videoInfo?.title"
        @select="handleQualitySelect"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import VideoInput from '../components/VideoInput.vue'
import VideoInfo from '../components/VideoInfo.vue'
import VideoPreviewPanel from '../components/VideoPreviewPanel.vue'
import { parseVideo } from '../api/video'
import type { VideoInfo as VideoInfoType, VideoQuality } from '../types/video'

const loading = ref(false)
const errorMessage = ref('')
const videoInfo = ref<VideoInfoType | null>(null)

async function handleParse(url: string) {
  loading.value = true
  errorMessage.value = ''
  videoInfo.value = null

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

function handleQualitySelect(_quality: VideoQuality) {
  // 清晰度选择由 VideoPreviewPanel 内部处理
}
</script>

<style scoped>
.home-view {
  max-width: 900px;
  margin: 0 auto;
}

.page-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-header span:first-child {
  font-size: 18px;
  font-weight: 600;
}

.card-header .subtitle {
  font-size: 13px;
  color: #909399;
}
</style>
