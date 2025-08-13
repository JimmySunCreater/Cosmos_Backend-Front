#!/bin/bash

# EC2公网IP管理脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

show_help() {
    echo "EC2公网IP管理工具"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  check     检查当前EC2实例IP信息"
    echo "  update    更新配置文件中的IP地址"
    echo "  status    显示当前配置状态"
    echo "  cron      设置定时自动更新任务"
    echo "  logs      查看IP更新日志"
    echo "  help      显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 check    # 检查EC2实例信息"
    echo "  $0 update   # 更新IP配置"
    echo "  $0 status   # 查看当前状态"
}

check_ec2_info() {
    echo "📡 检查EC2实例信息..."
    python3 "$SCRIPT_DIR/get_ec2_ip.py" \
        --instance-id "i-0bbe2d67c7493574f" \
        --region "us-west-2"
}

update_config() {
    echo "🔄 更新配置文件..."
    "$SCRIPT_DIR/update_ec2_ip.sh"
}

show_status() {
    echo "📋 当前配置状态:"
    echo ""
    
    # 显示配置文件中的IP
    CONFIG_FILE="$PROJECT_DIR/streamlit/config_streamlit.py"
    if [ -f "$CONFIG_FILE" ]; then
        echo "📝 配置文件: $CONFIG_FILE"
        grep -n "COSMOS.*URL\|EC2_PUBLIC_IP.*=" "$CONFIG_FILE" | head -10
    else
        echo "❌ 配置文件不存在"
    fi
    
    echo ""
    
    # 显示定时任务状态
    echo "⏰ 定时任务状态:"
    if crontab -l 2>/dev/null | grep -q "update_ec2_ip"; then
        echo "✅ 定时任务已设置"
        crontab -l | grep "update_ec2_ip"
    else
        echo "❌ 未设置定时任务"
    fi
    
    echo ""
    
    # 显示Streamlit运行状态
    echo "🌐 Streamlit运行状态:"
    if pgrep -f "streamlit.*streamlit_app.py" > /dev/null; then
        echo "✅ Streamlit正在运行"
        ps aux | grep "streamlit.*streamlit_app.py" | grep -v grep
    else
        echo "❌ Streamlit未运行"
    fi
}

setup_cron() {
    echo "⏰ 设置定时任务..."
    "$SCRIPT_DIR/setup_ip_cron.sh"
}

show_logs() {
    LOG_FILE="/home/ubuntu/cosmos_service/logs/ip_update.log"
    if [ -f "$LOG_FILE" ]; then
        echo "📄 IP更新日志 (最近20行):"
        echo "文件: $LOG_FILE"
        echo "----------------------------------------"
        tail -20 "$LOG_FILE"
    else
        echo "📄 暂无日志文件: $LOG_FILE"
    fi
}

# 主逻辑
case "$1" in
    check)
        check_ec2_info
        ;;
    update)
        update_config
        ;;
    status)
        show_status
        ;;
    cron)
        setup_cron
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        echo "请指定操作选项，使用 --help 查看帮助"
        echo ""
        show_help
        ;;
    *)
        echo "未知选项: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
