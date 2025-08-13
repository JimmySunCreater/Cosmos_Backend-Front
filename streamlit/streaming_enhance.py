#!/usr/bin/env python3
"""
流式场景增强模块
"""

import streamlit as st
import json
import uuid
import time
import threading
import queue
from websocket_client import StreamingSceneEnhancer

def call_streaming_enhance_api(scene_description, scene_type, api_key):
    """调用流式场景增强API"""
    scene_uuid = str(uuid.uuid4())
    
    # 创建流式增强器
    enhancer = StreamingSceneEnhancer(api_key)
    
    # 创建占位符用于显示流式内容
    status_placeholder = st.empty()
    content_placeholder = st.empty()
    progress_placeholder = st.empty()
    debug_placeholder = st.empty()  # 添加调试信息显示
    
    try:
        # 显示连接状态
        status_placeholder.info("🔗 正在连接WebSocket服务...")
        
        # 建立连接
        if not enhancer.connect():
            status_placeholder.error(f"❌ 连接失败: {enhancer.error_message}")
            return None, None
        
        status_placeholder.success("✅ WebSocket连接已建立")
        time.sleep(0.5)
        
        # 发送增强请求
        status_placeholder.info("📤 正在发送场景增强请求...")
        if not enhancer.send_enhancement_request(scene_description, scene_type):
            status_placeholder.error(f"❌ 发送请求失败: {enhancer.error_message}")
            return None, None
        
        status_placeholder.info("📨 正在接收流式响应...")
        
        # 初始化内容变量
        accumulated_content = ""
        final_result = None
        progress_bar = progress_placeholder.progress(0)
        progress_text = progress_placeholder.empty()
        
        # 处理流式消息
        message_count = 0
        for message_type, data in enhancer.get_messages():
            message_count += 1
            
            # 显示调试信息（简化版本，避免界面过于混乱）
            if message_count <= 5 or message_count % 20 == 0:  # 只显示前5条和每20条消息
                debug_placeholder.text(f"🔍 消息 {message_count}: {message_type} - {str(data)[:50]}...")
            elif message_count == 6:
                debug_placeholder.text(f"🔍 正在接收流式内容... (消息 {message_count}+)")
            
            if message_type == 'message':
                if isinstance(data, dict):
                    # 处理结构化消息
                    if 'type' in data:
                        if data['type'] == 'start':
                            # 开始处理
                            status_placeholder.info(f"🚀 {data.get('message', '开始处理...')}")
                            
                        elif data['type'] == 'content':
                            # 流式内容 - 这是主要的内容类型
                            text_content = data.get('text', '')
                            accumulated_content += text_content
                            content_placeholder.text_area(
                                "🔄 实时生成内容",
                                value=accumulated_content,
                                height=300,
                                disabled=True,
                                key=f"streaming_content_{message_count}"
                            )
                            # 更新进度
                            estimated_progress = min(len(accumulated_content) / 10, 90)  # 基于内容长度估算
                            progress_bar.progress(estimated_progress / 100)
                            progress_text.text(f"生成中... ({len(accumulated_content)} 字符)")
                            
                        elif data['type'] == 'progress':
                            # 进度更新
                            progress = data.get('progress', 0)
                            progress_bar.progress(min(progress / 100, 1.0))
                            progress_text.text(f"处理进度: {progress}%")
                            
                        elif data['type'] == 'complete':
                            # 完成
                            final_result = data.get('full_response', data.get('prompt_front', accumulated_content))
                            progress_bar.progress(1.0)
                            progress_text.text("✅ 生成完成!")
                            status_placeholder.success("🎉 场景描述生成完成!")
                            debug_placeholder.success(f"✅ 收到完成消息，最终结果长度: {len(final_result) if final_result else 0}")
                            break
                            
                        elif data['type'] == 'error':
                            # 错误处理
                            status_placeholder.error(f"❌ 处理错误: {data.get('message', '未知错误')}")
                            debug_placeholder.error(f"❌ 错误详情: {data}")
                            break
                            
                    # 处理其他可能的字段
                    elif 'content' in data:
                        # 直接内容更新
                        accumulated_content = data['content']
                        content_placeholder.text_area(
                            "🔄 实时生成内容",
                            value=accumulated_content,
                            height=300,
                            disabled=True,
                            key=f"streaming_content_{message_count}"
                        )
                        
                    elif 'full_response' in data:
                        # 最终结果
                        final_result = data['full_response']
                        progress_bar.progress(1.0)
                        progress_text.text("✅ 生成完成!")
                        status_placeholder.success("🎉 场景描述生成完成!")
                        debug_placeholder.success(f"✅ 收到完整响应，长度: {len(final_result)}")
                        break
                        
                else:
                    # 处理纯文本消息
                    accumulated_content += str(data)
                    content_placeholder.text_area(
                        "🔄 实时生成内容",
                        value=accumulated_content,
                        height=300,
                        disabled=True,
                        key=f"streaming_content_{message_count}"
                    )
                    
            elif message_type == 'error':
                status_placeholder.error(f"❌ 处理错误: {data}")
                debug_placeholder.error(f"❌ 错误详情: {data}")
                break
                
            elif message_type == 'close':
                if not final_result:
                    status_placeholder.warning("⚠️ 连接已关闭，可能未完成处理")
                    debug_placeholder.warning(f"⚠️ 连接关闭，累积内容长度: {len(accumulated_content)}")
                break
            
            # 更新进度（基于消息数量的估算）
            if message_type == 'message' and data.get('type') != 'progress':
                estimated_progress = min(message_count * 5, 90)
                progress_bar.progress(estimated_progress / 100)
        
        # 清理占位符
        progress_placeholder.empty()
        
        # 返回结果
        if final_result:
            debug_placeholder.success(f"✅ 返回最终结果，长度: {len(final_result)}")
            return scene_uuid, final_result
        elif accumulated_content:
            debug_placeholder.info(f"ℹ️ 返回累积内容，长度: {len(accumulated_content)}")
            return scene_uuid, accumulated_content
        else:
            debug_placeholder.error("❌ 未收到任何有效内容")
            status_placeholder.error("❌ 未收到有效响应")
            return None, None
            
    except Exception as e:
        status_placeholder.error(f"❌ 处理过程中出错: {str(e)}")
        debug_placeholder.error(f"❌ 异常详情: {str(e)}")
        return None, None
    finally:
        # 关闭连接
        enhancer.close()

def display_streaming_enhancement_ui():
    """显示流式增强界面"""
    st.subheader("🚀 流式场景增强")
    
    # 添加说明
    st.info("💡 使用WebSocket实现实时流式显示，可以看到场景描述的生成过程")
    
    # 输入区域
    col1, col2 = st.columns([3, 1])
    
    with col1:
        scene_description = st.text_area(
            "请输入简短的场景描述",
            placeholder="例如：雨后晚上的城市道路",
            height=100,
            key="streaming_scene_desc"
        )
    
    with col2:
        scene_type = st.selectbox(
            "选择场景类型",
            ["SingleView", "MultiView"],
            help="SingleView: 单视角场景，MultiView: 多视角场景",
            key="streaming_scene_type"
        )
        
        use_streaming = st.checkbox(
            "启用流式显示",
            value=True,
            help="实时显示生成过程"
        )
    
    # 生成按钮
    if st.button("🎬 开始流式生成", type="primary", key="streaming_generate"):
        if scene_description.strip():
            if use_streaming:
                # 使用流式API
                from config_streamlit import API_KEY
                scene_uuid, enhanced_description = call_streaming_enhance_api(
                    scene_description.strip(),
                    scene_type,
                    API_KEY
                )
            else:
                # 使用传统API作为备用
                from streamlit_app import call_enhance_api
                scene_uuid, enhanced_description = call_enhance_api(
                    scene_description.strip(),
                    scene_type
                )
            
            if scene_uuid and enhanced_description:
                st.success("✅ 场景描述生成成功！")
                
                # 显示UUID
                st.info(f"🆔 场景UUID: {scene_uuid}")
                
                # 显示最终结果
                st.subheader("📝 最终生成结果")
                st.text_area(
                    "增强后的场景描述",
                    value=enhanced_description,
                    height=200,
                    disabled=True,
                    key="final_result"
                )
                
                # 刷新场景列表
                if 'refresh_scenes' in st.session_state:
                    st.session_state.refresh_scenes = True
                    
        else:
            st.warning("⚠️ 请输入场景描述")

if __name__ == "__main__":
    # 测试界面
    st.title("流式场景增强测试")
    display_streaming_enhancement_ui()
