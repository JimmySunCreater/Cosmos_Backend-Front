#!/bin/bash

# 设置定时任务自动更新EC2公网IP

echo "⏰ 设置EC2公网IP自动更新定时任务..."

# 脚本路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPDATE_SCRIPT="$SCRIPT_DIR/update_ec2_ip.sh"

# 检查更新脚本是否存在
if [ ! -f "$UPDATE_SCRIPT" ]; then
    echo "❌ 找不到更新脚本: $UPDATE_SCRIPT"
    exit 1
fi

# 创建日志目录
LOG_DIR="/home/ubuntu/cosmos_service/logs"
mkdir -p "$LOG_DIR"

# 定时任务配置
CRON_JOB="*/30 * * * * $UPDATE_SCRIPT >> $LOG_DIR/ip_update.log 2>&1"

# 检查是否已存在相同的定时任务
if crontab -l 2>/dev/null | grep -q "$UPDATE_SCRIPT"; then
    echo "⚠️  定时任务已存在，正在更新..."
    # 删除旧的定时任务
    crontab -l 2>/dev/null | grep -v "$UPDATE_SCRIPT" | crontab -
fi

# 添加新的定时任务
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ 定时任务设置成功"
    echo "📋 任务详情:"
    echo "   - 执行频率: 每30分钟"
    echo "   - 执行脚本: $UPDATE_SCRIPT"
    echo "   - 日志文件: $LOG_DIR/ip_update.log"
    echo ""
    echo "📝 当前定时任务列表:"
    crontab -l | grep -E "(update_ec2_ip|#)"
    echo ""
    echo "🔧 管理命令:"
    echo "   查看日志: tail -f $LOG_DIR/ip_update.log"
    echo "   手动执行: $UPDATE_SCRIPT"
    echo "   删除任务: crontab -e (然后删除相关行)"
else
    echo "❌ 定时任务设置失败"
    exit 1
fi
