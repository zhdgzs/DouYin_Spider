<template>
  <div class="main-layout">
    <AppHeader>
      <template #user-info>
        <slot name="user-info"></slot>
      </template>
    </AppHeader>

    <el-main class="main-content">
      <div class="content-wrapper">
        <slot></slot>
      </div>
    </el-main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.main-content {
  flex: 1;
  padding: 24px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
