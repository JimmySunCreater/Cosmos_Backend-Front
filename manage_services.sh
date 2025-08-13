#!/bin/bash

# Cosmos 服务管理脚本

show_usage() {
    echo "用法: $0 {start|stop|restart|status|logs}"
    echo ""
    echo "命令说明:"
    echo "  start   - 启动所有服务"
    echo "  stop    - 停止所有服务"
    echo "  restart - 重启所有服务"
    echo "  status  - 查看服务状态"
    echo "  logs    - 查看服务日志"
    echo ""
    echo "服务访问地址:"
    echo "  API 服务:      http://localhost:8080"
    echo "  Streamlit UI:  http://localhost:8501"
    echo "  健康检查:      http://localhost:8080/health"
}

start_services() {
    echo "🚀 启动 Cosmos 服务..."
    sudo systemctl start cosmos-api.service
    sudo systemctl start cosmos-streamlit.service
    echo "✅ 服务启动完成"
    sleep 2
    show_status
}

stop_services() {
    echo "🛑 停止 Cosmos 服务..."
    sudo systemctl stop cosmos-api.service
    sudo systemctl stop cosmos-streamlit.service
    echo "✅ 服务停止完成"
}

restart_services() {
    echo "🔄 重启 Cosmos 服务..."
    sudo systemctl restart cosmos-api.service
    sudo systemctl restart cosmos-streamlit.service
    echo "✅ 服务重启完成"
    sleep 2
    show_status
}

show_status() {
    echo ""
    echo "📊 服务状态:"
    echo "============"
    
    # API 服务状态
    if systemctl is-active --quiet cosmos-api.service; then
        echo "✅ API 服务: 运行中 (http://localhost:8080)"
    else
        echo "❌ API 服务: 已停止"
    fi
    
    # Streamlit 服务状态
    if systemctl is-active --quiet cosmos-streamlit.service; then
        echo "✅ Streamlit UI: 运行中 (http://localhost:8501)"
    else
        echo "❌ Streamlit UI: 已停止"
    fi
    
    echo ""
    echo "🔍 端口监听状态:"
    ss -tlnp | grep -E ':(8080|8501)' || echo "没有发现监听端口"
    
    # 测试 API 健康状态
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo ""
        echo "🏥 API 健康检查: ✅ 正常"
        curl -s http://localhost:8080/health | python3 -m json.tool
    else
        echo ""
        echo "🏥 API 健康检查: ❌ 异常"
    fi
}

show_logs() {
    echo "📋 查看服务日志 (按 Ctrl+C 退出):"
    echo "================================"
    echo ""
    echo "API 服务日志:"
    echo "------------"
    sudo journalctl -u cosmos-api.service -n 10 --no-pager
    echo ""
    echo "Streamlit 服务日志:"
    echo "------------------"
    sudo journalctl -u cosmos-streamlit.service -n 10 --no-pager
}

case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

exit 0
