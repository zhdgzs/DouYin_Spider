<template>
  <div class="comment-view">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>💬 评论分析</span>
          <span class="subtitle">输入视频链接，获取评论列表</span>
        </div>
      </template>

      <!-- 链接输入 -->
      <el-form @submit.prevent="handleSearch">
        <el-form-item>
          <el-input
            v-model="videoUrl"
            placeholder="请输入抖音视频链接，如 https://www.douyin.com/video/xxx"
            size="large"
            clearable
          >
            <template #append>
              <el-button type="primary" :loading="loading" @click="handleSearch">
                获取评论
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

    <!-- 评论统计 -->
    <el-card v-if="comments.length > 0" class="page-card">
      <div class="comment-stats">
        <span>共 {{ total }} 条评论</span>
        <el-button
          type="primary"
          size="small"
          :loading="loadingAll"
          @click="handleLoadAll"
        >
          加载全部（含回复）
        </el-button>
      </div>
    </el-card>

    <!-- 评论列表 -->
    <el-card v-if="comments.length > 0" class="page-card">
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.cid" class="comment-item">
          <el-avatar :src="comment.user.avatar" :size="40" />
          <div class="comment-content">
            <div class="comment-header">
              <span class="comment-nickname">{{ comment.user.nickname }}</span>
              <span v-if="comment.ip_label" class="comment-location">{{ comment.ip_label }}</span>
            </div>
            <div class="comment-text">{{ comment.text }}</div>
            <div class="comment-footer">
              <span class="comment-time">{{ formatTime(comment.create_time) }}</span>
              <span class="comment-digg">❤️ {{ comment.digg_count }}</span>
              <span v-if="comment.reply_comment_total > 0" class="comment-replies">
                💬 {{ comment.reply_comment_total }} 条回复
              </span>
            </div>

            <!-- 回复列表 -->
            <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
              <div v-for="reply in comment.replies" :key="reply.cid" class="reply-item">
                <el-avatar :src="reply.user.avatar" :size="28" />
                <div class="reply-content">
                  <div class="reply-header">
                    <span class="reply-nickname">{{ reply.user.nickname }}</span>
                    <span v-if="reply.ip_label" class="reply-location">{{ reply.ip_label }}</span>
                  </div>
                  <div class="reply-text">{{ reply.text }}</div>
                  <div class="reply-footer">
                    <span class="reply-time">{{ formatTime(reply.create_time) }}</span>
                    <span class="reply-digg">❤️ {{ reply.digg_count }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载更多 -->
      <div v-if="hasMore" class="load-more">
        <el-button :loading="loadingMore" @click="handleLoadMore">
          加载更多
        </el-button>
      </div>
    </el-card>

    <!-- 空状态 -->
    <el-card v-if="searched && comments.length === 0" class="page-card">
      <el-empty description="暂无评论" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getCommentList, getAllComments } from '../api/comment'
import type { CommentItem, CommentWithReplies } from '../types/comment'

const videoUrl = ref('')
const loading = ref(false)
const loadingMore = ref(false)
const loadingAll = ref(false)
const errorMessage = ref('')
const searched = ref(false)

const comments = ref<(CommentItem | CommentWithReplies)[]>([])
const cursor = ref('0')
const hasMore = ref(false)
const total = ref(0)

function formatTime(timestamp: number): string {
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN')
}

async function handleSearch() {
  if (!videoUrl.value) {
    ElMessage.warning('请输入视频链接')
    return
  }

  loading.value = true
  errorMessage.value = ''
  comments.value = []
  cursor.value = '0'
  hasMore.value = false
  searched.value = true

  try {
    const res = await getCommentList(videoUrl.value, '0')
    if (res.success) {
      comments.value = res.data
      cursor.value = res.cursor
      hasMore.value = res.has_more
      total.value = res.total
      ElMessage.success('获取成功')
    } else {
      errorMessage.value = res.message || '获取评论失败'
    }
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
    const res = await getCommentList(videoUrl.value, cursor.value)
    if (res.success) {
      comments.value.push(...res.data)
      cursor.value = res.cursor
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
    const res = await getAllComments(videoUrl.value)
    if (res.success) {
      comments.value = res.data
      hasMore.value = false
      total.value = res.total
      ElMessage.success(`已加载全部 ${res.total} 条评论（含回复）`)
    }
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loadingAll.value = false
  }
}
</script>

<style scoped>
.comment-view {
  max-width: 800px;
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

.comment-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.comment-nickname {
  font-weight: 500;
  color: #303133;
}

.comment-location {
  font-size: 12px;
  color: #909399;
}

.comment-text {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 8px;
}

.comment-footer {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #909399;
}

.replies-list {
  margin-top: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reply-item {
  display: flex;
  gap: 8px;
}

.reply-content {
  flex: 1;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 2px;
}

.reply-nickname {
  font-size: 13px;
  font-weight: 500;
  color: #303133;
}

.reply-location {
  font-size: 11px;
  color: #909399;
}

.reply-text {
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
  margin-bottom: 4px;
}

.reply-footer {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: #909399;
}

.load-more {
  text-align: center;
  margin-top: 24px;
}
</style>
