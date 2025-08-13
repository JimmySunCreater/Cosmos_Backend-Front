#!/usr/bin/env python3
"""
Cosmos Predict API Service - GPU优化版本
处理视频生成任务的API服务，支持GPU智能分配和队列管理
"""

import os
import sys
import json
import uuid
from flask import Flask, jsonify, request, render_template, send_from_directory, Response
import subprocess
import threading
import queue
import time
import shlex
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError
import logging

# 导入配置
from config import Config
from gpu_manager import gpu_manager
from translator import BedrockTranslator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/cosmos_service/cosmos_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 北京时区
BEIJING_TZ = timezone(timedelta(hours=8))

@dataclass
class VideoTask:
    """视频生成任务数据结构"""
    uuid: str
    scene_type: str
    prompts: Dict[str, str]
    timestamp: datetime
    allocated_gpus: Optional[Any] = None  # 可以是单个GPU ID或GPU ID集合

class CosmosAPIService:
    """Cosmos预测API服务类"""
    
    def __init__(self):
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        self.task_queue = queue.Queue()
        self.active_tasks = {}  # task_uuid -> task_info
        self.task_lock = threading.Lock()
        
        # 初始化DynamoDB
        self.dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
        self.table = self.dynamodb.Table(Config.DYNAMODB_TABLE_NAME)
        
        # 初始化翻译器
        self.translator = BedrockTranslator(region_name='us-east-1')
        
        # Cosmos基础路径
        self.cosmos_base_path = Config.COSMOS_BASE_PATH
        
        # 启动任务调度线程
        self.scheduler_thread = threading.Thread(target=self._task_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # 注册路由
        self._register_routes()
        
    def _register_routes(self):
        """注册Flask路由"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """健康检查端点"""
            gpu_status = gpu_manager.get_status()
            with self.task_lock:
                active_task_count = len(self.active_tasks)
                current_tasks = list(self.active_tasks.keys()) if self.active_tasks else None
            
            return jsonify({
                'status': 'healthy',
                'queue_size': self.task_queue.qsize(),
                'active_tasks': active_task_count,
                'current_tasks': current_tasks,
                'available_gpus': len(gpu_status['available_gpus']),
                'occupied_gpus': len(gpu_status['occupied_gpus']),
                'gpu_status_detail': f"{len(gpu_status['available_gpus'])}/{gpu_status['total_gpus']} GPUs available",
                'multiview_ready': len(gpu_status['available_gpus']) == 8
            })
        
        @self.app.route('/generate', methods=['POST'])
        def generate_video():
            """接收视频生成任务"""
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                task_uuid = data.get('uuid')
                
                if not task_uuid:
                    return jsonify({'error': 'uuid is required'}), 400
                
                # 从DynamoDB获取SceneType和prompts
                scene_data = self._get_scene_data_from_db(task_uuid)
                if scene_data is None:
                    return jsonify({'error': f'No scene data found for uuid: {task_uuid}'}), 404
                
                scene_type = scene_data.get('SceneType')
                if not scene_type:
                    return jsonify({'error': f'SceneType not found for uuid: {task_uuid}'}), 404
                
                if scene_type not in ['MultiView', 'SingleView']:
                    return jsonify({'error': f'Invalid SceneType: {scene_type}'}), 400
                
                # 获取中文prompts
                prompts = self._extract_prompts_from_scene_data(scene_data, scene_type)
                if not prompts:
                    return jsonify({'error': f'No prompts found for uuid: {task_uuid}'}), 404
                
                # 异步翻译并处理任务
                threading.Thread(
                    target=self._translate_and_process_task,
                    args=(task_uuid, scene_type, prompts),
                    daemon=True
                ).start()
                
                return jsonify({
                    'message': 'Task added to queue successfully',
                    'uuid': task_uuid,
                    'scene_type': scene_type,
                    'status': 'Processing'
                })
                
            except Exception as e:
                logger.error(f"Error in generate_video: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/status/<task_uuid>', methods=['GET'])
        def get_task_status(task_uuid):
            """获取任务状态"""
            try:
                response = self.table.get_item(Key={'uuid': task_uuid})
                if 'Item' not in response:
                    return jsonify({'error': 'Task not found'}), 404
                
                item = response['Item']
                return jsonify({
                    'uuid': task_uuid,
                    'generation_status': item.get('generation_status', 'Unknown'),
                    'update_time': item.get('update_time', ''),
                    'queue_size': self.task_queue.qsize(),
                    'active_tasks': len(self.active_tasks),
                    'video_link': item.get('video_link', '')
                })
                
            except Exception as e:
                logger.error(f"Error getting task status: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/gpu-status', methods=['GET'])
        def get_gpu_status():
            """获取GPU状态"""
            try:
                gpu_status = gpu_manager.get_status()
                return jsonify({
                    'gpu_manager_status': gpu_status,
                    'queue_size': self.task_queue.qsize(),
                    'active_tasks': len(self.active_tasks),
                    'active_task_details': dict(self.active_tasks)
                })
            except Exception as e:
                logger.error(f"Error getting GPU status: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/logs', methods=['GET'])
        def view_logs():
            """日志查看器页面"""
            return render_template('logs.html')
        
        @self.app.route('/logs/stream', methods=['GET'])
        def stream_logs():
            """实时日志流（Server-Sent Events）"""
            def generate():
                try:
                    log_file = '/home/ubuntu/cosmos_service/cosmos_api.log'
                    if not os.path.exists(log_file):
                        yield f"data: Log file not found: {log_file}\n\n"
                        return

                    # 先发送最后1000行历史日志
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        recent_lines = lines[-1000:] if len(lines) > 1000 else lines
                        for line in recent_lines:
                            yield f"data: {line.strip()}\n\n"

                    # 持续监控新日志
                    with open(log_file, 'r', encoding='utf-8') as f:
                        # 移动到文件末尾
                        f.seek(0, 2)
                        while True:
                            line = f.readline()
                            if not line:
                                time.sleep(0.1)  # 没有新日志时短暂休息
                                continue
                            yield f"data: {line.strip()}\n\n"
                except Exception as e:
                    logger.error(f"Error in log streaming: {str(e)}")
                    yield f"data: Error: {str(e)}\n\n"

            return Response(generate(), mimetype='text/event-stream')
        
        @self.app.route('/logs/stream/<task_uuid>', methods=['GET'])
        def stream_task_logs(task_uuid):
            """获取特定任务的日志"""
            try:
                log_file = '/home/ubuntu/cosmos_service/cosmos_api.log'
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # 过滤包含特定UUID的日志行
                        task_lines = [line for line in lines if task_uuid in line]
                        return ''.join(task_lines), 200, {'Content-Type': 'text/plain; charset=utf-8'}
                else:
                    return 'Log file not found', 404
            except Exception as e:
                logger.error(f"Error reading task logs: {str(e)}")
                return f'Error reading task logs: {str(e)}', 500
    
    def _translate_and_process_task(self, task_uuid: str, scene_type: str, prompts: Dict[str, str]):
        """翻译prompts并处理任务"""
        try:
            logger.info(f"Starting translation for task {task_uuid}")
            
            # 更新状态为翻译中
            self._update_task_status(task_uuid, 'Translating')
            
            # 翻译所有提示词为英文
            translated_prompts = {}
            failed_translations = []
            
            for key, chinese_text in prompts.items():
                logger.info(f"Processing {key}: {chinese_text[:50]}...")
                english_text = self.translator.translate_to_english(chinese_text)
                
                if english_text:  # 只要翻译器返回了结果就认为成功
                    translated_prompts[key] = english_text
                    if english_text == chinese_text:
                        logger.info(f"Text {key} is already in English, no translation needed")
                    else:
                        logger.info(f"Successfully translated {key}")
                else:
                    failed_translations.append(key)
                    logger.error(f"Failed to translate {key}: translator returned None or empty result")
            
            if failed_translations:
                logger.error(f"Translation failed for keys: {failed_translations} in task {task_uuid}")
                self._update_task_status(task_uuid, 'Failed')
                return
            
            # 保存英文翻译到DynamoDB
            self._save_translated_prompts(task_uuid, scene_type, translated_prompts)
            
            # 创建任务并添加到队列
            task = VideoTask(
                uuid=task_uuid,
                scene_type=scene_type,
                prompts=translated_prompts,  # 使用翻译后的英文prompts
                timestamp=datetime.now(BEIJING_TZ)
            )
            
            # 更新状态为等待中
            self._update_task_status(task_uuid, 'Waiting')
            
            # 添加到队列
            self.task_queue.put(task)
            logger.info(f"Task added to queue after translation: {task_uuid}, SceneType: {scene_type}")
            
        except Exception as e:
            logger.error(f"Error in translate_and_process_task: {str(e)}")
            self._update_task_status(task_uuid, 'Failed')
    
    def _save_translated_prompts(self, task_uuid: str, scene_type: str, translated_prompts: Dict[str, str]):
        """保存翻译后的英文prompts到DynamoDB对应的_EN字段"""
        try:
            # 构建更新表达式
            update_expressions = []
            expr_names = {}
            expr_values = {}
            
            # 映射prompt key到对应的英文字段
            field_mapping = {
                'prompt': 'PROMPT_FRONT_EN',
                'prompt_left': 'PROMPT_FRONT_LEFT_EN',
                'prompt_right': 'PROMPT_FRONT_RIGHT_EN',
                'prompt_back': 'PROMPT_BACK_EN',
                'prompt_back_left': 'PROMPT_BACK_LEFT_EN',
                'prompt_back_right': 'PROMPT_BACK_RIGHT_EN'
            }
            
            for key, english_text in translated_prompts.items():
                if key in field_mapping:
                    field_name = field_mapping[key]
                    attr_name = f"#{field_name.lower()}"
                    attr_value = f":{field_name.lower()}"
                    
                    expr_names[attr_name] = field_name
                    expr_values[attr_value] = english_text
                    update_expressions.append(f"{attr_name} = {attr_value}")
                    
                    logger.info(f"Mapping {key} -> {field_name}")
            
            if update_expressions:
                update_expression = "SET " + ", ".join(update_expressions)
                
                self.table.update_item(
                    Key={'uuid': task_uuid},
                    UpdateExpression=update_expression,
                    ExpressionAttributeNames=expr_names,
                    ExpressionAttributeValues=expr_values
                )
                
                logger.info(f"Saved {len(translated_prompts)} translated prompts to DynamoDB for task {task_uuid}")
                
                # 记录保存的字段
                for key, field_name in field_mapping.items():
                    if key in translated_prompts:
                        logger.info(f"Saved {field_name}: {translated_prompts[key][:50]}...")
            
        except Exception as e:
            logger.error(f"Error saving translated prompts: {str(e)}")
    
    def _get_scene_data_from_db(self, task_uuid: str) -> Optional[Dict[str, Any]]:
        """从DynamoDB获取完整的场景数据"""
        try:
            response = self.table.get_item(Key={'uuid': task_uuid})
            if 'Item' in response:
                return response['Item']
            else:
                logger.warning(f"No scene data found for UUID: {task_uuid}")
                return None
        except Exception as e:
            logger.error(f"Error getting scene data from DynamoDB: {str(e)}")
            return None
    
    def _extract_prompts_from_scene_data(self, scene_data: Dict[str, Any], scene_type: str) -> Optional[Dict[str, str]]:
        """从场景数据中提取中文prompts用于翻译"""
        try:
            prompts = {}
            
            if scene_type == 'SingleView':
                # SingleView只需要前方视角
                front_prompt = scene_data.get('PROMPT_FRONT')
                if front_prompt:
                    prompts['prompt'] = front_prompt
                else:
                    logger.error(f"No front prompt found for SingleView task {scene_data.get('uuid')}")
                    return None
                    
            elif scene_type == 'MultiView':
                # MultiView需要所有6个视角的中文prompts
                prompt_keys = [
                    ('prompt', 'PROMPT_FRONT'),
                    ('prompt_left', 'PROMPT_FRONT_LEFT'),
                    ('prompt_right', 'PROMPT_FRONT_RIGHT'),
                    ('prompt_back', 'PROMPT_BACK'),
                    ('prompt_back_left', 'PROMPT_BACK_LEFT'),
                    ('prompt_back_right', 'PROMPT_BACK_RIGHT')
                ]
                
                for key, field in prompt_keys:
                    prompt_value = scene_data.get(field)
                    if prompt_value:
                        prompts[key] = prompt_value
                    else:
                        logger.warning(f"Missing Chinese prompt for {key} in task {scene_data.get('uuid')}")
                
                # 检查是否有足够的prompts
                if len(prompts) < 6:
                    logger.error(f"Insufficient Chinese prompts for MultiView task {scene_data.get('uuid')}: {len(prompts)}/6")
                    return None
            
            logger.info(f"Extracted {len(prompts)} Chinese prompts for {scene_type} task {scene_data.get('uuid')}")
            return prompts
            
        except Exception as e:
            logger.error(f"Error extracting prompts: {str(e)}")
            return None
        """从DynamoDB获取提示词参数"""
        try:
            response = self.table.get_item(Key={'uuid': task_uuid})
            
            if 'Item' not in response:
                logger.error(f"No item found for uuid: {task_uuid}")
                return None
            
            item = response['Item']
            
            if scene_type == 'MultiView':
                prompts = {
                    'prompt': item.get('PROMPT_FRONT', ''),
                    'prompt_left': item.get('PROMPT_FRONT_LEFT', ''),
                    'prompt_right': item.get('PROMPT_FRONT_RIGHT', ''),
                    'prompt_back': item.get('PROMPT_BACK', ''),
                    'prompt_back_left': item.get('PROMPT_BACK_LEFT', ''),
                    'prompt_back_right': item.get('PROMPT_BACK_RIGHT', '')
                }
            elif scene_type == 'SingleView':
                prompts = {
                    'prompt': item.get('PROMPT_FRONT', '')
                }
            
            # 检查必要的提示词是否存在
            if not prompts.get('prompt'):
                logger.error(f"No PROMPT_FRONT found for uuid: {task_uuid}")
                return None
            
            return prompts
            
        except Exception as e:
            logger.error(f"Error getting prompts: {str(e)}")
            return None
    
    def _update_task_status(self, task_uuid: str, status: str):
        """更新任务状态到DynamoDB"""
        try:
            beijing_time = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S BJT')
            
            self.table.update_item(
                Key={'uuid': task_uuid},
                UpdateExpression='SET generation_status = :status, update_time = :time',
                ExpressionAttributeValues={
                    ':status': status,
                    ':time': beijing_time
                }
            )
            logger.info(f"Updated task {task_uuid} generation_status to {status}")
            
        except Exception as e:
            logger.error(f"Error updating task status: {str(e)}")
    
    def _task_scheduler(self):
        """智能任务调度器 - 支持并行处理SingleView任务"""
        logger.info("Task scheduler thread started")
        
        while True:
            try:
                # 检查是否有任务可以处理
                if not self.task_queue.empty():
                    # 获取GPU状态
                    gpu_status = gpu_manager.get_status()
                    available_gpus = len(gpu_status['available_gpus'])
                    
                    # 尝试从队列中获取任务
                    try:
                        task = self.task_queue.get(timeout=1)
                        
                        # 检查是否可以分配资源
                        can_process = False
                        
                        if task.scene_type == 'SingleView':
                            # SingleView只需要1个GPU
                            if available_gpus >= 1:
                                can_process = True
                        elif task.scene_type == 'MultiView':
                            # MultiView需要所有8个GPU
                            if available_gpus == 8:
                                can_process = True
                        
                        if can_process:
                            # 启动新的处理线程
                            processing_thread = threading.Thread(
                                target=self._process_single_task,
                                args=(task,),
                                daemon=True
                            )
                            processing_thread.start()
                            logger.info(f"Started processing thread for task {task.uuid} ({task.scene_type})")
                        else:
                            # 资源不足，将任务放回队列
                            self.task_queue.put(task)
                            logger.info(f"Task {task.uuid} ({task.scene_type}) waiting for resources. Available GPUs: {available_gpus}")
                            time.sleep(30)  # 等待30秒再检查
                            
                    except queue.Empty:
                        continue
                else:
                    # 队列为空，等待
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in task scheduler: {str(e)}")
                time.sleep(1)
    
    def _process_single_task(self, task: VideoTask):
        """处理单个任务"""
        try:
            # 添加到活跃任务列表
            with self.task_lock:
                self.active_tasks[task.uuid] = {
                    'scene_type': task.scene_type,
                    'start_time': datetime.now(BEIJING_TZ).isoformat(),
                    'status': 'Allocating GPU'
                }
            
            logger.info(f"Processing task: {task.uuid}, SceneType: {task.scene_type}")
            
            # 分配GPU资源
            if task.scene_type == 'SingleView':
                allocated_gpu = gpu_manager.allocate_gpu_for_singleview(task.uuid)
                if allocated_gpu is None:
                    logger.error(f"No available GPU for SingleView task {task.uuid}")
                    self._update_task_status(task.uuid, 'Failed')
                    return
                task.allocated_gpus = allocated_gpu
            else:  # MultiView
                allocated_gpus = gpu_manager.allocate_gpus_for_multiview(task.uuid)
                if allocated_gpus is None:
                    logger.error(f"Not enough GPUs for MultiView task {task.uuid}")
                    self._update_task_status(task.uuid, 'Failed')
                    return
                task.allocated_gpus = allocated_gpus
            
            # 更新活跃任务状态
            with self.task_lock:
                if task.uuid in self.active_tasks:
                    self.active_tasks[task.uuid]['status'] = 'Generating'
                    self.active_tasks[task.uuid]['allocated_gpus'] = (
                        [task.allocated_gpus] if task.scene_type == 'SingleView' 
                        else list(task.allocated_gpus)
                    )
            
            # 更新数据库状态为Generating
            self._update_task_status(task.uuid, 'Generating')
            
            # 执行视频生成
            success = self._execute_video_generation(task)
            
            # 如果视频生成成功，上传到S3
            if success:
                logger.info(f"Video generation successful, uploading to S3 for task {task.uuid}")
                with self.task_lock:
                    if task.uuid in self.active_tasks:
                        self.active_tasks[task.uuid]['status'] = 'Uploading to S3'
                
                upload_success = self._upload_video_to_s3(task.uuid, task.scene_type)
                if upload_success:
                    logger.info(f"Video uploaded to S3 successfully for task {task.uuid}")
                    final_status = 'Finished'
                else:
                    logger.error(f"Video upload to S3 failed for task {task.uuid}")
                    final_status = 'Failed'
            else:
                final_status = 'Failed'
            
            # 释放GPU资源
            if task.scene_type == 'SingleView':
                gpu_manager.release_gpu(task.allocated_gpus, task.uuid)
            else:  # MultiView
                gpu_manager.release_gpus(task.allocated_gpus, task.uuid)
            
            # 更新最终状态
            self._update_task_status(task.uuid, final_status)
            
            logger.info(f"Task {task.uuid} completed with status: {final_status}")
            
        except Exception as e:
            logger.error(f"Error processing task {task.uuid}: {str(e)}")
            self._update_task_status(task.uuid, 'Failed')
            
            # 确保释放GPU资源
            if hasattr(task, 'allocated_gpus') and task.allocated_gpus is not None:
                if task.scene_type == 'SingleView':
                    gpu_manager.release_gpu(task.allocated_gpus, task.uuid)
                else:
                    gpu_manager.release_gpus(task.allocated_gpus, task.uuid)
        finally:
            # 从活跃任务列表中移除
            with self.task_lock:
                if task.uuid in self.active_tasks:
                    del self.active_tasks[task.uuid]
    
    def _execute_video_generation(self, task: VideoTask) -> bool:
        """执行视频生成命令"""
        try:
            # 使用Conda的正确激活方式
            conda_init = f"source /home/ubuntu/miniconda3/etc/profile.d/conda.sh"
            conda_activate = f"conda activate cosmos-predict1"
            
            if task.scene_type == 'MultiView':
                # MultiView使用所有分配的GPU
                num_gpus = str(len(task.allocated_gpus))
                nproc_per_node = num_gpus
                
                cmd = [
                    "torchrun",
                    f"--nproc_per_node={nproc_per_node}",
                    "cosmos_predict1/diffusion/inference/text2world_multiview.py",
                    "--num_gpus", num_gpus,
                    "--checkpoint_dir", "checkpoints",
                    "--diffusion_transformer_dir", "Cosmos-Predict1-7B-Text2World-Sample-AV-Multiview",
                    "--prompt", task.prompts['prompt'],
                    "--prompt_left", task.prompts['prompt_left'],
                    "--prompt_right", task.prompts['prompt_right'],
                    "--prompt_back", task.prompts['prompt_back'],
                    "--prompt_back_left", task.prompts['prompt_back_left'],
                    "--prompt_back_right", task.prompts['prompt_back_right'],
                    "--video_save_name", task.uuid
                ]
                
                # 设置GPU环境变量
                gpu_list = ','.join(map(str, sorted(task.allocated_gpus)))
                env_vars = f"CUDA_VISIBLE_DEVICES={gpu_list}"
                
            else:  # SingleView使用单个GPU
                gpu_id = task.allocated_gpus
                
                cmd = [
                    "python",  # 单GPU不需要torchrun
                    "cosmos_predict1/diffusion/inference/text2world.py",
                    "--checkpoint_dir", "checkpoints",
                    "--diffusion_transformer_dir", "Cosmos-Predict1-7B-Text2World",
                    "--prompt", task.prompts['prompt'],
                    "--offload_prompt_upsampler",
                    "--offload_text_encoder_model",
                    "--offload_tokenizer",
                    "--offload_diffusion_transformer",
                    "--offload_guardrail_models",
                    "--disable_prompt_upsampler",
                    "--disable_guardrail",
                    "--video_save_name", task.uuid
                ]
                
                # 设置单GPU环境变量
                env_vars = f"CUDA_VISIBLE_DEVICES={gpu_id}"
            
            # 构建完整的bash命令，正确处理包含空格的参数
            cmd_str = ' '.join(shlex.quote(arg) for arg in cmd)
            full_cmd = f"{conda_init} && {conda_activate} && cd {self.cosmos_base_path} && {env_vars} CUDA_HOME=$CONDA_PREFIX PYTHONPATH=$(pwd) {cmd_str}"
            
            logger.info(f"Executing command: {full_cmd}")
            
            # 执行命令
            process = subprocess.Popen(
                full_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                executable='/bin/bash'
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                logger.info(f"Video generation completed successfully for {task.uuid}")
                logger.info(f"Output: {stdout}")
                return True
            else:
                logger.error(f"Video generation failed for {task.uuid}")
                logger.error(f"Error: {stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Exception during video generation: {str(e)}")
            return False
    
    def _upload_video_to_s3(self, task_uuid: str, scene_type: str) -> bool:
        """上传生成的视频到S3并更新DynamoDB的video_link字段"""
        try:
            # S3配置
            s3_client = boto3.client('s3', region_name='us-east-1')
            s3_bucket = 'documents-distrubution'
            s3_folder = 'cosmos-video'
            cloudfront_domain = 'd3bb5kiveg9mt4.cloudfront.net'
            
            # 确定文件名
            if scene_type == 'SingleView':
                local_video = f"{task_uuid}.mp4"
            else:  # MultiView
                local_video = f"{task_uuid}_grid.mp4"
            
            local_path = f"{self.cosmos_base_path}/outputs/{local_video}"
            s3_key = f"{s3_folder}/{local_video}"
            
            # 检查本地文件是否存在
            if not os.path.exists(local_path):
                logger.error(f"Video file not found: {local_path}")
                return False
            
            logger.info(f"Found video file: {local_path}")
            file_size = os.path.getsize(local_path) / (1024 * 1024)  # MB
            logger.info(f"File size: {file_size:.2f} MB")
            
            # 上传到S3
            logger.info(f"Uploading to s3://{s3_bucket}/{s3_key}")
            s3_client.upload_file(
                local_path,
                s3_bucket,
                s3_key,
                ExtraArgs={'ContentType': 'video/mp4'}
            )
            
            # 生成CloudFront URL
            video_url = f"{cloudfront_domain}/{s3_key}"
            logger.info(f"CloudFront URL: https://{video_url}")
            
            # 更新DynamoDB的video_link字段
            logger.info(f"Updating DynamoDB video_link for task {task_uuid}")
            self.table.update_item(
                Key={'uuid': task_uuid},
                UpdateExpression='SET video_link = :url',
                ExpressionAttributeValues={':url': video_url}
            )
            
            logger.info(f"Successfully uploaded video and updated video_link for {task_uuid}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading video to S3: {str(e)}")
            return False
    
    def run(self, host='0.0.0.0', port=8080, debug=False):
        """启动Flask应用"""
        logger.info(f"Starting Cosmos API Service on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug, threaded=True)

def main():
    """主函数"""
    service = CosmosAPIService()
    service.run(
        host=Config.API_HOST,
        port=Config.API_PORT,
        debug=Config.API_DEBUG
    )

if __name__ == '__main__':
    main()
