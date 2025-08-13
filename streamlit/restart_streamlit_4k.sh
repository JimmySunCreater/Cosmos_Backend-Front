#!/bin/bash

# 4K显示器优化版Streamlit重启脚本

echo "🔄 正在重启Streamlit服务（4K优化版）..."

# 停止现有的streamlit进程
echo "📴 停止现有Streamlit进程..."
pkill -f streamlit

# 等待进程完全停止
sleep 2

# 检查是否还有残留进程
if pgrep -f streamlit > /dev/null; then
    echo "⚠️  强制终止残留进程..."
    pkill -9 -f streamlit
    sleep 1
fi

# 切换到streamlit目录
cd /home/ubuntu/cosmos_service/streamlit

# 检查依赖
echo "📦 检查Python依赖..."
pip3 install -r requirements_streamlit.txt --quiet

# 启动streamlit（4K优化版）
echo "🚀 启动4K优化版Streamlit..."
echo "📱 访问地址: http://localhost:5000"
echo "🖥️  4K显示器优化已启用"
echo "📊 支持的分辨率:"
echo "   - 4K (3840x2160): 大字体，宽布局"
echo "   - 2K (2560x1440): 中等字体，适中布局"
echo "   - FHD (1920x1080): 标准字体，标准布局"
echo ""
echo "💡 提示: 页面标题栏会显示检测到的分辨率信息"
echo ""

# 后台启动streamlit
nohup streamlit run streamlit_app.py --server.port=5000 --server.address=0.0.0.0 > streamlit_4k.log 2>&1 &

# 获取进程ID
STREAMLIT_PID=$!

echo "✅ Streamlit已启动 (PID: $STREAMLIT_PID)"
echo "📝 日志文件: streamlit_4k.log"

# 等待几秒钟检查启动状态
sleep 3

if ps -p $STREAMLIT_PID > /dev/null; then
    echo "🎉 Streamlit启动成功！"
    echo "🌐 请在浏览器中访问: http://localhost:5000"
    echo ""
    echo "🔧 如需查看日志:"
    echo "   tail -f streamlit_4k.log"
    echo ""
    echo "🛑 如需停止服务:"
    echo "   pkill -f streamlit"
else
    echo "❌ Streamlit启动失败，请检查日志:"
    echo "   tail streamlit_4k.log"
    exit 1
fi
