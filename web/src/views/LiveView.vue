<template>
  <div class="live-view">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>📺 直播信息</span>
          <span class="subtitle">输入直播间链接，获取直播信息和商品列表</span>
        </div>
      </template>

      <!-- 链接输入 -->
      <el-form @submit.prevent="handleSearch">
        <el-form-item>
          <el-input
            v-model="liveUrl"
            placeholder="请输入抖音直播间链接，如 https://live.douyin.com/xxx"
            size="large"
            clearable
          >
            <template #append>
              <el-button type="primary" :loading="loading" @click="handleSearch">
                获取信息
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

    <!-- 直播间信息 -->
    <el-card v-if="liveInfo" class="page-card">
      <div class="live-info-card">
        <div class="live-status">
          <el-tag :type="liveInfo.is_living ? 'danger' : 'info'" size="large">
            {{ liveInfo.is_living ? '🔴 直播中' : '⚪ 未开播' }}
          </el-tag>
        </div>
        <div class="live-details">
          <div class="live-title">{{ liveInfo.room_title || '直播间' }}</div>
          <div class="live-ids">
            <span>直播间ID: {{ liveInfo.room_id }}</span>
            <span>主播ID: {{ liveInfo.user_id }}</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 商品列表 -->
    <el-card v-if="liveInfo && liveInfo.is_living" class="page-card">
      <template #header>
        <div class="products-header">
          <span>商品列表 ({{ products.length }})</span>
          <el-button
            type="primary"
            size="small"
            :loading="loadingProducts"
            @click="handleLoadProducts"
          >
            {{ products.length > 0 ? '刷新商品' : '加载商品' }}
          </el-button>
        </div>
      </template>

      <div v-if="products.length > 0" class="products-grid">
        <div v-for="product in products" :key="product.promotion_id" class="product-item">
          <div class="product-cover">
            <el-image :src="product.cover" fit="cover" lazy>
              <template #error>
                <div class="image-error">
                  <el-icon><Goods /></el-icon>
                </div>
              </template>
            </el-image>
            <div v-if="!product.in_stock" class="out-of-stock">已售罄</div>
          </div>
          <div class="product-info">
            <div class="product-title">{{ product.title }}</div>
            <div class="product-price">
              <span class="current-price">¥{{ product.price.toFixed(2) }}</span>
              <span v-if="product.market_price > product.price" class="market-price">
                ¥{{ product.market_price.toFixed(2) }}
              </span>
            </div>
            <div class="product-sales">已售 {{ product.sales }}</div>
          </div>
        </div>
      </div>

      <el-empty v-else description="暂无商品，点击上方按钮加载" />

      <!-- 加载更多 -->
      <div v-if="hasMoreProducts && products.length > 0" class="load-more">
        <el-button :loading="loadingMore" @click="handleLoadMoreProducts">
          加载更多
        </el-button>
      </div>
    </el-card>

    <!-- 未开播提示 -->
    <el-card v-if="liveInfo && !liveInfo.is_living" class="page-card">
      <el-empty description="直播间未开播，无法获取商品信息" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Goods } from '@element-plus/icons-vue'
import { getLiveInfo, getLiveProducts } from '../api/live'
import type { LiveInfo, ProductItem } from '../types/live'

const liveUrl = ref('')
const loading = ref(false)
const loadingProducts = ref(false)
const loadingMore = ref(false)
const errorMessage = ref('')

const liveInfo = ref<LiveInfo | null>(null)
const products = ref<ProductItem[]>([])
const productOffset = ref('0')
const hasMoreProducts = ref(false)

async function handleSearch() {
  if (!liveUrl.value) {
    ElMessage.warning('请输入直播间链接')
    return
  }

  loading.value = true
  errorMessage.value = ''
  liveInfo.value = null
  products.value = []
  productOffset.value = '0'
  hasMoreProducts.value = false

  try {
    const res = await getLiveInfo(liveUrl.value)
    if (res.success && res.data) {
      liveInfo.value = res.data
      ElMessage.success('获取成功')
    } else {
      errorMessage.value = res.message || '获取直播间信息失败'
    }
  } catch (err: unknown) {
    const error = err as Error
    errorMessage.value = error.message || '请求失败'
  } finally {
    loading.value = false
  }
}

async function handleLoadProducts() {
  if (!liveInfo.value) return

  loadingProducts.value = true
  products.value = []
  productOffset.value = '0'

  try {
    const res = await getLiveProducts(
      liveUrl.value,
      liveInfo.value.room_id,
      liveInfo.value.user_id,
      '0'
    )
    if (res.success) {
      products.value = res.data
      productOffset.value = res.offset
      hasMoreProducts.value = res.has_more
      ElMessage.success(`已加载 ${res.data.length} 个商品`)
    } else {
      ElMessage.error(res.message || '加载商品失败')
    }
  } catch (err) {
    ElMessage.error('加载商品失败')
  } finally {
    loadingProducts.value = false
  }
}

async function handleLoadMoreProducts() {
  if (!liveInfo.value || !hasMoreProducts.value || loadingMore.value) return

  loadingMore.value = true
  try {
    const res = await getLiveProducts(
      liveUrl.value,
      liveInfo.value.room_id,
      liveInfo.value.user_id,
      productOffset.value
    )
    if (res.success) {
      products.value.push(...res.data)
      productOffset.value = res.offset
      hasMoreProducts.value = res.has_more
    }
  } catch (err) {
    ElMessage.error('加载失败')
  } finally {
    loadingMore.value = false
  }
}
</script>

<style scoped>
.live-view {
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

.live-info-card {
  display: flex;
  gap: 24px;
  align-items: center;
}

.live-details {
  flex: 1;
}

.live-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
}

.live-ids {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: #909399;
}

.products-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.product-item {
  border-radius: 8px;
  overflow: hidden;
  background: #f5f7fa;
}

.product-cover {
  position: relative;
  aspect-ratio: 1;
}

.product-cover .el-image {
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
  font-size: 32px;
}

.out-of-stock {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.product-info {
  padding: 12px;
}

.product-title {
  font-size: 13px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 8px;
  line-height: 1.4;
}

.product-price {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 4px;
}

.current-price {
  font-size: 16px;
  font-weight: 600;
  color: #f56c6c;
}

.market-price {
  font-size: 12px;
  color: #909399;
  text-decoration: line-through;
}

.product-sales {
  font-size: 12px;
  color: #909399;
}

.load-more {
  text-align: center;
  margin-top: 24px;
}
</style>
