<template>
  <div class="app-container">
    <!-- 认证检测（静默检测，不强制弹框） -->
    <AuthChecker
      @auth-success="handleAuthSuccess"
      @auth-required="handleAuthRequired"
    />

    <!-- Cookie 管理弹窗 -->
    <CookieManager
      v-model="showCookieManager"
      @cookie-updated="handleCookieUpdated"
    />

    <MainLayout>
      <template #user-info>
        <template v-if="userInfo">
          <div class="user-info" @click="showCookieManager = true">
            <el-avatar v-if="userInfo.avatar" :src="userInfo.avatar" :size="32" />
            <el-avatar v-else :size="32" icon="User" />
            <span class="nickname">{{ userInfo.nickname || `UID: ${userInfo.uid}` }}</span>
          </div>
        </template>
        <template v-else>
          <el-button
            :type="cookieInvalid ? 'danger' : 'primary'"
            text
            @click="showCookieManager = true"
          >
            <el-icon v-if="cookieInvalid" style="margin-right: 4px"><Warning /></el-icon>
            {{ cookieInvalid ? 'Cookie 无效' : 'Cookie 管理' }}
          </el-button>
        </template>
      </template>

      <!-- Cookie 无效提示（非阻塞） -->
      <el-alert
        v-if="cookieInvalid && !userInfo"
        title="Cookie 无效或未设置"
        description="部分功能可能受限，点击右上角「Cookie 管理」更新 Cookie"
        type="warning"
        show-icon
        :closable="true"
        @close="cookieInvalid = false"
        style="margin-bottom: 24px"
      />

      <!-- 路由视图 -->
      <router-view />
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Warning, User } from '@element-plus/icons-vue'
import MainLayout from './components/layout/MainLayout.vue'
import AuthChecker from './components/AuthChecker.vue'
import CookieManager from './components/CookieManager.vue'
import type { UserInfo } from './types/auth'

// 认证状态
const showCookieManager = ref(false)
const userInfo = ref<UserInfo | null>(null)
const cookieInvalid = ref(false)

// 认证成功
function handleAuthSuccess(info: UserInfo) {
  userInfo.value = info
  cookieInvalid.value = false
}

// 需要认证（不自动弹框，只标记状态）
function handleAuthRequired() {
  cookieInvalid.value = true
}

// Cookie 更新后刷新认证状态
function handleCookieUpdated() {
  window.location.reload()
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 20px;
  transition: background-color 0.2s;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-info .nickname {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}
</style>
