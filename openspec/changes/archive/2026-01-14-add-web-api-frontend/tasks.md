# Implementation Tasks

## Phase 1: 基础 Web API 和视频解析页面

### 1. 后端 API 搭建
- [x] 1.1 创建 `requirements-api.txt`（独立依赖文件，不修改原有 requirements.txt）
- [x] 1.2 创建 `api/` 目录结构
- [x] 1.3 实现 FastAPI 应用入口 `api/main.py`
- [x] 1.4 实现视频解析接口 `POST /api/video/parse`（含文件大小获取）
- [x] 1.5 实现健康检查接口 `GET /api/health`
- [x] 1.6 配置 CORS 跨域支持
- [x] 1.7 实现视频代理接口 `GET /api/video/proxy`（用于预览播放）

### 2. 视频解析服务
- [x] 2.1 封装视频信息获取服务 `api/services/video_service.py`
- [x] 2.2 实现多清晰度视频地址提取
- [x] 2.3 实现视频文件大小获取（通过 HEAD 请求获取 Content-Length）
- [x] 2.4 实现视频信息格式化输出
- [x] 2.5 添加错误处理和异常捕获

### 3. 前端页面搭建
- [x] 3.1 初始化 Vue 3 + Vite 项目 `web/`
- [x] 3.2 安装依赖（axios, element-plus）
- [x] 3.3 创建主页面布局
- [x] 3.4 实现链接输入组件
- [x] 3.5 实现视频信息展示组件
- [x] 3.6 实现清晰度选择列表组件（含文件大小显示、选中状态）
- [x] 3.7 实现视频预览播放器组件（放置在清晰度列表下方）
- [x] 3.8 实现清晰度与播放器联动（点击切换视频源）
- [x] 3.9 实现复制链接功能
- [x] 3.10 实现下载功能

### 4. 集成和测试
- [x] 4.1 配置前端代理到后端 API
- [ ] 4.2 测试完整流程
- [x] 4.3 添加加载状态和错误提示
- [x] 4.4 编写启动脚本 `start-api.sh`

### 5. 文档更新
- [ ] 5.1 更新 README.md 添加 Web API 使用说明
- [ ] 5.2 添加 API 文档说明

---

## 重要约束

⚠️ **不修改现有代码**：
- `main.py` 保持原样，不做任何修改
- `dy_apis/`、`builder/`、`utils/` 等模块仅被 API 服务引用，不做修改
- 使用独立的 `requirements-api.txt` 管理 API 依赖

---

## 目录结构规划

```
DouYin_Spider/
├── api/                          # FastAPI 后端（新增）
│   ├── __init__.py
│   ├── main.py                   # FastAPI 应用入口
│   ├── routers/
│   │   ├── __init__.py
│   │   └── video.py              # 视频相关路由
│   ├── services/
│   │   ├── __init__.py
│   │   └── video_service.py      # 视频解析服务
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── video.py              # Pydantic 模型
│   └── config.py                 # 配置管理
│
├── web/                          # Vue 3 前端（新增）
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.ts
│       ├── App.vue
│       ├── components/
│       │   ├── VideoInput.vue    # 链接输入组件
│       │   ├── VideoInfo.vue     # 视频信息组件
│       │   ├── QualityList.vue   # 清晰度列表（含文件大小）
│       │   └── VideoPlayer.vue   # 视频预览组件（联动清晰度）
│       ├── api/
│       │   └── video.ts          # API 调用
│       └── types/
│           └── video.ts          # 类型定义
│
├── main.py                       # 原有爬虫入口（保持不变）
├── requirements.txt              # 原有依赖（保持不变）
├── requirements-api.txt          # API 专用依赖（新增）
├── start-api.sh                  # API 启动脚本（新增）
└── start-web.sh                  # 前端启动脚本（新增）
```

---

## API 接口设计

### POST /api/video/parse

**请求：**
```json
{
  "url": "https://www.douyin.com/video/7445533736877264178"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "video_id": "7445533736877264178",
    "title": "视频标题",
    "desc": "视频描述",
    "author": {
      "nickname": "作者昵称",
      "avatar": "头像URL",
      "sec_uid": "xxx"
    },
    "statistics": {
      "digg_count": 12345,
      "comment_count": 678,
      "share_count": 90,
      "collect_count": 123
    },
    "cover": "封面图URL",
    "duration": 15000,
    "create_time": 1704067200,
    "video_urls": [
      {
        "quality": "720p",
        "gear_name": "normal_720_0",
        "width": 1280,
        "height": 720,
        "file_size": 13107200,
        "file_size_str": "12.5 MB",
        "url": "https://..."
      },
      {
        "quality": "540p",
        "gear_name": "normal_540_0",
        "width": 960,
        "height": 540,
        "file_size": 8598323,
        "file_size_str": "8.2 MB",
        "url": "https://..."
      }
    ]
  }
}
```

### GET /api/health

**响应：**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### GET /api/video/proxy

**请求参数：**
- `url`: 原始视频 URL

**响应：**
- 视频流 (video/mp4)
