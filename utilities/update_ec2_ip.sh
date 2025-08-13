#!/bin/bash

# EC2公网IP自动更新脚本

echo "🔄 开始更新EC2公网IP配置..."

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# EC2配置
INSTANCE_ID="i-0bbe2d67c7493574f"
REGION="us-west-2"
CONFIG_FILE="$PROJECT_DIR/streamlit/config_streamlit.py"

# 检查Python脚本是否存在
if [ ! -f "$SCRIPT_DIR/get_ec2_ip.py" ]; then
    echo "❌ 找不到get_ec2_ip.py脚本"
    exit 1
fi

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 找不到配置文件: $CONFIG_FILE"
    exit 1
fi

# 获取当前IP信息
echo "📡 获取EC2实例信息..."
python3 "$SCRIPT_DIR/get_ec2_ip.py" --instance-id "$INSTANCE_ID" --region "$REGION"

# 更新配置文件
echo ""
echo "📝 更新配置文件..."
python3 "$SCRIPT_DIR/get_ec2_ip.py" --instance-id "$INSTANCE_ID" --region "$REGION" --update-config --config-file "$CONFIG_FILE"

# 检查更新结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ EC2公网IP配置更新完成"
    
    # 显示更新后的配置
    echo "📋 当前配置:"
    grep "COSMOS_LOG_URL" "$CONFIG_FILE" || echo "未找到COSMOS_LOG_URL配置"
    
    # 如果Streamlit正在运行，提示重启
    if pgrep -f "streamlit.*streamlit_app.py" > /dev/null; then
        echo ""
        echo "⚠️  检测到Streamlit正在运行，建议重启以应用新配置:"
        echo "   pkill -f streamlit"
        echo "   cd $PROJECT_DIR && ./start_web_ui.sh"
    fi
else
    echo "❌ 配置更新失败"
    exit 1
fi
