#!/usr/bin/env python3
"""
WebSocket客户端模块，用于与场景增强API进行流式通信
"""

import websocket
import json
import threading
import time
import queue
import uuid
from typing import Callable, Optional, Dict, Any

class StreamingSceneEnhancer:
    """流式场景增强客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.websocket_url = "wss://qopfrzscp0.execute-api.us-west-2.amazonaws.com/prod"
        self.ws = None
        self.message_queue = queue.Queue()
        self.is_connected = False
        self.is_processing = False
        self.error_message = None
        self.connection_thread = None
        
    def on_message(self, ws, message):
        """接收消息回调"""
        try:
            data = json.loads(message)
            self.message_queue.put(('message', data))
        except json.JSONDecodeError:
            self.message_queue.put(('raw', message))
    
    def on_error(self, ws, error):
        """错误回调"""
        self.error_message = str(error)
        self.message_queue.put(('error', str(error)))
        self.is_connected = False
    
    def on_close(self, ws, close_status_code, close_msg):
        """关闭连接回调"""
        self.is_connected = False
        self.is_processing = False
        self.message_queue.put(('close', {'code': close_status_code, 'message': close_msg}))
    
    def on_open(self, ws):
        """连接建立回调"""
        self.is_connected = True
        self.message_queue.put(('open', 'Connected'))
    
    def connect(self) -> bool:
        """建立WebSocket连接"""
        try:
            self.ws = websocket.WebSocketApp(
                self.websocket_url,
                header={"x-api-key": self.api_key},
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # 在单独线程中运行WebSocket
            self.connection_thread = threading.Thread(
                target=self.ws.run_forever,
                daemon=True
            )
            self.connection_thread.start()
            
            # 等待连接建立
            timeout = 10
            start_time = time.time()
            while not self.is_connected and time.time() - start_time < timeout:
                time.sleep(0.1)
            
            return self.is_connected
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def send_enhancement_request(self, scene_description: str, scene_type: str) -> bool:
        """发送场景增强请求"""
        if not self.is_connected:
            return False
        
        try:
            # 生成UUID
            scene_uuid = str(uuid.uuid4())
            
            message = {
                "action": "process",
                "scene_description": scene_description,
                "SceneType": scene_type,  # 修改为大写S，与传统API保持一致
                "uuid": scene_uuid,
                "api_key": self.api_key
            }
            
            self.ws.send(json.dumps(message))
            self.is_processing = True
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def get_messages(self):
        """获取消息生成器"""
        while self.is_processing or not self.message_queue.empty():
            try:
                # 非阻塞获取消息
                message_type, data = self.message_queue.get(timeout=1.0)
                yield message_type, data
                
                # 如果收到完成消息，停止处理
                if message_type == 'message' and isinstance(data, dict):
                    if (data.get('type') == 'complete' or 
                        data.get('status') == 'completed' or
                        'full_response' in data or
                        'complete' in str(data).lower()):
                        self.is_processing = False
                        break
                elif message_type == 'error' or message_type == 'close':
                    self.is_processing = False
                    break
                    
            except queue.Empty:
                # 如果长时间没有消息，检查连接状态
                if not self.is_connected:
                    self.is_processing = False
                    break
                continue
            except Exception as e:
                yield 'error', str(e)
                break
    
    def close(self):
        """关闭连接"""
        self.is_processing = False
        if self.ws:
            self.ws.close()
        self.is_connected = False

def test_streaming_enhancer():
    """测试流式增强器"""
    enhancer = StreamingSceneEnhancer("C2G4GCEdCP2KMKYKZlpxgaX28k2ud4sxY4gEa3Zh")
    
    print("🔗 连接WebSocket...")
    if not enhancer.connect():
        print(f"❌ 连接失败: {enhancer.error_message}")
        return
    
    print("✅ 连接成功")
    
    # 发送测试请求
    print("📤 发送场景增强请求...")
    if not enhancer.send_enhancement_request("一个美丽的日落海滩场景", "SingleView"):
        print(f"❌ 发送请求失败: {enhancer.error_message}")
        return
    
    print("📨 接收流式响应...")
    for message_type, data in enhancer.get_messages():
        print(f"[{message_type}] {data}")
    
    enhancer.close()
    print("🔌 连接已关闭")

if __name__ == "__main__":
    test_streaming_enhancer()
