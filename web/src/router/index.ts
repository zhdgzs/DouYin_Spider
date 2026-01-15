/**
 * Vue Router 配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: '视频解析' }
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('../views/UserView.vue'),
    meta: { title: '用户分析' }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('../views/SearchView.vue'),
    meta: { title: '搜索中心' }
  },
  {
    path: '/comment',
    name: 'Comment',
    component: () => import('../views/CommentView.vue'),
    meta: { title: '评论分析' }
  },
  {
    path: '/live',
    name: 'Live',
    component: () => import('../views/LiveView.vue'),
    meta: { title: '直播信息' }
  },
  {
    path: '/collection',
    name: 'Collection',
    component: () => import('../views/CollectionView.vue'),
    meta: { title: '我的收藏' }
  },
  {
    path: '/relation',
    name: 'Relation',
    component: () => import('../views/RelationView.vue'),
    meta: { title: '关系网络' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：更新页面标题
router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title || '抖音工具'} - 抖音视频解析工具`
  next()
})

export default router
