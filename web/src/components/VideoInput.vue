<template>
  <div class="video-input">
    <el-input
      v-model="inputUrl"
      placeholder="请输入抖音视频链接，如: https://www.douyin.com/video/xxx"
      size="large"
      clearable
      @keyup.enter="handleParse"
    >
      <template #append>
        <el-button type="primary" :loading="loading" @click="handleParse">
          解析
        </el-button>
      </template>
    </el-input>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'parse', url: string): void
}>()

const inputUrl = ref('')

function handleParse() {
  if (inputUrl.value.trim()) {
    emit('parse', inputUrl.value.trim())
  }
}
</script>

<style scoped>
.video-input {
  margin-bottom: 24px;
}
</style>
