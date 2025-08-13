#!/bin/bash

echo "🧪 启动4K显示器测试页面..."

# 停止主应用
pkill -f "streamlit run streamlit_app.py"

# 启动测试页面
cd /home/ubuntu/cosmos_service/streamlit
echo "🚀 启动测试页面在端口5001..."
streamlit run test_4k_display.py --server.port=5001 --server.address=0.0.0.0 &

sleep 3

echo "✅ 测试页面已启动！"
echo "🌐 请访问: http://localhost:5001"
echo ""
echo "📋 测试检查项："
echo "1. 页面标题栏是否显示分辨率信息"
echo "2. 在4K显示器上字体是否足够大（20px）"
echo "3. 布局是否充分利用屏幕宽度"
echo "4. 侧边栏宽度是否合适（400px）"
echo "5. 各种组件的字体大小是否协调"
echo ""
echo "🔄 测试完成后，运行以下命令恢复主应用："
echo "   pkill -f test_4k_display"
echo "   ./restart_streamlit_4k.sh"
