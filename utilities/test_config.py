#!/usr/bin/env python3
"""
配置文件测试脚本
验证EC2 IP自动获取功能是否正常工作
"""

import sys
import os

# 添加项目路径
sys.path.append('/home/ubuntu/cosmos_service/streamlit')

try:
    # 导入配置
    from config_streamlit import *
    
    print("✅ 配置文件导入成功")
    print(f"🌐 COSMOS_API_URL: {COSMOS_API_URL}")
    print(f"🌐 COSMOS_LOG_URL: {COSMOS_LOG_URL}")
    print(f"📡 EC2实例ID: {EC2_INSTANCE_ID}")
    print(f"🗺️  AWS区域: {EC2_REGION}")
    print(f"🖥️  EC2公网IP: {EC2_PUBLIC_IP}")
    
    # 测试API URL连通性
    import requests
    try:
        api_health_url = f"{COSMOS_API_URL}/health"
        print(f"\n🔍 测试API连接: {api_health_url}")
        
        response = requests.get(api_health_url, timeout=5)
        if response.status_code == 200:
            print("✅ API连接成功")
            data = response.json()
            print(f"📊 API服务状态: {data.get('status', 'unknown')}")
            print(f"🎬 队列大小: {data.get('queue_size', 'unknown')}")
            print(f"⚡ 活跃任务: {data.get('active_tasks', 'unknown')}")
        else:
            print(f"⚠️  API连接异常，状态码: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API连接失败: {str(e)}")
    
    # 测试LOG URL连通性（如果与API URL不同）
    if COSMOS_LOG_URL != COSMOS_API_URL:
        try:
            log_health_url = f"{COSMOS_LOG_URL}/health"
            print(f"\n🔍 测试日志连接: {log_health_url}")
            
            response = requests.get(log_health_url, timeout=5)
            if response.status_code == 200:
                print("✅ 日志连接成功")
            else:
                print(f"⚠️  日志连接异常，状态码: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 日志连接失败: {str(e)}")
    else:
        print("\n📝 API和日志使用相同URL")
    
except ImportError as e:
    print(f"❌ 配置文件导入失败: {str(e)}")
except Exception as e:
    print(f"❌ 配置测试失败: {str(e)}")
