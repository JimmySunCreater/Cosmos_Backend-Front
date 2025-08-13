#!/bin/bash

# Cosmos CloudScape界面启动脚本

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}=== Cosmos CloudScape界面启动脚本 ===${NC}"
echo -e "${YELLOW}当前目录: $SCRIPT_DIR${NC}"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: Python3 未安装${NC}"
    exit 1
fi

# 检查端口是否被占用
PORT=5001
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}警告: 端口 $PORT 已被占用，尝试终止占用进程...${NC}"
    pkill -f "python3.*http.server.*$PORT" || true
    sleep 2
fi

# 启动HTTP服务器
echo -e "${GREEN}启动CloudScape界面服务器...${NC}"
echo -e "${BLUE}访问地址: http://localhost:$PORT${NC}"
echo -e "${BLUE}访问地址: http://$(hostname -I | awk '{print $1}'):$PORT${NC}"
echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
echo ""

# 启动简单的HTTP服务器
python3 -m http.server $PORT

echo -e "${GREEN}服务已停止${NC}"
