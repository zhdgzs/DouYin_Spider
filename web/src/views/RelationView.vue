<template>
  <div class="relation-view">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>🔗 关系网络</span>
          <span class="subtitle">查看粉丝、关注列表和通知</span>
        </div>
      </template>

      <!-- 用户信息输入 -->
      <el-form :inline="true" @submit.prevent="handleSearch">
        <el-form-item label="用户ID">
          <el-input v-model="userId" placeholder="用户ID" />
        </el-form-item>
        <el-form-item label="安全ID">
          <el-input v-model="secUid" placeholder="sec_uid" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSearch">
            查询
          </el-button>
        </el-form-item>
      </el-form>

      <el-divider />

      <!-- 通知列表（当前用户） -->
      <div class="notice-section">
        <el-button type="primary" :loading="loadingNotices" @click="handleLoadNotices">
          加载我的通知
        </el-button>
      </div>

      <!-- 错误提示 -->
      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        closable
        @close="errorMessage = ''"
        style="margin-top: 16px"
      />
    </el-card>

    <!-- 粉丝/关注切换 -->
    <el-card v-if="searched" class="page-card">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="粉丝列表" name="followers">
          <div v-if="followers.length > 0" class="users-list">
            <div v-for="user in followers" :key="user.uid" class="user-item">
              <el-avatar :src="user.avatar" :size="50" />
              <div class="user-info">
                <div class="user-name">{{ user.nickname }}</div>
                <div class="user-signature">{{ user.signature || '暂无签名' }}</div>
                <div class="user-stats">
                  <span>粉丝 {{ formatNumber(user.follower_count) }}</span>
                  <span>关注 {{ formatNumber(user.following_count) }}</span>
                  <span>作品 {{ user.aweme_count }}</span>
                </div>
              </div>
              <el-tag v-if="user.is_following" type="success" size="small">已关注</el-tag>
            </div>
          </div>
          <el-empty v-else description="暂无粉丝数据" />
          <div v-if="hasMoreFollowers && followers.length > 0" class="load-more">
            <el-button :loading="loadingMore" @click="handleLoadMoreFollowers">
              加载更多
            </el-button>
          </div>
        </el-tab-pane>

        <el-tab-pane label="关注列表" name="following">
          <div v-if="following.length > 0" class="users-list">
            <div v-for="user in following" :key="user.uid" class="user-item">
              <el-avatar :src="user.avatar" :size="50" />
              <div class="user-info">
                <div class="user-name">{{ user.nickname }}</div>
                <div class="user-signature">{{ user.signature || '暂无签名' }}</div>
                <div class="user-stats">
                  <span>粉丝 {{ formatNumber(user.follower_count) }}</span>
                  <span>关注 {{ formatNumber(user.following_count) }}</span>
                  <span>作品 {{ user.aweme_count }}</span>
                </div>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无关注数据" />
          <div v-if="hasMoreFollowing && following.length > 0" class="load-more">
            <el-button :loading="loadingMore" @click="handleLoadMoreFollowing">
              加载更多
            </el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 通知列表 -->
    <el-card v-if="notices.length > 0" class="page-card">
      <template #header>
        <span>📬 我的通知</span>
      </template>
      <div class="notices-list">
        <div v-for="notice in notices" :key="notice.notice_id" class="notice-item">
          <el-avatar :src="notice.from_user_avatar" :size="40" />
          <div class="notice-content">
            <div class="notice-header">
              <span class="notice-user">{{ notice.from_user_nickname }}</span>
              <span class="notice-time">{{ formatTime(notice.create_time) }}</span>
            </div>
            <div class="notice-text">{{ notice.content }}</div>
          </div>
          <el-image
            v-if="notice.aweme_cover"
            :src="notice.aweme_cover"
            fit="cover"
            class="notice-cover"
          />
        </div>
      </div>
      <div v-if="hasMoreNotices" class="load-more">
        <el-button :loading="loadingMoreNotices" @click="handleLoadMoreNotices">
          加载更多
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getFollowerList, getFollowingList, getNoticeList } from '../api/relation'
import type { RelationUser, NoticeItem } from '../types/relation'

const userId = ref('')
const secUid = ref('')
const loading = ref(false)
const loadingMore = ref(false)
const loadingNotices = ref(false)
const loadingMoreNotices = ref(false)
const errorMessage = ref('')
const searched = ref(false)
const activeTab = ref('followers')

const followers = ref<RelationUser[]>([])
const following = ref<RelationUser[]>([])
const notices = ref<NoticeItem[]>([])

const followerMaxTime = ref('0')
const followingMaxTime = ref('0')
const noticeMaxTime = ref('0')
const hasMoreFollowers = ref(false)
const hasMoreFollowing = ref(false)
const hasMoreNotices = ref(false)

function formatNumber(num: number): string {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

function formatTime(timestamp: number): string {
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN')
}

async function handleSearch() {
  if (!userId.value || !secUid.value) {
    ElMessage.warning('请输入用户ID和安全ID')
    return
  }

  loading.value = true
  errorMessage.value = ''
  followers.value = []
  following.value = []
  followerMaxTime.value = '0'
  followingMaxTime.value = '0'
  searched.value = true

  try {
    if (activeTab.value === 'followers') {
      await loadFollowers()
    } else {
      await loadFollowing()
    }
    ElMessage.success('查询成功')
  } catch (err: unknown) {
    const error = err as Error
    errorMessage.value = error.message || '查询失败'
  } finally {
    loading.value = false
  }
}

async function loadFollowers() {
  const res = await getFollowerList(userId.value, secUid.value, '0')
  if (res.success) {
    followers.value = res.data
    followerMaxTime.value = res.max_time
    hasMoreFollowers.value = res.has_more
  } else {
    throw new Error(res.message)
  }
}

async function loadFollowing() {
  const res = await getFollowingList(userId.value, secUid.value, '0')
  if (res.success) {
    following.value = res.data
    followingMaxTime.value = res.max_time
    hasMoreFollowing.value = res.has_more
  } else {
    throw new Error(res.message)
  }
}

function handleTabChange() {
  if (searched.value && userId.value && secUid.value) {
    if (activeTab.value === 'followers' && followers.value.length === 0) {
      loadFollowers()
    } else if (activeTab.value === 'following' && following.value.length === 0) {
      loadFollowing()
    }
  }
}

async function handleLoadMoreFollowers() {
  if (!hasMoreFollowers.value || loadingMore.value) return

  loadingMore.value = true
  try {
    const res = await getFollowerList(userId.value, secUid.value, followerMaxTime.value)
    if (res.success) {
      followers.value.push(...res.data)
      followerMaxTime.value = res.max_time
      hasMoreFollowers.value = res.has_more
    }
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loadingMore.value = false
  }
}

async function handleLoadMoreFollowing() {
  if (!hasMoreFollowing.value || loadingMore.value) return

  loadingMore.value = true
  try {
    const res = await getFollowingList(userId.value, secUid.value, followingMaxTime.value)
    if (res.success) {
      following.value.push(...res.data)
      followingMaxTime.value = res.max_time
      hasMoreFollowing.value = res.has_more
    }
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loadingMore.value = false
  }
}

async function handleLoadNotices() {
  loadingNotices.value = true
  notices.value = []
  noticeMaxTime.value = '0'

  try {
    const res = await getNoticeList('0', '20', '700')
    if (res.success) {
      notices.value = res.data
      noticeMaxTime.value = res.max_time
      hasMoreNotices.value = res.has_more
      ElMessage.success('加载成功')
    } else {
      ElMessage.error(res.message || '加载通知失败')
    }
  } catch (err) {
    ElMessage.error('加载通知失败')
  } finally {
    loadingNotices.value = false
  }
}

async function handleLoadMoreNotices() {
  if (!hasMoreNotices.value || loadingMoreNotices.value) return

  loadingMoreNotices.value = true
  try {
    const res = await getNoticeList(noticeMaxTime.value, '20', '700')
    if (res.success) {
      notices.value.push(...res.data)
      noticeMaxTime.value = res.max_time
      hasMoreNotices.value = res.has_more
    }
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loadingMoreNotices.value = false
  }
}
</script>

<style scoped>
.relation-view {
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

.notice-section {
  margin-top: 16px;
}

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
  align-items: center;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 4px;
}

.user-signature {
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-stats {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #909399;
}

.notices-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notice-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.notice-content {
  flex: 1;
}

.notice-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.notice-user {
  font-weight: 500;
}

.notice-time {
  font-size: 12px;
  color: #909399;
}

.notice-text {
  font-size: 13px;
  color: #606266;
}

.notice-cover {
  width: 60px;
  height: 80px;
  border-radius: 4px;
  flex-shrink: 0;
}

.load-more {
  text-align: center;
  margin-top: 24px;
}
</style>
