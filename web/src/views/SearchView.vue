<template>
  <div class="search-view">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>🔍 搜索中心</span>
          <span class="subtitle">搜索抖音作品、用户、直播</span>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form @submit.prevent="handleSearch">
        <el-form-item>
          <el-input
            v-model="keyword"
            placeholder="请输入搜索关键词"
            size="large"
            clearable
          >
            <template #append>
              <el-button type="primary" :loading="loading" @click="handleSearch">
                搜索
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>

      <!-- 搜索类型切换 -->
      <el-tabs v-model="searchType" @tab-change="handleTabChange">
        <el-tab-pane label="作品" name="works" />
        <el-tab-pane label="用户" name="users" />
        <el-tab-pane label="直播" name="lives" />
      </el-tabs>

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

    <!-- 作品搜索结果 -->
    <el-card v-if="searchType === 'works' && workResults.length > 0" class="page-card">
      <div class="works-grid">
        <div v-for="work in workResults" :key="work.aweme_id" class="work-item">
          <div class="work-cover">
            <el-image :src="work.cover" fit="cover" lazy>
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>
          <div class="work-info">
            <div class="work-desc">{{ work.desc || '无描述' }}</div>
            <div class="work-author">
              <el-avatar :src="work.author_avatar" :size="20" />
              <span>{{ work.author_nickname }}</span>
            </div>
            <div class="work-stats">
              <span>❤️ {{ formatNumber(work.digg_count) }}</span>
              <span>💬 {{ formatNumber(work.comment_count) }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 用户搜索结果 -->
    <el-card v-if="searchType === 'users' && userResults.length > 0" class="page-card">
      <div class="users-list">
        <div v-for="user in userResults" :key="user.uid" class="user-item">
          <el-avatar :src="user.avatar" :size="60" />
          <div class="user-info">
            <div class="user-name">
              <span class="nickname">{{ user.nickname }}</span>
              <el-tag v-if="user.custom_verify" type="primary" size="small">
                {{ user.custom_verify }}
              </el-tag>
            </div>
            <div class="user-id">抖音号: {{ user.unique_id || user.uid }}</div>
            <div class="user-signature">{{ user.signature || '暂无签名' }}</div>
            <div class="user-stats">
              <span>粉丝 {{ formatNumber(user.follower_count) }}</span>
              <span>作品 {{ user.aweme_count }}</span>
              <span>获赞 {{ formatNumber(user.total_favorited) }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 直播搜索结果 -->
    <el-card v-if="searchType === 'lives' && liveResults.length > 0" class="page-card">
      <div class="lives-grid">
        <div v-for="live in liveResults" :key="live.room_id" class="live-item">
          <div class="live-cover">
            <el-image :src="live.cover" fit="cover" lazy>
              <template #error>
                <div class="image-error">
                  <el-icon><VideoCameraFilled /></el-icon>
                </div>
              </template>
            </el-image>
            <div class="live-badge">🔴 直播中</div>
            <div class="live-viewers">{{ formatNumber(live.user_count) }} 观看</div>
          </div>
          <div class="live-info">
            <div class="live-title">{{ live.title || '直播中' }}</div>
            <div class="live-anchor">
              <el-avatar :src="live.anchor_avatar" :size="20" />
              <span>{{ live.anchor_nickname }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 空状态 -->
    <el-card v-if="searched && currentResults.length === 0" class="page-card">
      <el-empty description="暂无搜索结果" />
    </el-card>

    <!-- 加载更多 -->
    <div v-if="hasMore && currentResults.length > 0" class="load-more">
      <el-button :loading="loadingMore" @click="handleLoadMore">
        加载更多
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Picture, VideoCameraFilled } from '@element-plus/icons-vue'
import { searchWorks, searchUsers, searchLives } from '../api/search'
import type { SearchWorkItem, SearchUserItem, SearchLiveItem } from '../types/search'

const keyword = ref('')
const searchType = ref('works')
const loading = ref(false)
const loadingMore = ref(false)
const errorMessage = ref('')
const searched = ref(false)

const workResults = ref<SearchWorkItem[]>([])
const userResults = ref<SearchUserItem[]>([])
const liveResults = ref<SearchLiveItem[]>([])
const cursor = ref('0')
const hasMore = ref(false)

const currentResults = computed(() => {
  switch (searchType.value) {
    case 'works': return workResults.value
    case 'users': return userResults.value
    case 'lives': return liveResults.value
    default: return []
  }
})

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

function clearResults() {
  workResults.value = []
  userResults.value = []
  liveResults.value = []
  cursor.value = '0'
  hasMore.value = false
}

async function handleSearch() {
  if (!keyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  loading.value = true
  errorMessage.value = ''
  clearResults()
  searched.value = true

  try {
    await doSearch()
    ElMessage.success('搜索完成')
  } catch (err: unknown) {
    const error = err as Error
    errorMessage.value = error.message || '搜索失败'
  } finally {
    loading.value = false
  }
}

async function doSearch(append = false) {
  const offset = append ? cursor.value : '0'

  switch (searchType.value) {
    case 'works': {
      const res = await searchWorks(keyword.value, offset)
      if (res.success) {
        if (append) {
          workResults.value.push(...res.data)
        } else {
          workResults.value = res.data
        }
        cursor.value = res.cursor
        hasMore.value = res.has_more
      } else {
        throw new Error(res.message)
      }
      break
    }
    case 'users': {
      const res = await searchUsers(keyword.value, offset)
      if (res.success) {
        if (append) {
          userResults.value.push(...res.data)
        } else {
          userResults.value = res.data
        }
        cursor.value = res.cursor
        hasMore.value = res.has_more
      } else {
        throw new Error(res.message)
      }
      break
    }
    case 'lives': {
      const res = await searchLives(keyword.value, offset)
      if (res.success) {
        if (append) {
          liveResults.value.push(...res.data)
        } else {
          liveResults.value = res.data
        }
        cursor.value = res.cursor
        hasMore.value = res.has_more
      } else {
        throw new Error(res.message)
      }
      break
    }
  }
}

function handleTabChange() {
  if (keyword.value.trim() && searched.value) {
    handleSearch()
  }
}

async function handleLoadMore() {
  if (!hasMore.value || loadingMore.value) return

  loadingMore.value = true
  try {
    await doSearch(true)
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loadingMore.value = false
  }
}
</script>

<style scoped>
.search-view {
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

/* 作品网格 */
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

.work-author {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;
  margin-bottom: 8px;
}

.work-stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

/* 用户列表 */
.users-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.user-info {
  flex: 1;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.nickname {
  font-size: 16px;
  font-weight: 600;
}

.user-id {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.user-signature {
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
}

.user-stats {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #909399;
}

/* 直播网格 */
.lives-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.live-item {
  border-radius: 8px;
  overflow: hidden;
  background: #f5f7fa;
}

.live-cover {
  position: relative;
  aspect-ratio: 16/9;
}

.live-cover .el-image {
  width: 100%;
  height: 100%;
}

.live-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: rgba(255, 0, 0, 0.8);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.live-viewers {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.live-info {
  padding: 12px;
}

.live-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.live-anchor {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;
}

.load-more {
  text-align: center;
  margin-bottom: 24px;
}
</style>
