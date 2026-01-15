#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  抖音视频解析 - 一键打包脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# 打包前端
echo -e "\n${GREEN}[1/2] 打包前端...${NC}"
cd "$SCRIPT_DIR/web"
npm install
npx vite build
mkdir -p "$SCRIPT_DIR/dist"
cp -r dist/* "$SCRIPT_DIR/dist/"
echo -e "${GREEN}前端打包完成: $SCRIPT_DIR/dist/${NC}"

# 打包后端 Docker
echo -e "\n${GREEN}[2/2] 构建后端 Docker 镜像...${NC}"
cd "$SCRIPT_DIR"

# 检测 Docker 权限
DOCKER_CMD="docker"
if ! docker ps >/dev/null 2>&1; then
    if sudo docker ps >/dev/null 2>&1; then
        DOCKER_CMD="sudo docker"
        echo -e "${YELLOW}需要 sudo 权限运行 Docker${NC}"
    else
        echo -e "${RED}错误: 无法访问 Docker，请检查 Docker 是否安装并运行${NC}"
        exit 1
    fi
fi

$DOCKER_CMD build -f Dockerfile.api -t douyin-api:latest .
echo -e "${GREEN}Docker 镜像构建完成: douyin-api:latest${NC}"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "前端静态文件: ${GREEN}$SCRIPT_DIR/dist/${NC}"
echo -e "后端 Docker 镜像: ${GREEN}douyin-api:latest${NC}"
echo -e "\n部署命令:"
echo -e "  ${GREEN}docker run -d -p 8000:8000 --env-file .env douyin-api:latest${NC}"
