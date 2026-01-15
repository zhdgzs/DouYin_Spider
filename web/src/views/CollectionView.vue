<template>
  <div class="collection-view">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>⭐ 我的收藏</span>
          <span class="subtitle">管理您的收藏夹</span>
        </div>
      </template>

      <el-button type="primary" :loading="loading" @click="handleRefresh">
        刷新收藏夹
      </el-button>

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

    <!-- 收藏夹列表 -->
    <el-card v-if="collections.length > 0" class="page-card">
      <div class="collections-grid">
        <div v-for="folder in collections" :key="folder.collect_id" class="collection-item">
          <div class="collection-cover">
            <el-image v-if="folder.cover" :src="folder.cover" fit="cover" lazy>
              <template #error>
                <div class="image-error">
                  <el-icon><Folder /></el-icon>
                </div>
              </template>
            </el-image>
            <div v-else class="image-error">
              <el-icon><Folder /></el-icon>
            </div>
            <div class="collection-count">{{ folder.video_count }} 个视频</div>
          </div>
          <div class="collection-info">
            <div class="collection-name">{{ folder.name }}</div>
            <div class="collection-time">
              创建于 {{ formatTime(folder.create_time) }}
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 空状态 -->
    <el-card v-if="loaded && collections.length === 0" class="page-card">
      <el-empty description="暂无收藏夹，点击上方按钮刷新" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Folder } from '@element-plus/icons-vue'
import { getCollectionList } from '../api/collection'
import type { CollectionFolder } from '../types/collection'

const loading = ref(false)
const errorMessage = ref('')
const loaded = ref(false)
const collections = ref<CollectionFolder[]>([])

function formatTime(timestamp: number): string {
  const date = new Date(timestamp * 1000)
  return date.toLocaleDateString('zh-CN')
}

async function handleRefresh() {
  loading.value = true
  errorMessage.value = ''

  try {
    const res = await getCollectionList()
    if (res.success) {
      collections.value = res.data
      loaded.value = true
      ElMessage.success('刷新成功')
    } else {
      errorMessage.value = res.message || '获取收藏夹失败'
    }
  } catch (err: unknown) {
    const error = err as Error
    errorMessage.value = error.message || '请求失败'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  handleRefresh()
})
</script>

<style scoped>
.collection-view {
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

.collections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.collection-item {
  border-radius: 8px;
  overflow: hidden;
  background: #f5f7fa;
  cursor: pointer;
  transition: transform 0.2s;
}

.collection-item:hover {
  transform: translateY(-4px);
}

.collection-cover {
  position: relative;
  aspect-ratio: 16/9;
}

.collection-cover .el-image {
  width: 100%;
  height: 100%;
}

.image-error {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 32px;
}

.collection-count {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.collection-info {
  padding: 12px;
}

.collection-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.collection-time {
  font-size: 12px;
  color: #909399;
}
</style>
