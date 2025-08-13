#!/usr/bin/env python3
"""
Cosmos API Service 配置文件
"""

import os

class Config:
    """配置类"""
    
    # API服务配置
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '8080'))
    API_DEBUG = os.getenv('API_DEBUG', 'false').lower() == 'true'
    
    # AWS配置
    AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'SceneGeneration')
    
    # Conda环境配置
    CONDA_ENV_PATH = os.getenv('CONDA_ENV_PATH', '/home/ubuntu/miniconda3/envs/cosmos-predict1')
    COSMOS_BASE_PATH = os.getenv('COSMOS_BASE_PATH', '/home/ubuntu/cosmos-predict1')
    
    # 模型配置
    CHECKPOINT_DIR = os.getenv('CHECKPOINT_DIR', 'checkpoints')
    MULTIVIEW_MODEL_DIR = os.getenv('MULTIVIEW_MODEL_DIR', 'Cosmos-Predict1-7B-Text2World-Sample-AV-Multiview')
    SINGLEVIEW_MODEL_DIR = os.getenv('SINGLEVIEW_MODEL_DIR', 'Cosmos-Predict1-7B-Text2World')
    
    # GPU配置
    NUM_GPUS = int(os.getenv('NUM_GPUS', '8'))
    NPROC_PER_NODE = int(os.getenv('NPROC_PER_NODE', '8'))
    
    # 日志配置
    LOG_FILE = os.getenv('LOG_FILE', '/home/ubuntu/cosmos_service/cosmos_api.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # 队列配置
    MAX_QUEUE_SIZE = int(os.getenv('MAX_QUEUE_SIZE', '100'))
    TASK_TIMEOUT = int(os.getenv('TASK_TIMEOUT', '3600'))  # 1小时超时
    
    @classmethod
    def validate(cls):
        """验证配置"""
        errors = []
        
        # 检查必要的路径
        if not os.path.exists(cls.CONDA_ENV_PATH):
            errors.append(f"Conda environment path not found: {cls.CONDA_ENV_PATH}")
        
        if not os.path.exists(cls.COSMOS_BASE_PATH):
            errors.append(f"Cosmos base path not found: {cls.COSMOS_BASE_PATH}")
        
        # 检查端口范围
        if not (1 <= cls.API_PORT <= 65535):
            errors.append(f"Invalid API port: {cls.API_PORT}")
        
        # 检查GPU数量
        if cls.NUM_GPUS <= 0:
            errors.append(f"Invalid GPU count: {cls.NUM_GPUS}")
        
        return errors
    
    @classmethod
    def print_config(cls):
        """打印当前配置"""
        print("=== Cosmos API Service Configuration ===")
        print(f"API Host: {cls.API_HOST}")
        print(f"API Port: {cls.API_PORT}")
        print(f"Debug Mode: {cls.API_DEBUG}")
        print(f"AWS Region: {cls.AWS_REGION}")
        print(f"DynamoDB Table: {cls.DYNAMODB_TABLE_NAME}")
        print(f"Conda Environment: {cls.CONDA_ENV_PATH}")
        print(f"Cosmos Base Path: {cls.COSMOS_BASE_PATH}")
        print(f"Number of GPUs: {cls.NUM_GPUS}")
        print(f"Log File: {cls.LOG_FILE}")
        print("=" * 40)
