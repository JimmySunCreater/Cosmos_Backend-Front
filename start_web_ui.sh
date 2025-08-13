#!/bin/bash

# Cosmos场景管理Web界面启动脚本

echo "🎬 启动Cosmos场景管理Web界面..."
echo "🌙 配置为Dark主题模式"

# 检查streamlit目录是否存在
if [ ! -d "streamlit" ]; then
    echo "❌ streamlit目录不存在"
    exit 1
fi

# 进入streamlit目录并启动
cd streamlit
./start_streamlit.sh
