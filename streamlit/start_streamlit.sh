#!/bin/bash

# Streamlit应用启动脚本

echo "🚀 启动Cosmos场景管理系统..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi

# 检查Streamlit是否安装
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 安装Streamlit依赖..."
    pip3 install -r requirements_streamlit.txt
fi

# 设置环境变量
export STREAMLIT_SERVER_PORT=5000
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 启动Streamlit应用
echo "🌐 启动Web界面..."
echo "访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"

streamlit run streamlit_app.py \
    --server.port=5000 \
    --server.address=0.0.0.0 \
    --browser.gatherUsageStats=false \
    --server.headless=true
