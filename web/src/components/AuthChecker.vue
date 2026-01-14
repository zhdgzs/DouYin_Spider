<template>
  <!-- 无 UI，仅逻辑组件 -->
</template>

<script setup lang="ts">
/**
 * 认证检测组件
 * 页面加载时自动检测 Cookie 状态，无效时触发事件
 */
import { onMounted } from 'vue'
import { checkAuth } from '../api/auth'
import type { UserInfo } from '../types/auth'

const emit = defineEmits<{
  (e: 'auth-success', userInfo: UserInfo): void
  (e: 'auth-required'): void
  (e: 'auth-error', error: string): void
}>()

onMounted(async () => {
  try {
    const result = await checkAuth()

    if (result.valid && result.user_info) {
      emit('auth-success', result.user_info)
    } else {
      emit('auth-required')
    }
  } catch (err: unknown) {
    const error = err as Error
    emit('auth-error', error.message || '认证检测失败')
    emit('auth-required')
  }
})
</script>
