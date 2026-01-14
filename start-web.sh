#!/bin/bash

# 前端开发服务器启动脚本
# 使用方法: ./start-web.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/web"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  抖音视频解析 - 前端开发服务器${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查 Node.js 环境
if ! command -v node &> /dev/null; then
    echo -e "${RED}错误: 未找到 Node.js${NC}"
    echo -e "${YELLOW}请安装 Node.js 18+ 版本${NC}"
    exit 1
fi

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}错误: 未找到 npm${NC}"
    exit 1
fi

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo -e "${GREEN}安装依赖...${NC}"
    npm install
fi

echo -e "${GREEN}启动前端开发服务器...${NC}"
echo -e "${GREEN}访问地址: http://localhost:3000${NC}"
echo -e "${YELLOW}注意: 请确保后端 API 服务已启动 (./start-api.sh)${NC}"
echo ""

npm run dev
