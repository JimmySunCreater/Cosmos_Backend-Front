#!/usr/bin/env python3
"""
Cosmos视频生成场景管理系统 - Streamlit界面
"""

import streamlit as st
import requests
import uuid
import time
from config_streamlit import *
from responsive_styles_4k import get_4k_optimized_css, get_screen_detection_script, get_log_diagnosis_responsive_css
from responsive_layout import (
    responsive_columns, responsive_text_area
)

# 导入流式增强模块
try:
    from streaming_enhance import call_streaming_enhance_api
    STREAMING_AVAILABLE = True
except ImportError as e:
    STREAMING_AVAILABLE = False
    st.warning(f"流式功能不可用: {e}")

# 兼容性函数
def safe_rerun():
    """安全的页面刷新函数，兼容不同版本的Streamlit"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except AttributeError:
            st.write("页面将自动刷新...")
            time.sleep(0.1)

# 配置页面
st.set_page_config(**PAGE_CONFIG)

# 通用请求头
COMMON_HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# 初始化session state
if 'scenes' not in st.session_state:
    st.session_state.scenes = []
if 'selected_scene' not in st.session_state:
    st.session_state.selected_scene = None
if 'refresh_scenes' not in st.session_state:
    st.session_state.refresh_scenes = True

def call_enhance_api(scene_description, scene_type):
    """调用场景增强API"""
    scene_uuid = str(uuid.uuid4())
    
    payload = {
        "scene_description": scene_description,
        "uuid": scene_uuid,
        "SceneType": scene_type
    }
    
    try:
        with st.spinner(f"正在生成{scene_type}场景描述，请稍候..."):
            response = requests.post(
                ENHANCE_API_URL,
                headers=COMMON_HEADERS,
                json=payload,
                timeout=120
            )
        
        if response.status_code == 200:
            return scene_uuid, response.text
        else:
            st.error(f"API调用失败: {response.status_code} - {response.text}")
            return None, None
            
    except requests.exceptions.Timeout:
        st.error("请求超时，请稍后重试")
        return None, None
    except Exception as e:
        st.error(f"请求失败: {str(e)}")
        return None, None

def get_scenes_from_library():
    """从场景库获取所有场景"""
    try:
        response = requests.get(
            LIBRARY_API_URL,
            headers=COMMON_HEADERS,
            params={"limit": 100}
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            st.error(f"获取场景列表失败: {response.status_code}")
            return []
            
    except Exception as e:
        st.error(f"获取场景列表失败: {str(e)}")
        return []


def delete_scene(scene_uuid):
    """删除场景"""
    try:
        response = requests.delete(
            f"{LIBRARY_API_URL}/{scene_uuid}",
            headers=COMMON_HEADERS
        )
        
        if response.status_code == 204:
            st.success("场景删除成功！")
            st.session_state.refresh_scenes = True
            return True
        else:
            st.error(f"删除失败: {response.status_code}")
            return False
            
    except Exception as e:
        st.error(f"删除失败: {str(e)}")
        return False

def submit_video_generation(scene_uuid):
    """提交视频生成任务"""
    try:
        response = requests.post(
            f"{COSMOS_API_URL}/generate",
            headers=COMMON_HEADERS,
            json={"uuid": scene_uuid}
        )
        
        if response.status_code == 200:
            data = response.json()
            st.success(f"视频生成任务提交成功！")
            st.info(f"任务UUID: {scene_uuid}")
            st.info(f"场景类型: {data.get('scene_type', 'Unknown')}")
            st.info(f"队列位置: {data.get('queue_position', 'Unknown')}")
            return True
        else:
            st.error(f"提交失败: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        st.error(f"提交失败: {str(e)}")
        return False

def main():
    # 应用4K优化的响应式CSS样式
    st.markdown(get_4k_optimized_css(), unsafe_allow_html=True)
    
    # 添加屏幕检测脚本
    st.markdown(get_screen_detection_script(), unsafe_allow_html=True)
    
    st.title("Cosmos视频生成场景管理系统")
    
    # 侧边栏
    with st.sidebar:
        # 在侧边栏顶部显示Amazon logo
        try:
            st.image("/home/ubuntu/cosmos_service/streamlit/amazon.png", width=144)  # 120 * 1.2 = 144
        except Exception as e:
            st.error(f"无法加载Amazon logo: {str(e)}")
        
        st.header("功能导航")
        page = st.radio(
            "选择功能",
            ["场景生成", "场景管理", "视频生成", "日志诊断"]
        )
    
    if page == "场景生成":
        show_scene_generation()
    elif page == "场景管理":
        show_scene_management()
    elif page == "视频生成":
        show_video_generation()
    elif page == "日志诊断":
        show_log_diagnosis()

def show_scene_generation():
    """场景生成页面"""
    st.header("场景描述生成")
    
    col1, col2 = responsive_columns([2, 1])
    
    with col1:
        # 标题和启用流式生成选项放在同一行
        title_col1, title_col2 = st.columns([3, 1])
        
        with title_col1:
            st.subheader("输入简短场景描述")
        
        with title_col2:
            # 添加生成模式选择
            if STREAMING_AVAILABLE:
                use_streaming = st.checkbox(
                    "启用流式生成",
                    value=False,
                    help="实时显示生成过程，可以看到内容逐步生成"
                )
            else:
                use_streaming = False
                st.info("流式生成功能不可用，使用传统生成模式")
        
        # 文本输入区域
        scene_description = responsive_text_area(
            "",
            placeholder="例如：雨后晚上的城市道路",
            height=100
        )
        
        scene_type = st.selectbox(
            "选择场景类型",
            ["SingleView", "MultiView"],
            help="SingleView: 单视角场景，MultiView: 多视角场景"
        )
        
        if st.button("生成增强场景描述", type="primary"):
            if scene_description.strip():
                if use_streaming and STREAMING_AVAILABLE:
                    # 使用流式生成
                    scene_uuid, enhanced_description = call_streaming_enhance_api(
                        scene_description.strip(),
                        scene_type,
                        API_KEY
                    )
                else:
                    # 使用传统生成
                    scene_uuid, enhanced_description = call_enhance_api(
                        scene_description.strip(), 
                        scene_type
                    )
                
                if scene_uuid and enhanced_description:
                    st.success("场景描述生成成功！")
                    st.session_state.refresh_scenes = True
                    
                    # 显示生成的UUID
                    st.info(f"场景UUID: {scene_uuid}")
                    
                    # 显示增强后的描述
                    st.subheader("增强后的场景描述")
                    st.text_area(
                        "生成结果",
                        value=enhanced_description,
                        height=200,
                        disabled=True
                    )
            else:
                st.warning("请输入场景描述")
    
    with col2:
        st.subheader("使用说明")
        st.info("""
        **场景类型说明：**
        
        **SingleView**
        - 单一视角场景
        - 生成前方视角描述
        - 适合简单场景
        
        **MultiView**
        - 多视角场景
        - 生成6个视角描述
        - 适合复杂场景
        
        **注意事项：**
        - 描述尽量具体清晰
        - 生成后自动保存到场景库
        """)
        
        # 显示API状态
        if STREAMING_AVAILABLE:
            st.subheader("流式生成")
            st.success("WebSocket流式API可用")
            st.info("""
            **流式生成特点：**
            - 实时显示生成过程
            - 可以看到内容逐步生成
            - 支持进度显示
            - 使用WebSocket连接
            """)
        else:
            st.subheader("流式生成")
            st.warning("流式生成功能不可用")
        
        st.subheader("传统生成")
        st.info("""
        **传统生成特点：**
        - 等待完成后显示结果
        - 使用REST API
        - 生成完成后一次性显示
        - 稳定可靠
        """)

def show_scene_management():
    """场景管理页面"""
    # 标题和刷新按钮放在同一行
    title_col1, title_col2 = st.columns([3, 1])
    
    with title_col1:
        st.header("场景库管理")
    
    with title_col2:
        if st.button("刷新列表", type="secondary"):
            st.session_state.refresh_scenes = True
            safe_rerun()
    
    # 刷新场景列表
    if st.session_state.refresh_scenes:
        st.session_state.scenes = get_scenes_from_library()
        st.session_state.refresh_scenes = False
    
    # 调整列比例：左侧更宽，右侧更窄
    col1, col2 = responsive_columns([2, 1])
    
    with col1:
        # 删除场景列表标题，内容直接开始
        if st.session_state.scenes:
            # 创建场景选择框
            scene_options = []
            for scene in st.session_state.scenes:
                scene_type = scene.get('SceneType', 'Unknown')
                description = scene.get('scene_description', 'No description')[:50]
                scene_options.append(f"{scene_type} - {description}...")
            
            selected_index = st.selectbox(
                "选择场景",
                range(len(scene_options)),
                format_func=lambda x: scene_options[x]
            )
            
            if selected_index is not None:
                st.session_state.selected_scene = st.session_state.scenes[selected_index]
                
                # 检查是否有视频链接，如果有则显示播放器
                selected_scene = st.session_state.scenes[selected_index]
                video_link = selected_scene.get('video_link')
                
                if video_link:
                    st.markdown("---")
                    st.subheader("视频播放")
                    
                    # 处理视频链接格式
                    if video_link.startswith('http'):
                        video_url = video_link
                    else:
                        # 如果是S3路径，添加https前缀
                        video_url = f"https://{video_link}"
                    
                    try:
                        # 显示视频播放器
                        st.video(video_url)
                        st.success(f"视频已生成完成")
                        st.info(f"视频链接: {video_url}")
                        
                        # 添加下载链接
                        st.markdown(f"[下载视频]({video_url})")
                        
                    except Exception as e:
                        st.error(f"视频播放失败: {str(e)}")
                        st.info(f"视频链接: {video_url}")
                        st.markdown(f"[直接访问视频]({video_url})")
                else:
                    st.markdown("---")
                    st.info("该场景暂无生成的视频")
        else:
            st.info("暂无场景数据")
    
    with col2:
        st.subheader("场景详情")
        
        if st.session_state.selected_scene:
            scene = st.session_state.selected_scene
            
            # 显示完整UUID
            st.markdown(f"**UUID:** {scene.get('uuid', 'N/A')}")
            st.markdown(f"**类型:** {scene.get('SceneType', 'N/A')}")
            st.markdown(f"**更新:** {scene.get('update_time', 'N/A')[:10] if scene.get('update_time') else 'N/A'}")
            
            # 显示原始描述（适配页面宽度）
            st.markdown("**原始描述**")
            st.text_area(
                "场景描述",
                value=scene.get('scene_description', ''),
                height=80,
                key="original_desc_compact",
                disabled=True
            )
            
            # 显示增强后的描述
            if scene.get('SceneType') == 'SingleView':
                st.markdown("**前方视角描述**")
                st.text_area(
                    "PROMPT_FRONT",
                    value=scene.get('PROMPT_FRONT', ''),
                    height=120,
                    key="front_desc_compact",
                    disabled=True
                )
            else:
                # MultiView显示所有视角（适配页面宽度）
                st.markdown("**多视角描述**")
                views = [
                    ("前方", "PROMPT_FRONT"),
                    ("左前", "PROMPT_FRONT_LEFT"),
                    ("右前", "PROMPT_FRONT_RIGHT"),
                    ("后方", "PROMPT_BACK"),
                    ("左后", "PROMPT_BACK_LEFT"),
                    ("右后", "PROMPT_BACK_RIGHT")
                ]
                
                # 使用tabs显示不同视角，适配页面宽度
                view_tabs = st.tabs([view_name for view_name, _ in views])
                for tab, (view_name, view_key) in zip(view_tabs, views):
                    with tab:
                        st.text_area(
                            view_key,
                            value=scene.get(view_key, ''),
                            height=100,
                            key=f"{view_key}_compact",
                            disabled=True
                        )
            
            # 操作按钮
            st.markdown("---")
            if st.button("删除场景", type="secondary", use_container_width=True):
                st.session_state.show_delete_confirm = True
            
        else:
            st.info("请从左侧选择场景")
    
    # 删除确认对话框（移到列外面）
    if st.session_state.get('show_delete_confirm', False):
        st.warning("确定要删除这个场景吗？此操作无法撤销！")
        col_confirm, col_cancel = responsive_columns([1, 1])
        
        with col_confirm:
            if st.button("确认删除", type="primary"):
                delete_scene(st.session_state.selected_scene['uuid'])
                st.session_state.show_delete_confirm = False
                safe_rerun()
        
        with col_cancel:
            if st.button("取消", type="secondary"):
                st.session_state.show_delete_confirm = False
                safe_rerun()

def show_video_generation():
    """视频生成页面"""
    st.header("视频生成")
    
    # 刷新场景列表
    if st.session_state.refresh_scenes:
        st.session_state.scenes = get_scenes_from_library()
        st.session_state.refresh_scenes = False
    
    col1, col2 = responsive_columns([2, 1])  # 改为与场景管理页面一致的比例
    
    with col1:
        st.subheader("选择场景")
        
        if st.session_state.scenes:
            # 创建场景选择框
            scene_options = []
            for i, scene in enumerate(st.session_state.scenes):
                scene_type = scene.get('SceneType', 'Unknown')
                description = scene.get('scene_description', 'No description')[:50]
                scene_options.append(f"{scene_type} - {description}...")
            
            selected_index = st.selectbox(
                "选择要生成视频的场景",
                range(len(scene_options)),
                format_func=lambda x: scene_options[x],
                key="video_scene_select"
            )
            
            if selected_index is not None:
                selected_scene = st.session_state.scenes[selected_index]
                
                # 显示场景预览
                st.subheader("场景预览")
                st.write(f"**类型:** {selected_scene.get('SceneType', 'N/A')}　　**UUID:** {selected_scene.get('uuid', 'N/A')}")
                st.text_area(
                    "场景描述",
                    value=selected_scene.get('scene_description', ''),
                    height=100,
                    disabled=True
                )
                
                # 提交按钮
                if st.button("提交视频生成任务", type="primary"):
                    submit_video_generation(selected_scene['uuid'])
                
                # 查询任务状态
                st.subheader("任务状态查询")
                if st.button("查询当前任务状态"):
                    check_task_status(selected_scene['uuid'])
        else:
            st.info("暂无可用场景，请先生成场景描述")
    
    with col2:
        st.subheader("系统状态")
        
        # 添加检查按钮，样式与场景详情一致
        if st.button("检查系统状态", type="secondary", use_container_width=True):
            check_system_status()
        
        st.markdown("---")
        
        st.subheader("生成说明")
        st.info("""
        **视频生成流程：**
        
        1. 选择已生成的场景
        2. 点击提交生成任务
        3. 系统自动处理视频生成
        4. 完成后可通过API查询结果
        
        **注意事项：**
        - 确保场景描述完整
        - 生成过程中请勿重复提交
        - 可通过状态查询查看进度
        """)

def check_task_status(task_uuid):
    """查询任务状态"""
    try:
        response = requests.get(f"{COSMOS_API_URL}/status/{task_uuid}")
        if response.status_code == 200:
            data = response.json()
            status = data.get('generation_status', 'Unknown')
            
            if status == 'Waiting':
                st.info(f"任务状态: 等待中")
            elif status == 'Generating':
                st.warning(f"任务状态: 生成中")
            elif status == 'Finished':
                st.success(f"任务状态: 已完成")
                video_link = data.get('video_link')
                if video_link:
                    st.success(f"视频链接: https://{video_link}")
            elif status == 'Failed':
                st.error(f"任务状态: 失败")
            else:
                st.info(f"任务状态: {status}")
            
            # 显示详细信息
            with st.expander("详细信息"):
                st.json(data)
        elif response.status_code == 404:
            try:
                error_data = response.json()
                if error_data.get('error') == 'Task not found':
                    st.warning(f"任务未找到: {task_uuid}")
                    st.info("请确认UUID是否正确，或任务是否已提交")
                else:
                    st.error(f"查询失败: {error_data.get('error', '未知错误')}")
            except:
                st.error(f"任务未找到: {task_uuid}")
        else:
            st.error(f"查询失败: HTTP {response.status_code}")
            try:
                error_data = response.json()
                st.error(f"错误详情: {error_data}")
            except:
                st.error(f"响应内容: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("无法连接到API服务，请检查服务是否运行")
    except requests.exceptions.Timeout:
        st.error("请求超时，请稍后重试")
    except Exception as e:
        st.error(f"查询失败: {str(e)}")

def check_system_status():
    """检查系统状态"""
    try:
        response = requests.get(f"{COSMOS_API_URL}/health")
        if response.status_code == 200:
            data = response.json()
            st.success("系统运行正常")
            
            # 直接从API响应中获取GPU状态
            gpu_status_detail = data.get('gpu_status_detail', '0/8 GPUs available')
            # 提取格式为"X/Y"的部分
            gpu_status = gpu_status_detail.split()[0]  # 获取"0/8"部分
            
            # 使用HTML表格显示指标，确保对齐
            metrics_html = f"""
            <div style="text-align: center; font-family: monospace;">
                <div style="font-weight: bold; margin-bottom: 5px;">
                    活跃任务&nbsp;&nbsp;&nbsp;&nbsp;可用GPU&nbsp;&nbsp;&nbsp;&nbsp;队列任务
                </div>
                <div style="font-weight: bold; font-size: 1.1em;">
                    {data.get('active_tasks', 0)}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{gpu_status}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{data.get('queue_size', 0)}
                </div>
            </div>
            """
            st.markdown(metrics_html, unsafe_allow_html=True)
            
            # 显示详细状态
            with st.expander("详细状态"):
                st.json(data)
        else:
            st.error("系统状态异常")
    except Exception as e:
        st.error(f"无法连接到视频生成服务: {str(e)}")

def show_log_diagnosis():
    """日志诊断页面 - 4K优化版"""
    # 应用日志诊断页面专用的响应式样式
    st.markdown(get_log_diagnosis_responsive_css(), unsafe_allow_html=True)
    
    # 嵌入日志页面，根据屏幕分辨率动态调整高度
    st.markdown("""
    <script>
    // 根据屏幕分辨率动态设置iframe高度
    function setIframeHeight() {
        const screenWidth = window.screen.width;
        const screenHeight = window.screen.height;
        let height;
        
        if (screenWidth >= 3840 || screenHeight >= 2160) {
            // 4K屏幕
            height = Math.max(screenHeight - 200, 1800);
        } else if (screenWidth >= 2560) {
            // 2K屏幕
            height = Math.max(screenHeight - 160, 1200);
        } else if (screenWidth >= 1920) {
            // Full HD屏幕
            height = Math.max(screenHeight - 140, 900);
        } else if (screenWidth >= 1200) {
            // 标准大屏幕
            height = Math.max(screenHeight - 120, 700);
        } else if (screenWidth >= 768) {
            // 中等屏幕
            height = Math.max(screenHeight - 100, 500);
        } else if (screenWidth >= 576) {
            // 小屏幕
            height = Math.max(screenHeight - 80, 400);
        } else {
            // 超小屏幕
            height = Math.max(screenHeight - 60, 300);
        }
        
        // 查找iframe并设置高度
        setTimeout(function() {
            const iframe = document.querySelector('iframe');
            if (iframe) {
                iframe.style.height = height + 'px';
            }
        }, 500);
    }
    
    // 页面加载时设置
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setIframeHeight);
    } else {
        setIframeHeight();
    }
    
    // 窗口大小改变时重新设置
    window.addEventListener('resize', setIframeHeight);
    
    // 定期检查并调整（确保生效）
    setInterval(setIframeHeight, 2000);
    </script>
    """, unsafe_allow_html=True)
    
    # 嵌入日志页面
    try:
        import streamlit.components.v1 as components
        
        # 根据屏幕大小计算初始高度
        components.iframe(
            src=f"{COSMOS_LOG_URL}/logs",
            height=800,  # 初始高度，会被JavaScript动态调整
            scrolling=True
        )
    except Exception as e:
        st.error(f"无法加载日志页面: {str(e)}")
        st.markdown(f"请直接访问: [{COSMOS_LOG_URL}/logs]({COSMOS_LOG_URL}/logs)")

if __name__ == "__main__":
    main()
