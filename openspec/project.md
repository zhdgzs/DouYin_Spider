# Project Context

## Purpose
抖音数据爬虫工具，用于采集抖音平台的视频、用户、评论、直播等数据。支持批量爬取作品信息、用户作品列表、搜索结果，以及直播间实时消息监听（WebSocket）。数据可导出为 Excel 或下载媒体文件。

**核心功能：**
- 单个/批量作品信息爬取
- 用户全部作品爬取
- 关键词搜索（作品/用户/直播）
- 评论获取（一级/二级评论）
- 直播间实时消息监听（礼物、聊天、进入、点赞、关注）
- 收藏夹管理
- 粉丝/关注列表获取
- 数据导出（Excel、视频/图片下载）

## Tech Stack
- **语言**: Python 3.x
- **HTTP 请求**: requests
- **WebSocket**: websockets, websocket-client
- **协议解析**: protobuf (Protocol Buffers)
- **数据处理**: openpyxl (Excel), json
- **HTML 解析**: BeautifulSoup4
- **JavaScript 执行**: PyExecJS (签名生成)
- **异步支持**: asyncio, aiofiles
- **日志**: loguru
- **重试机制**: retry
- **环境配置**: python-dotenv

## Project Conventions

### Code Style
- 使用中文注释和文档字符串
- 函数命名采用 snake_case
- 类命名采用 PascalCase
- 静态方法用于无状态 API 调用
- 参数使用类型注解

### Architecture Patterns
```
DouYin_Spider/
├── main.py              # 主入口，Data_Spider 类
├── dy_apis/             # API 封装层
│   └── douyin_api.py    # DouyinAPI 静态方法集合
├── dy_live/             # 直播模块
│   └── server.py        # WebSocket 直播监听
├── builder/             # 请求构建器
│   ├── auth.py          # DouyinAuth 认证类
│   ├── header.py        # HeaderBuilder 请求头构建
│   ├── params.py        # Params 参数构建
│   └── proto.py         # Protobuf 构建
├── utils/               # 工具函数
│   ├── common_util.py   # 通用工具
│   ├── data_util.py     # 数据处理/下载
│   ├── dy_util.py       # 抖音特定工具（签名等）
│   └── cookie_util.py   # Cookie 处理
└── static/              # 静态资源
    ├── *.proto          # Protobuf 定义
    └── *_pb2.py         # 生成的 Protobuf 代码
```

**设计原则：**
- API 层与业务逻辑分离
- Builder 模式构建复杂请求
- 认证信息集中管理（DouyinAuth）
- 数据处理与下载解耦

### Testing Strategy
- 目前无自动化测试
- 通过 `if __name__ == '__main__'` 块进行手动测试
- 建议添加单元测试覆盖核心 API 方法

### Git Workflow
- 主分支: master
- 提交信息: 中英文混合，简洁描述变更
- 建议采用 Conventional Commits 规范

## Domain Context
**抖音 Web API 特点：**
- 需要 Cookie 认证（msToken, s_v_web_id, ttwid 等）
- 请求需携带签名参数（a_bogus, verifyFp）
- 分页使用 cursor/offset 机制
- 直播消息通过 WebSocket + Protobuf 传输
- 部分接口需要 CSRF token

**关键概念：**
- `aweme_id`: 作品 ID
- `sec_user_id`: 用户安全 ID
- `room_id`: 直播间 ID
- `msToken`: 请求令牌
- `a_bogus`: 请求签名参数

## Important Constraints
- **认证依赖**: 需要有效的抖音 Cookie 才能正常工作
- **反爬限制**: 请求频率过高可能触发风控
- **签名算法**: 依赖 JavaScript 执行环境生成签名
- **API 变更**: 抖音接口可能随时变更，需要维护更新
- **法律合规**: 仅供学习研究，请遵守相关法律法规

## External Dependencies
- **抖音 Web API**: https://www.douyin.com
- **抖音直播 API**: https://live.douyin.com
- **抖音创作者平台**: https://creator.douyin.com
- **WebSocket 服务**: wss://webcast5-ws-web-lf.douyin.com
