<template>
  <div class="video-info" v-if="info">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>视频信息</span>
        </div>
      </template>

      <div class="info-content">
        <div class="info-row">
          <div class="cover" v-if="info.cover">
            <el-image :src="info.cover" fit="cover" />
          </div>
          <div class="details">
            <div class="info-item">
              <span class="label">标题:</span>
              <span class="value">{{ info.title || info.desc || '无标题' }}</span>
            </div>
            <div class="info-item">
              <span class="label">作者:</span>
              <span class="value">
                <el-avatar :size="24" :src="info.author.avatar" />
                {{ info.author.nickname }}
              </span>
            </div>
            <div class="info-item stats">
              <span class="stat">
                <el-icon><Star /></el-icon>
                {{ formatNumber(info.statistics.digg_count) }} 点赞
              </span>
              <span class="stat">
                <el-icon><ChatDotRound /></el-icon>
                {{ formatNumber(info.statistics.comment_count) }} 评论
              </span>
              <span class="stat">
                <el-icon><Share /></el-icon>
                {{ formatNumber(info.statistics.share_count) }} 分享
              </span>
              <span class="stat">
                <el-icon><Collection /></el-icon>
                {{ formatNumber(info.statistics.collect_count) }} 收藏
              </span>
            </div>
            <div class="info-item">
              <span class="label">发布时间:</span>
              <span class="value">{{ formatTime(info.create_time) }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { Star, ChatDotRound, Share, Collection } from '@element-plus/icons-vue'
import type { VideoInfo } from '../types/video'

defineProps<{
  info: VideoInfo | null
}>()

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

function formatTime(timestamp: number): string {
  if (!timestamp) return '未知'
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.video-info {
  margin-bottom: 24px;
}

.card-header {
  font-weight: bold;
}

.info-content {
  padding: 8px 0;
}

.info-row {
  display: flex;
  gap: 20px;
}

.cover {
  flex-shrink: 0;
  width: 120px;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
}

.cover .el-image {
  width: 100%;
  height: 100%;
}

.details {
  flex: 1;
}

.info-item {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.label {
  color: #909399;
  flex-shrink: 0;
}

.value {
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stats {
  flex-wrap: wrap;
}

.stat {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-right: 16px;
  color: #606266;
  font-size: 14px;
}
</style>
