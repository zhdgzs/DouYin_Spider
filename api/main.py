"""
FastAPI 应用入口
抖音视频解析 Web API 服务
"""
import os
import sys

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from loguru import logger

from api.config import (
    API_VERSION, CORS_ORIGINS, CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS, HOST, PORT
)
from api.routers.video import router as video_router
from api.routers.auth import router as auth_router

# 创建 FastAPI 应用
app = FastAPI(
    title="抖音视频解析 API",
    description="提供抖音视频链接解析、多清晰度下载地址获取等功能",
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# 注册路由
app.include_router(video_router)
app.include_router(auth_router)

# 静态文件服务 (前端构建产物)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "web", "dist")
if os.path.exists(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        """提供前端页面"""
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info(f"抖音视频解析 API 服务启动 - 版本 {API_VERSION}")
    logger.info(f"API 文档: http://{HOST}:{PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("抖音视频解析 API 服务关闭")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
