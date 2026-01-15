<template>
  <div class="user-view">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>👤 用户分析</span>
          <span class="subtitle">输入用户主页链接，获取用户信息和作品列表</span>
        </div>
      </template>

      <!-- 链接输入 -->
      <el-form @submit.prevent="handleSearch">
        <el-form-item>
          <el-input
            v-model="userUrl"
            placeholder="请输入抖音用户主页链接，如 https://www.douyin.com/user/xxx"
            size="large"
            clearable
          >
            <template #append>
              <el-button type="primary" :loading="loading" @click="handleSearch">
                分析
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>

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
    </el-card>

    <!-- 用户信息卡片 -->
    <el-card v-if="userInfo" class="page-card">
      <div class="user-info-card">
        <el-avatar :src="userInfo.avatar_larger || userInfo.avatar" :size="80" />
        <div class="user-details">
          <div class="user-name">
            <span class="nickname">{{ userInfo.nickname }}</span>
            <el-tag v-if="userInfo.is_verified" type="primary" size="small">
              {{ userInfo.custom_verify || '已认证' }}
            </el-tag>
          </div>
          <div class="user-id">
            抖音号: {{ userInfo.unique_id || userInfo.short_id || userInfo.uid }}
          </div>
          <div class="user-signature">{{ userInfo.signature || '暂无签名' }}</div>
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-value">{{ formatNumber(userInfo.aweme_count) }}</span>
              <span class="stat-label">作品</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ formatNumber(userInfo.follower_count) }}</span>
              <span class="stat-label">粉丝</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ formatNumber(userInfo.following_count) }}</span>
              <span class="stat-label">关注</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ formatNumber(userInfo.total_favorited) }}</span>
              <span class="stat-label">获赞</span>
            </div>
          </div>
          <div v-if="userInfo.ip_location" class="user-location">
            📍 IP属地: {{ userInfo.ip_location }}
          </div>
        </div>
      </div>
    </el-card>

    <!-- 作品列表 -->
    <el-card v-if="userInfo" class="page-card">
      <template #header>
        <div class="works-header">
          <span>作品列表 ({{ works.length }})</span>
          <el-button
            type="primary"
            size="small"
            :loading="loadingAll"
            @click="handleLoadAll"
          >
            加载全部
          </el-button>
        </div>
      </template>

      <div v-if="works.length > 0" class="works-grid">
        <div v-for="work in works" :key="work.aweme_id" class="work-item">
          <div class="work-cover">
            <el-image :src="work.cover" fit="cover" lazy>
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
            <div class="work-duration">{{ formatDuration(work.duration) }}</div>
          </div>
          <div class="work-info">
            <div class="work-desc">{{ work.desc || '无描述' }}</div>
            <div class="work-stats">
              <span>❤️ {{ formatNumber(work.digg_count) }}</span>
              <span>💬 {{ formatNumber(work.comment_count) }}</span>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-else description="暂无作品" />

      <!-- 加载更多 -->
      <div v-if="hasMore && works.length > 0" class="load-more">
        <el-button :loading="loadingMore" @click="handleLoadMore">
          加载更多
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'
import { getUserInfo, getUserWorks, getUserAllWorks } from '../api/user'
import type { UserInfo, WorkItem } from '../types/user'

const userUrl = ref('')
const loading = ref(false)
const loadingMore = ref(false)
const loadingAll = ref(false)
const errorMessage = ref('')
const userInfo = ref<UserInfo | null>(null)
const works = ref<WorkItem[]>([])
const maxCursor = ref('0')
const hasMore = ref(false)

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

function formatDuration(ms: number): string {
  const seconds = Math.floor(ms / 1000)
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

async function handleSearch() {
  if (!userUrl.value) {
    ElMessage.warning('请输入用户主页链接')
    return
  }

  loading.value = true
  errorMessage.value = ''
  userInfo.value = null
  works.value = []
  maxCursor.value = '0'
  hasMore.value = false

  try {
    // 获取用户信息
    const infoRes = await getUserInfo(userUrl.value)
    if (!infoRes.success || !infoRes.data) {
      errorMessage.value = infoRes.message || '获取用户信息失败'
      return
    }
    userInfo.value = infoRes.data

    // 获取作品列表
    const worksRes = await getUserWorks(userUrl.value, '0')
    if (worksRes.success) {
      works.value = worksRes.data
      maxCursor.value = worksRes.max_cursor
      hasMore.value = worksRes.has_more
    }

    ElMessage.success('获取成功')
  } catch (err: unknown) {
    const error = err as Error
    errorMessage.value = error.message || '请求失败'
  } finally {
    loading.value = false
  }
}

async function handleLoadMore() {
  if (!hasMore.value || loadingMore.value) return

  loadingMore.value = true
  try {
    const res = await getUserWorks(userUrl.value, maxCursor.value)
    if (res.success) {
      works.value.push(...res.data)
      maxCursor.value = res.max_cursor
      hasMore.value = res.has_more
    }
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loadingMore.value = false
  }
}

async function handleLoadAll() {
  if (loadingAll.value) return

  loadingAll.value = true
  try {
    const res = await getUserAllWorks(userUrl.value)
    if (res.success) {
      works.value = res.data
      hasMore.value = false
      ElMessage.success(`已加载全部 ${res.total} 个作品`)
    }
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loadingAll.value = false
  }
}
</script>

<style scoped>
.user-view {
  max-width: 1000px;
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

.user-info-card {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.user-details {
  flex: 1;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.nickname {
  font-size: 20px;
  font-weight: 600;
}

.user-id {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.user-signature {
  font-size: 14px;
  color: #606266;
  margin-bottom: 16px;
}

.user-stats {
  display: flex;
  gap: 32px;
  margin-bottom: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.user-location {
  font-size: 13px;
  color: #909399;
}

.works-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.work-item {
  border-radius: 8px;
  overflow: hidden;
  background: #f5f7fa;
}

.work-cover {
  position: relative;
  aspect-ratio: 9/16;
}

.work-cover .el-image {
  width: 100%;
  height: 100%;
}

.work-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.image-error {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #909399;
}

.work-info {
  padding: 12px;
}

.work-desc {
  font-size: 13px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 8px;
}

.work-stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

.load-more {
  text-align: center;
  margin-top: 24px;
}
</style>
