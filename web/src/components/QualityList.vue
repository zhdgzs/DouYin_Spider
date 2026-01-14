<template>
  <div class="quality-list" v-if="qualities.length > 0">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>清晰度选择（点击切换预览）</span>
        </div>
      </template>

      <el-table
        :data="qualities"
        :row-class-name="getRowClassName"
        @row-click="handleRowClick"
        style="width: 100%"
        highlight-current-row
      >
        <el-table-column label="清晰度" width="100">
          <template #default="{ row }">
            <span class="quality-badge" :class="{ active: row === selectedQuality }">
              <el-icon v-if="row === selectedQuality"><VideoPlay /></el-icon>
              {{ row.quality }}
            </span>
          </template>
        </el-table-column>

        <el-table-column label="分辨率" width="120">
          <template #default="{ row }">
            {{ row.width }} × {{ row.height }}
          </template>
        </el-table-column>

        <el-table-column label="文件大小" width="120">
          <template #default="{ row }">
            {{ row.file_size_str || '未知' }}
          </template>
        </el-table-column>

        <el-table-column label="操作" min-width="120">
          <template #default="{ row }">
              <el-button size="small" type="primary" @click.stop="handleDownload(row)">
                <el-icon><Download /></el-icon>
                下载
              </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="tip">
        <el-icon><InfoFilled /></el-icon>
        点击行可切换预览清晰度，当前预览: {{ selectedQuality?.quality || '无' }}
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { VideoPlay, Download, InfoFilled } from '@element-plus/icons-vue'
import type { VideoQuality } from '../types/video'
import { getDownloadUrl } from '../api/video'

const props = defineProps<{
  qualities: VideoQuality[]
  videoTitle?: string
}>()

const emit = defineEmits<{
  (e: 'select', quality: VideoQuality): void
}>()

const selectedQuality = ref<VideoQuality | null>(null)

// 当清晰度列表变化时，默认选中最高清晰度
watch(() => props.qualities, (newQualities) => {
  if (newQualities.length > 0) {
    selectedQuality.value = newQualities[0]
    emit('select', newQualities[0])
  }
}, { immediate: true })

function getRowClassName({ row }: { row: VideoQuality }) {
  return row === selectedQuality.value ? 'selected-row' : ''
}

function handleRowClick(row: VideoQuality) {
  selectedQuality.value = row
  emit('select', row)
}

function handleDownload(row: VideoQuality) {
  // 生成文件名：视频标题_清晰度.mp4
  const title = props.videoTitle || 'video'
  const filename = `${title}_${row.quality}.mp4`
  const downloadUrl = getDownloadUrl(row.url, filename)
  window.open(downloadUrl, '_blank')
}
</script>

<style scoped>
.quality-list {
  margin-bottom: 24px;
}

.card-header {
  font-weight: bold;
}

.quality-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 4px;
  background: #f0f2f5;
  cursor: pointer;
  transition: all 0.3s;
}

.quality-badge.active {
  background: #409eff;
  color: white;
}

:deep(.selected-row) {
  background-color: #ecf5ff !important;
}

:deep(.el-table__row) {
  cursor: pointer;
}

:deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.tip {
  margin-top: 12px;
  padding: 8px 12px;
  background: #f4f4f5;
  border-radius: 4px;
  font-size: 13px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
