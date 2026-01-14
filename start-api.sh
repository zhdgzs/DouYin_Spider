#!/bin/bash

# 抖音视频解析 API 启动脚本
# 使用方法: ./start-api.sh [dev|prod]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  抖音视频解析 API 服务${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 python3${NC}"
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}警告: 未找到 .env 文件${NC}"
    echo -e "${YELLOW}请创建 .env 文件并配置 COOKIE 环境变量${NC}"
    echo ""
    echo "示例 .env 文件内容:"
    echo "COOKIE=your_douyin_cookie_here"
    echo ""
fi

# 检查依赖
echo -e "${GREEN}检查依赖...${NC}"
pip3 install -q -r requirements.txt
pip3 install -q -r requirements-api.txt

MODE=${1:-dev}

if [ "$MODE" == "prod" ]; then
    echo -e "${GREEN}启动生产模式...${NC}"
    echo -e "${GREEN}API 文档: http://0.0.0.0:8000/docs${NC}"
    python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
else
    echo -e "${GREEN}启动开发模式 (热重载)...${NC}"
    echo -e "${GREEN}API 文档: http://localhost:8000/docs${NC}"
    python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
fi
