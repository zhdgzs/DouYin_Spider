<template>
  <div class="video-preview-panel" v-if="qualities.length > 0">
    <el-card shadow="hover" class="panel-card">
      <template #header>
        <div class="card-header">
          <span>视频预览与下载</span>
          <span class="quality-tag" v-if="selectedQuality">
            {{ selectedQuality.quality }}
            <template v-if="selectedQuality.fps > 0"> · {{ selectedQuality.fps }}fps</template>
          </span>
        </div>
      </template>

      <div class="panel-content">
        <!-- 左侧：视频预览 -->
        <div class="video-section">
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
        </div>

        <!-- 右侧：清晰度列表 -->
        <div class="quality-section">
          <div class="quality-header">
            <el-icon><VideoCamera /></el-icon>
            <span>清晰度选择</span>
          </div>

          <div class="quality-list">
            <div
              v-for="(item, index) in qualities"
              :key="index"
              class="quality-item"
              :class="{ active: item === selectedQuality }"
              @click="handleSelect(item)"
            >
              <div class="quality-main">
                <div class="quality-label">
                  <el-icon v-if="item === selectedQuality" class="play-icon"><VideoPlay /></el-icon>
                  <span class="quality-name">{{ item.quality }}</span>
                  <el-tag v-if="item.fps >= 60" size="small" type="warning" effect="plain">高帧率</el-tag>
                </div>
                <div class="quality-meta">
                  <span class="resolution">{{ item.width }}×{{ item.height }}</span>
                  <span v-if="item.fps > 0" class="fps">{{ item.fps }}fps</span>
                </div>
              </div>

              <div class="quality-info">
                <div class="file-size">{{ item.file_size_str || '未知' }}</div>
                <div v-if="item.bitrate_str && item.bitrate_str !== '未知'" class="bitrate">
                  {{ item.bitrate_str }}
                </div>
              </div>

              <el-button
                class="download-btn"
                size="small"
                type="primary"
                :icon="Download"
                circle
                @click.stop="handleDownload(item)"
              />
            </div>
          </div>

          <div class="quality-tip">
            <el-icon><InfoFilled /></el-icon>
            <span>点击切换清晰度预览，点击按钮下载</span>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { Loading, WarningFilled, VideoPlay, Download, InfoFilled, VideoCamera } from '@element-plus/icons-vue'
import type { VideoQuality } from '../types/video'
import { getProxyUrl, getDownloadUrl } from '../api/video'

const props = defineProps<{
  qualities: VideoQuality[]
  videoTitle?: string
}>()

const emit = defineEmits<{
  (e: 'select', quality: VideoQuality): void
}>()

const videoRef = ref<HTMLVideoElement | null>(null)
const loading = ref(false)
const error = ref('')
const currentTime = ref(0)
const selectedQuality = ref<VideoQuality | null>(null)

// 使用代理 URL 绕过防盗链
const proxyUrl = computed(() => {
  if (!selectedQuality.value?.url) return ''
  return getProxyUrl(selectedQuality.value.url)
})

// 当清晰度列表变化时，默认选中最高清晰度
watch(() => props.qualities, (newQualities) => {
  if (newQualities.length > 0) {
    selectedQuality.value = newQualities[0]
    emit('select', newQualities[0])
  }
}, { immediate: true })

// 监听选中清晰度变化，切换视频源
watch(() => selectedQuality.value, async (newQuality, oldQuality) => {
  if (newQuality && newQuality !== oldQuality) {
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

function handleSelect(quality: VideoQuality) {
  selectedQuality.value = quality
  emit('select', quality)
}

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

function handleDownload(quality: VideoQuality) {
  const title = props.videoTitle || 'video'
  // 文件名包含帧率信息（如果有）
  const fpsLabel = quality.fps > 0 ? `_${quality.fps}fps` : ''
  const filename = `${title}_${quality.quality}${fpsLabel}.mp4`
  const downloadUrl = getDownloadUrl(quality.url, filename)
  window.open(downloadUrl, '_blank')
}
</script>

<style scoped>
.video-preview-panel {
  margin-bottom: 24px;
}

.panel-card {
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: bold;
}

.quality-tag {
  font-size: 12px;
  padding: 2px 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  font-weight: normal;
}

.panel-content {
  display: flex;
  gap: 20px;
  min-height: 300px;
}

/* 左侧视频区域 */
.video-section {
  flex: 1;
  min-width: 0;
}

.player-container {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 16 / 9;
}

video {
  width: 100%;
  height: 100%;
  object-fit: contain;
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

/* 右侧清晰度列表 */
.quality-section {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.quality-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.quality-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quality-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #f5f7fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.quality-item:hover {
  background: #ecf5ff;
  border-color: #c6e2ff;
}

.quality-item.active {
  background: #ecf5ff;
  border-color: #409eff;
}

.quality-main {
  flex: 1;
  min-width: 0;
}

.quality-label {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.play-icon {
  color: #409eff;
  font-size: 14px;
}

.quality-name {
  font-weight: 600;
  font-size: 14px;
  color: #303133;
}

.quality-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #909399;
}

.resolution {
  font-family: monospace;
}

.fps {
  color: #e6a23c;
}

.quality-info {
  text-align: right;
  flex-shrink: 0;
}

.file-size {
  font-size: 13px;
  font-weight: 500;
  color: #606266;
}

.bitrate {
  font-size: 11px;
  color: #909399;
  margin-top: 2px;
}

.download-btn {
  flex-shrink: 0;
}

.quality-tip {
  margin-top: 12px;
  padding: 8px 10px;
  background: #f4f4f5;
  border-radius: 6px;
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 响应式：小屏幕时改为上下布局 */
@media (max-width: 768px) {
  .panel-content {
    flex-direction: column;
  }

  .quality-section {
    width: 100%;
  }

  .quality-list {
    max-height: 200px;
  }
}
</style>
