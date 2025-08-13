#!/bin/bash

# Cosmos CloudScape界面公网访问启动脚本

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}=== Cosmos CloudScape界面公网访问启动脚本 ===${NC}"
echo -e "${YELLOW}当前目录: $SCRIPT_DIR${NC}"

# 获取公网IP
PUBLIC_IP=$(curl -s ifconfig.me)
PRIVATE_IP=$(hostname -I | awk '{print $1}')

echo -e "${GREEN}检测到的IP地址:${NC}"
echo -e "${BLUE}  公网IP: $PUBLIC_IP${NC}"
echo -e "${BLUE}  私有IP: $PRIVATE_IP${NC}"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: Python3 未安装${NC}"
    exit 1
fi

# 设置端口
PORT=5001

# 检查端口是否被占用
if sudo lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}警告: 端口 $PORT 已被占用，尝试终止占用进程...${NC}"
    sudo pkill -f "python3.*http.server.*$PORT" || true
    sleep 2
fi

# 检查防火墙状态
echo -e "${YELLOW}检查防火墙状态...${NC}"
UFW_STATUS=$(sudo ufw status | grep "Status:" | awk '{print $2}')

if [ "$UFW_STATUS" = "active" ]; then
    echo -e "${YELLOW}防火墙已启用，检查端口 $PORT 是否开放...${NC}"
    if ! sudo ufw status | grep -q "$PORT"; then
        echo -e "${YELLOW}开放端口 $PORT...${NC}"
        sudo ufw allow $PORT/tcp
        echo -e "${GREEN}端口 $PORT 已开放${NC}"
    else
        echo -e "${GREEN}端口 $PORT 已经开放${NC}"
    fi
else
    echo -e "${GREEN}防火墙未启用，无需配置${NC}"
fi

# 启动HTTP服务器，绑定到所有接口
echo -e "${GREEN}启动CloudScape界面服务器（公网访问模式）...${NC}"
echo -e "${BLUE}本地访问地址: http://localhost:$PORT${NC}"
echo -e "${BLUE}内网访问地址: http://$PRIVATE_IP:$PORT${NC}"
echo -e "${GREEN}公网访问地址: http://$PUBLIC_IP:$PORT${NC}"
echo ""
echo -e "${YELLOW}注意: 请确保AWS安全组已开放端口 $PORT${NC}"
echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
echo ""

# 启动服务器，绑定到所有接口 (0.0.0.0)
python3 -m http.server $PORT --bind 0.0.0.0

echo -e "${GREEN}服务已停止${NC}"
