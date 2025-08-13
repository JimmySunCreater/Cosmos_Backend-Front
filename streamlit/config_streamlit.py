"""
Streamlit应用配置文件
"""

import boto3
import requests
from botocore.exceptions import ClientError, NoCredentialsError

def get_available_cosmos_server():
    """
    动态获取可用的Cosmos服务器IP地址
    返回 (private_ip, public_ip) 元组
    优先级：i-0bbe2d67c7493574f > i-07997436e1281b482
    """
    # 目标实例ID列表，按优先级排序
    target_instances = [
        "i-0bbe2d67c7493574f",
        "i-07997436e1281b482"
    ]
    
    try:
        # 创建EC2客户端
        ec2_client = boto3.client('ec2', region_name='us-west-2')
        
        # 获取实例信息
        response = ec2_client.describe_instances(InstanceIds=target_instances)
        
        # 检查每个实例的状态和可用性
        for instance_id in target_instances:
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if instance['InstanceId'] == instance_id:
                        # 检查实例是否运行中
                        if instance['State']['Name'] == 'running':
                            private_ip = instance.get('PrivateIpAddress')
                            public_ip = instance.get('PublicIpAddress')
                            
                            if private_ip:
                                # 测试服务是否可用（使用私有IP测试，因为我们在同一VPC内）
                                try:
                                    health_url = f"http://{private_ip}:8080/health"
                                    health_response = requests.get(health_url, timeout=5)
                                    if health_response.status_code == 200:
                                        print(f"✅ 使用Cosmos服务器: {instance_id}")
                                        print(f"   私有IP: {private_ip} (用于API调用)")
                                        print(f"   公网IP: {public_ip or 'N/A'} (用于日志页面)")
                                        return private_ip, public_ip
                                except requests.exceptions.RequestException:
                                    print(f"⚠️ 实例 {instance_id} ({private_ip}) 服务不可用")
                                    continue
        
        # 如果都不可用，返回默认IP
        print("⚠️ 所有目标实例都不可用，使用默认IP")
        return "172.31.8.172", None
        
    except (ClientError, NoCredentialsError) as e:
        print(f"⚠️ AWS API调用失败: {e}")
        print("使用默认IP地址")
        return "172.31.8.172", None
    except Exception as e:
        print(f"⚠️ 获取服务器IP时出错: {e}")
        return "172.31.8.172", None

# 动态获取Cosmos服务器IP
COSMOS_PRIVATE_IP, COSMOS_PUBLIC_IP = get_available_cosmos_server()

# API配置
ENHANCE_API_URL = "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/enhence"  # 保留作为备用
WEBSOCKET_ENHANCE_URL = "wss://qopfrzscp0.execute-api.us-west-2.amazonaws.com/prod"  # 新的WebSocket API
LIBRARY_API_URL = "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/library"
COSMOS_API_URL = f"http://{COSMOS_PRIVATE_IP}:8080"  # 使用私有IP进行API调用
COSMOS_LOG_URL = f"http://{COSMOS_PUBLIC_IP}:8080" if COSMOS_PUBLIC_IP else f"http://{COSMOS_PRIVATE_IP}:8080"  # 日志页面使用公网IP
API_KEY = "C2G4GCEdCP2KMKYKZlpxgaX28k2ud4sxY4gEa3Zh"

# 页面配置
PAGE_CONFIG = {
    "page_title": "Cosmos视频生成场景管理系统",
    "page_icon": None,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# API超时设置
API_TIMEOUT = {
    "enhance": 120,  # 场景增强API超时时间（秒）
    "library": 30,   # 场景库API超时时间（秒）
    "cosmos": 30     # Cosmos API超时时间（秒）
}

# 场景类型配置
SCENE_TYPES = {
    "SingleView": {
        "name": "单视角",
        "description": "单一视角场景，生成前方视角描述，适合简单场景",
        "icon": None,
        "estimated_time": "约1小时"
    },
    "MultiView": {
        "name": "多视角", 
        "description": "多视角场景，生成6个视角描述，适合复杂场景",
        "icon": None,
        "estimated_time": "约2小时"
    }
}

# 多视角视角配置
MULTIVIEW_ANGLES = [
    ("前方", "PROMPT_FRONT"),
    ("左前方", "PROMPT_FRONT_LEFT"),
    ("右前方", "PROMPT_FRONT_RIGHT"),
    ("后方", "PROMPT_BACK"),
    ("左后方", "PROMPT_BACK_LEFT"),
    ("右后方", "PROMPT_BACK_RIGHT")
]

# 状态映射
STATUS_MAPPING = {
    "Waiting": {"icon": None, "color": "info", "text": "等待中"},
    "Generating": {"icon": None, "color": "warning", "text": "生成中"},
    "Finished": {"icon": None, "color": "success", "text": "已完成"},
    "Failed": {"icon": None, "color": "error", "text": "失败"}
}
