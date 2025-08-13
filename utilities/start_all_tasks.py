#!/usr/bin/env python3
"""
启动DynamoDB中所有等待中的任务
"""

import requests
import json
import time
import boto3
from botocore.exceptions import ClientError

def get_all_tasks():
    """获取DynamoDB中的所有任务"""
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('SceneGeneration')
        
        response = table.scan()
        items = response['Items']
        
        print(f"📋 从DynamoDB获取到 {len(items)} 个任务")
        return items
        
    except Exception as e:
        print(f"❌ 获取任务失败: {str(e)}")
        return []

def submit_task(uuid, scene_type):
    """提交单个任务"""
    try:
        payload = {"uuid": uuid}
        
        response = requests.post(
            "http://localhost:8080/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 任务提交成功: {uuid} ({scene_type})")
            return True
        else:
            print(f"❌ 任务提交失败: {uuid} - {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 任务提交异常: {uuid} - {str(e)}")
        return False

def check_api_health():
    """检查API服务健康状态"""
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"🟢 API服务健康")
            print(f"   - 队列大小: {data['queue_size']}")
            print(f"   - 活跃任务: {data['active_tasks']}")
            print(f"   - 可用GPU: {data['available_gpus']}")
            print(f"   - MultiView就绪: {data['multiview_ready']}")
            return True
        else:
            print(f"🔴 API服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"🔴 API服务连接失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 启动DynamoDB中的所有任务")
    print("=" * 50)
    
    # 1. 检查API服务状态
    if not check_api_health():
        print("❌ API服务不可用，退出")
        return
    
    # 2. 获取所有任务
    tasks = get_all_tasks()
    if not tasks:
        print("❌ 没有找到任务，退出")
        return
    
    # 3. 分析任务状态
    waiting_tasks = []
    finished_tasks = []
    generating_tasks = []
    failed_tasks = []
    
    for task in tasks:
        uuid = task['uuid']
        scene_type = task.get('SceneType', 'Unknown')
        status = task.get('generation_status', 'Unknown')
        
        if status == 'Waiting':
            waiting_tasks.append((uuid, scene_type))
        elif status == 'Finished':
            finished_tasks.append((uuid, scene_type))
        elif status == 'Generating':
            generating_tasks.append((uuid, scene_type))
        elif status == 'Failed':
            failed_tasks.append((uuid, scene_type))
    
    print(f"\n📊 任务状态统计:")
    print(f"   - 等待中: {len(waiting_tasks)} 个")
    print(f"   - 生成中: {len(generating_tasks)} 个")
    print(f"   - 已完成: {len(finished_tasks)} 个")
    print(f"   - 已失败: {len(failed_tasks)} 个")
    
    # 4. 显示详细信息
    if waiting_tasks:
        print(f"\n⏳ 等待中的任务:")
        for uuid, scene_type in waiting_tasks:
            print(f"   - {uuid} ({scene_type})")
    
    if generating_tasks:
        print(f"\n🔄 生成中的任务:")
        for uuid, scene_type in generating_tasks:
            print(f"   - {uuid} ({scene_type})")
    
    if finished_tasks:
        print(f"\n✅ 已完成的任务:")
        for uuid, scene_type in finished_tasks:
            print(f"   - {uuid} ({scene_type})")
    
    if failed_tasks:
        print(f"\n❌ 失败的任务:")
        for uuid, scene_type in failed_tasks:
            print(f"   - {uuid} ({scene_type})")
    
    # 5. 询问是否启动等待中的任务
    if waiting_tasks:
        print(f"\n🎯 发现 {len(waiting_tasks)} 个等待中的任务")
        choice = input("是否启动所有等待中的任务? (y/n): ").lower().strip()
        
        if choice == 'y':
            print(f"\n🚀 开始启动 {len(waiting_tasks)} 个任务...")
            success_count = 0
            
            for i, (uuid, scene_type) in enumerate(waiting_tasks, 1):
                print(f"\n[{i}/{len(waiting_tasks)}] 启动任务: {uuid}")
                if submit_task(uuid, scene_type):
                    success_count += 1
                
                # 避免过快提交，给服务器一点处理时间
                if i < len(waiting_tasks):
                    time.sleep(1)
            
            print(f"\n📈 启动结果:")
            print(f"   - 成功启动: {success_count} 个")
            print(f"   - 启动失败: {len(waiting_tasks) - success_count} 个")
            
        else:
            print("❌ 用户取消启动")
    
    # 6. 询问是否重新启动失败的任务
    if failed_tasks:
        print(f"\n🔄 发现 {len(failed_tasks)} 个失败的任务")
        choice = input("是否重新启动失败的任务? (y/n): ").lower().strip()
        
        if choice == 'y':
            print(f"\n🚀 开始重新启动 {len(failed_tasks)} 个失败任务...")
            success_count = 0
            
            for i, (uuid, scene_type) in enumerate(failed_tasks, 1):
                print(f"\n[{i}/{len(failed_tasks)}] 重启任务: {uuid}")
                if submit_task(uuid, scene_type):
                    success_count += 1
                
                if i < len(failed_tasks):
                    time.sleep(1)
            
            print(f"\n📈 重启结果:")
            print(f"   - 成功重启: {success_count} 个")
            print(f"   - 重启失败: {len(failed_tasks) - success_count} 个")
    
    # 7. 最终状态检查
    print(f"\n🔍 最终API状态:")
    check_api_health()
    
    print(f"\n✅ 任务启动完成!")

if __name__ == "__main__":
    main()
