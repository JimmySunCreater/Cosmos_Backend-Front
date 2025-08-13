#!/bin/bash

# 部署验证脚本 - 验证EC2 IP自动配置功能

echo "🔍 Cosmos服务部署验证"
echo "=================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    local status=$1
    local message=$2
    
    if [ "$status" = "OK" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    else
        echo -e "${RED}❌ $message${NC}"
    fi
}

# 1. 检查EC2实例信息
echo -e "\n${BLUE}1. 检查EC2实例信息${NC}"
echo "-----------------------------------"
if python3 "$SCRIPT_DIR/get_ec2_ip.py" --instance-id "i-0bbe2d67c7493574f" --region "us-west-2" > /dev/null 2>&1; then
    print_status "OK" "EC2实例信息获取成功"
    
    # 获取当前IP - 使用更简单的方法
    CURRENT_IP=$(python3 "$SCRIPT_DIR/get_ec2_ip.py" --instance-id "i-0bbe2d67c7493574f" --region "us-west-2" 2>/dev/null | grep "🌐 公网IP:" | cut -d' ' -f3)
    
    if [ -n "$CURRENT_IP" ] && [ "$CURRENT_IP" != "无" ]; then
        print_status "OK" "当前公网IP: $CURRENT_IP"
    else
        print_status "ERROR" "无法获取公网IP"
        # 尝试从配置文件获取IP
        CURRENT_IP=$(python3 -c "import sys; sys.path.append('$PROJECT_DIR/streamlit'); from config_streamlit import EC2_PUBLIC_IP; print(EC2_PUBLIC_IP)" 2>/dev/null)
        if [ -n "$CURRENT_IP" ]; then
            print_status "OK" "从配置获取IP: $CURRENT_IP"
        fi
    fi
else
    print_status "ERROR" "EC2实例信息获取失败"
fi

# 2. 检查配置文件
echo -e "\n${BLUE}2. 检查配置文件${NC}"
echo "-----------------------------------"
CONFIG_FILE="$PROJECT_DIR/streamlit/config_streamlit.py"
if [ -f "$CONFIG_FILE" ]; then
    print_status "OK" "配置文件存在: $CONFIG_FILE"
    
    # 检查配置内容
    if grep -q "COSMOS_API_URL.*EC2_PUBLIC_IP" "$CONFIG_FILE"; then
        print_status "OK" "COSMOS_API_URL配置正确"
    else
        print_status "ERROR" "COSMOS_API_URL配置异常"
    fi
    
    if grep -q "COSMOS_LOG_URL.*EC2_PUBLIC_IP" "$CONFIG_FILE"; then
        print_status "OK" "COSMOS_LOG_URL配置正确"
    else
        print_status "ERROR" "COSMOS_LOG_URL配置异常"
    fi
else
    print_status "ERROR" "配置文件不存在"
fi

# 3. 测试配置导入
echo -e "\n${BLUE}3. 测试配置导入${NC}"
echo "-----------------------------------"
if python3 "$SCRIPT_DIR/test_config.py" > /dev/null 2>&1; then
    print_status "OK" "配置文件导入成功"
    
    # 获取配置的URL
    CONFIG_URLS=$(python3 "$SCRIPT_DIR/test_config.py" 2>/dev/null | grep "COSMOS.*URL:" | head -2)
    echo "$CONFIG_URLS"
else
    print_status "ERROR" "配置文件导入失败"
fi

# 4. 测试API连接
echo -e "\n${BLUE}4. 测试API连接${NC}"
echo "-----------------------------------"
if [ -n "$CURRENT_IP" ]; then
    API_URL="http://$CURRENT_IP:8080/health"
    
    if curl -s --connect-timeout 5 "$API_URL" > /dev/null 2>&1; then
        print_status "OK" "API服务连接成功: $API_URL"
        
        # 获取服务状态
        STATUS=$(curl -s --connect-timeout 5 "$API_URL" | jq -r '.status' 2>/dev/null)
        if [ "$STATUS" = "healthy" ]; then
            print_status "OK" "API服务状态健康"
        else
            print_status "WARN" "API服务状态: $STATUS"
        fi
    else
        print_status "ERROR" "API服务连接失败: $API_URL"
    fi
else
    print_status "ERROR" "无法测试API连接，IP地址未知"
fi

# 5. 检查Streamlit服务
echo -e "\n${BLUE}5. 检查Streamlit服务${NC}"
echo "-----------------------------------"
if pgrep -f "streamlit.*streamlit_app.py" > /dev/null; then
    print_status "OK" "Streamlit服务正在运行"
    
    # 测试Streamlit端口
    if curl -s --connect-timeout 5 "http://localhost:8501" > /dev/null 2>&1; then
        print_status "OK" "Streamlit Web界面可访问"
    else
        print_status "WARN" "Streamlit Web界面连接异常"
    fi
else
    print_status "ERROR" "Streamlit服务未运行"
fi

# 6. 检查工具脚本
echo -e "\n${BLUE}6. 检查工具脚本${NC}"
echo "-----------------------------------"
TOOLS=("get_ec2_ip.py" "update_ec2_ip.sh" "manage_ec2_ip.sh" "test_config.py")

for tool in "${TOOLS[@]}"; do
    if [ -f "$SCRIPT_DIR/$tool" ] && [ -x "$SCRIPT_DIR/$tool" ]; then
        print_status "OK" "$tool 存在且可执行"
    else
        print_status "ERROR" "$tool 不存在或无执行权限"
    fi
done

# 7. 检查定时任务
echo -e "\n${BLUE}7. 检查定时任务${NC}"
echo "-----------------------------------"
if crontab -l 2>/dev/null | grep -q "update_ec2_ip"; then
    print_status "OK" "IP更新定时任务已设置"
    crontab -l | grep "update_ec2_ip"
else
    print_status "WARN" "IP更新定时任务未设置"
    echo "   可运行: $SCRIPT_DIR/setup_ip_cron.sh"
fi

# 总结
echo -e "\n${BLUE}部署验证完成${NC}"
echo "=================================="
echo "如果所有检查项都显示 ✅，说明EC2 IP自动配置功能部署成功！"
echo ""
echo "🔧 管理命令:"
echo "   检查状态: $SCRIPT_DIR/manage_ec2_ip.sh status"
echo "   更新IP:   $SCRIPT_DIR/manage_ec2_ip.sh update"
echo "   设置定时: $SCRIPT_DIR/manage_ec2_ip.sh cron"
echo "   查看日志: $SCRIPT_DIR/manage_ec2_ip.sh logs"
