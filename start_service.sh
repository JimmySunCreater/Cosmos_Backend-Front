#!/bin/bash

# Cosmos API Service 启动脚本

# 设置环境变量
export API_HOST="0.0.0.0"
export API_PORT="8080"
export API_DEBUG="false"

# 设置AWS区域（根据你的实际区域调整）
export AWS_DEFAULT_REGION="us-west-2"

# 设置GPU数量
export NUM_GPUS="8"
export NPROC_PER_NODE="8"

# 确保日志目录存在
mkdir -p /home/ubuntu/cosmos_service/logs

# 启动服务
echo "Starting Cosmos API Service..."
echo "Service will be available at http://0.0.0.0:8080"
echo "Health check: http://0.0.0.0:8080/health"
echo "Logs will be written to /home/ubuntu/cosmos_service/cosmos_api.log"
echo "Using $NUM_GPUS GPUs"

cd /home/ubuntu/cosmos_service
python3 cosmos_api_service_simple.py
