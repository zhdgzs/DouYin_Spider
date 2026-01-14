"""
API 配置管理
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# API 版本
API_VERSION = "1.0.0"

# 服务配置
HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", "8000"))

# CORS 配置
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# 请求超时配置 (秒)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# 视频代理配置
VIDEO_PROXY_CHUNK_SIZE = 1024 * 1024  # 1MB
