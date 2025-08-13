#!/usr/bin/env python3
"""
GPU管理器 - 管理GPU资源分配
"""

import threading
import time
import subprocess
import json
from typing import Optional, Set, Dict
import logging

logger = logging.getLogger(__name__)

class GPUManager:
    """GPU资源管理器"""
    
    def __init__(self, total_gpus: int = 8):
        self.total_gpus = total_gpus
        self.available_gpus: Set[int] = set(range(total_gpus))
        self.occupied_gpus: Dict[int, str] = {}  # gpu_id -> task_uuid
        self.lock = threading.Lock()
        
    def get_gpu_memory_usage(self) -> Dict[int, Dict]:
        """获取GPU内存使用情况"""
        try:
            result = subprocess.run([
                'nvidia-smi', '--query-gpu=index,memory.used,memory.total,utilization.gpu',
                '--format=csv,noheader,nounits'
            ], capture_output=True, text=True, check=True)
            
            gpu_info = {}
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    gpu_id = int(parts[0])
                    memory_used = int(parts[1])
                    memory_total = int(parts[2])
                    utilization = int(parts[3])
                    
                    gpu_info[gpu_id] = {
                        'memory_used': memory_used,
                        'memory_total': memory_total,
                        'utilization': utilization,
                        'memory_free': memory_total - memory_used
                    }
            return gpu_info
        except Exception as e:
            logger.error(f"Failed to get GPU memory usage: {e}")
            return {}
    
    def allocate_gpu_for_singleview(self, task_uuid: str) -> Optional[int]:
        """为SingleView任务分配一个GPU"""
        with self.lock:
            # 获取GPU内存使用情况
            gpu_info = self.get_gpu_memory_usage()
            
            # 找到内存使用最少的可用GPU
            best_gpu = None
            min_memory_used = float('inf')
            
            for gpu_id in self.available_gpus:
                if gpu_id in gpu_info:
                    memory_used = gpu_info[gpu_id]['memory_used']
                    # 只选择内存使用少于1GB的GPU（认为是空闲的）
                    if memory_used < 1024 and memory_used < min_memory_used:
                        min_memory_used = memory_used
                        best_gpu = gpu_id
            
            if best_gpu is not None:
                self.available_gpus.remove(best_gpu)
                self.occupied_gpus[best_gpu] = task_uuid
                logger.info(f"Allocated GPU {best_gpu} for SingleView task {task_uuid}")
                return best_gpu
            else:
                logger.warning(f"No available GPU for SingleView task {task_uuid}")
                return None
    
    def allocate_gpus_for_multiview(self, task_uuid: str) -> Optional[Set[int]]:
        """为MultiView任务分配所有8个GPU"""
        with self.lock:
            if len(self.available_gpus) == 8:  # 必须所有8个GPU都可用
                allocated_gpus = set(self.available_gpus)
                for gpu_id in allocated_gpus:
                    self.occupied_gpus[gpu_id] = task_uuid
                self.available_gpus.clear()
                logger.info(f"Allocated all 8 GPUs {allocated_gpus} for MultiView task {task_uuid}")
                return allocated_gpus
            else:
                logger.info(f"MultiView task {task_uuid} waiting for all GPUs. Available: {len(self.available_gpus)}/8")
                return None
    
    def release_gpu(self, gpu_id: int, task_uuid: str):
        """释放单个GPU"""
        with self.lock:
            if gpu_id in self.occupied_gpus and self.occupied_gpus[gpu_id] == task_uuid:
                del self.occupied_gpus[gpu_id]
                self.available_gpus.add(gpu_id)
                logger.info(f"Released GPU {gpu_id} from task {task_uuid}")
            else:
                logger.warning(f"GPU {gpu_id} was not allocated to task {task_uuid}")
    
    def release_gpus(self, gpu_ids: Set[int], task_uuid: str):
        """释放多个GPU"""
        with self.lock:
            for gpu_id in gpu_ids:
                if gpu_id in self.occupied_gpus and self.occupied_gpus[gpu_id] == task_uuid:
                    del self.occupied_gpus[gpu_id]
                    self.available_gpus.add(gpu_id)
            logger.info(f"Released GPUs {gpu_ids} from task {task_uuid}")
    
    def get_status(self) -> Dict:
        """获取GPU管理器状态"""
        with self.lock:
            gpu_info = self.get_gpu_memory_usage()
            return {
                'total_gpus': self.total_gpus,
                'available_gpus': list(self.available_gpus),
                'occupied_gpus': dict(self.occupied_gpus),
                'gpu_memory_info': gpu_info
            }
    
    def force_cleanup(self):
        """强制清理所有GPU分配（用于紧急情况）"""
        with self.lock:
            logger.warning("Force cleaning up all GPU allocations")
            self.occupied_gpus.clear()
            self.available_gpus = set(range(self.total_gpus))

# 全局GPU管理器实例
gpu_manager = GPUManager(total_gpus=8)
