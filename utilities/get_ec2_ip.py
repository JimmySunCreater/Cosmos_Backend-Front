#!/usr/bin/env python3
"""
EC2公网IP获取工具
用于自动获取指定EC2实例的公网IP地址
"""

import boto3
import json
import sys
import argparse
from datetime import datetime

def get_ec2_public_ip(instance_id, region='us-west-2'):
    """
    获取EC2实例的公网IP地址
    
    Args:
        instance_id (str): EC2实例ID
        region (str): AWS区域
    
    Returns:
        dict: 包含IP地址和实例信息的字典
    """
    try:
        # 创建EC2客户端
        ec2_client = boto3.client('ec2', region_name=region)
        
        # 获取实例信息
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        
        # 提取实例信息
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_info = {
                    'instance_id': instance_id,
                    'public_ip': instance.get('PublicIpAddress'),
                    'private_ip': instance.get('PrivateIpAddress'),
                    'state': instance.get('State', {}).get('Name'),
                    'instance_type': instance.get('InstanceType'),
                    'availability_zone': instance.get('Placement', {}).get('AvailabilityZone'),
                    'launch_time': instance.get('LaunchTime').isoformat() if instance.get('LaunchTime') else None,
                    'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])},
                    'region': region,
                    'query_time': datetime.now().isoformat()
                }
                
                return {
                    'success': True,
                    'data': instance_info,
                    'message': f"成功获取实例 {instance_id} 信息"
                }
                
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'message': f"获取EC2信息失败: {str(e)}"
        }

def update_config_file(instance_id, region='us-west-2', config_file=None):
    """
    更新配置文件中的IP地址
    
    Args:
        instance_id (str): EC2实例ID
        region (str): AWS区域
        config_file (str): 配置文件路径
    """
    if not config_file:
        config_file = "/home/ubuntu/cosmos_service/streamlit/config_streamlit.py"
    
    result = get_ec2_public_ip(instance_id, region)
    
    if result['success'] and result['data']['public_ip']:
        public_ip = result['data']['public_ip']
        
        try:
            # 读取配置文件
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找并替换IP地址 - 更新COSMOS_LOG_URL
            import re
            pattern1 = r'COSMOS_LOG_URL = "http://[\d.]+:8080"'
            replacement1 = f'COSMOS_LOG_URL = "http://{public_ip}:8080"'
            new_content = re.sub(pattern1, replacement1, content)
            
            # 查找并替换IP地址 - 更新COSMOS_API_URL
            pattern2 = r'COSMOS_API_URL = "http://[\d.]+:8080"'
            replacement2 = f'COSMOS_API_URL = "http://{public_ip}:8080"'
            new_content = re.sub(pattern2, replacement2, new_content)
            
            # 写回文件
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 成功更新配置文件: {config_file}")
            print(f"🌐 新的COSMOS_API_URL: http://{public_ip}:8080")
            print(f"🌐 新的COSMOS_LOG_URL: http://{public_ip}:8080")
            
        except Exception as e:
            print(f"❌ 更新配置文件失败: {str(e)}")
    else:
        print(f"❌ {result['message']}")

def main():
    parser = argparse.ArgumentParser(description='EC2公网IP获取工具')
    parser.add_argument('--instance-id', '-i', 
                       default='i-0bbe2d67c7493574f',
                       help='EC2实例ID (默认: i-0bbe2d67c7493574f)')
    parser.add_argument('--region', '-r', 
                       default='us-west-2',
                       help='AWS区域 (默认: us-west-2)')
    parser.add_argument('--update-config', '-u', 
                       action='store_true',
                       help='更新配置文件中的IP地址')
    parser.add_argument('--config-file', '-c',
                       help='配置文件路径')
    parser.add_argument('--json', '-j',
                       action='store_true',
                       help='以JSON格式输出')
    
    args = parser.parse_args()
    
    # 获取EC2信息
    result = get_ec2_public_ip(args.instance_id, args.region)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result['success']:
            data = result['data']
            print(f"🖥️  实例ID: {data['instance_id']}")
            print(f"🌐 公网IP: {data['public_ip'] or '无'}")
            print(f"🏠 私网IP: {data['private_ip'] or '无'}")
            print(f"⚡ 状态: {data['state']}")
            print(f"📦 实例类型: {data['instance_type']}")
            print(f"📍 可用区: {data['availability_zone']}")
            print(f"🕐 查询时间: {data['query_time']}")
            
            if data['tags']:
                print("🏷️  标签:")
                for key, value in data['tags'].items():
                    print(f"   {key}: {value}")
        else:
            print(f"❌ {result['message']}")
    
    # 更新配置文件
    if args.update_config:
        update_config_file(args.instance_id, args.region, args.config_file)

if __name__ == "__main__":
    main()
