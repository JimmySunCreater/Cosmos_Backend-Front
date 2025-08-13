#!/bin/bash
# Cosmos API 部署状态检查脚本

echo "🚀 Cosmos API 部署状态检查"
echo "================================"

# 检查服务状态
echo "📋 1. 检查systemd服务状态:"
sudo systemctl is-active cosmos-api
sudo systemctl is-enabled cosmos-api

# 检查端口监听
echo ""
echo "🌐 2. 检查端口监听状态:"
sudo lsof -i :8080 | head -2

# 检查API健康状态
echo ""
echo "💚 3. 检查API健康状态:"
curl -s http://localhost:8080/health | python3 -m json.tool

# 检查GPU状态
echo ""
echo "🎮 4. 检查GPU状态:"
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

# 检查日志
echo ""
echo "📝 5. 最近的服务日志:"
sudo journalctl -u cosmos-api --no-pager -n 5

# 检查进程
echo ""
echo "🔍 6. 检查相关进程:"
ps aux | grep cosmos_api_service_simple | grep -v grep

echo ""
echo "✅ 部署状态检查完成!"
