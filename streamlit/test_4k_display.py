"""
4K显示器测试页面
用于验证响应式布局和字体大小是否正确
"""

import streamlit as st
from responsive_styles_4k import get_4k_optimized_css, get_screen_detection_script, get_mobile_viewport_meta

def main():
    # 应用4K优化样式
    st.markdown(get_4k_optimized_css(), unsafe_allow_html=True)
    st.markdown(get_screen_detection_script(), unsafe_allow_html=True)
    st.markdown(get_mobile_viewport_meta(), unsafe_allow_html=True)
    
    st.title("🖥️ 4K显示器优化测试页面")
    
    # 显示屏幕信息
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
        <h3>📊 屏幕检测信息</h3>
        <p>请查看浏览器标题栏，会显示检测到的分辨率信息</p>
        <p>不同分辨率下的字体和布局会自动调整：</p>
        <ul>
            <li><strong>4K (3840x2160+)</strong>: 大字体 (20px)，宽布局 (3200px)</li>
            <li><strong>2K (2560x1440)</strong>: 中等字体 (17px)，适中布局 (2200px)</li>
            <li><strong>FHD (1920x1080)</strong>: 标准字体 (15px)，标准布局 (1600px)</li>
            <li><strong>标准 (1200px+)</strong>: 默认字体 (14px)，默认布局 (1400px)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 测试各种组件
    st.header("🧪 组件测试")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 输入组件测试")
        
        # 文本输入
        text_input = st.text_input("文本输入框", placeholder="请输入文本测试字体大小")
        
        # 文本区域
        text_area = st.text_area("文本区域", placeholder="请输入多行文本测试\n字体大小和区域高度", height=100)
        
        # 选择框
        select_option = st.selectbox("选择框", ["选项1", "选项2", "选项3"])
        
        # 按钮
        if st.button("测试按钮 - 检查字体大小"):
            st.success("✅ 按钮点击成功！字体大小应该根据屏幕分辨率自动调整")
    
    with col2:
        st.subheader("📊 信息显示")
        
        # 指标
        st.metric("测试指标", "1234", "56")
        
        # 信息框
        st.info("ℹ️ 这是信息框，字体大小会根据屏幕分辨率调整")
        st.success("✅ 这是成功信息框")
        st.warning("⚠️ 这是警告信息框")
        st.error("❌ 这是错误信息框")
    
    # 表格测试
    st.subheader("📋 表格测试")
    import pandas as pd
    
    test_data = pd.DataFrame({
        '列1': ['数据1', '数据2', '数据3'],
        '列2': ['测试A', '测试B', '测试C'],
        '列3': [100, 200, 300],
        '列4': ['这是较长的文本内容用于测试表格字体大小', '另一段文本', '第三段文本']
    })
    
    st.dataframe(test_data)
    
    # 代码块测试
    st.subheader("💻 代码块测试")
    
    code_example = '''
def test_function():
    """
    这是一个测试函数
    用于验证代码块的字体大小
    """
    print("Hello, 4K Display!")
    return "字体大小测试"
    '''
    
    st.code(code_example, language='python')
    
    # JSON测试
    st.subheader("📄 JSON显示测试")
    
    test_json = {
        "screen_optimization": "4K Display",
        "font_sizes": {
            "4K": "20px",
            "2K": "17px",
            "FHD": "15px",
            "Standard": "14px"
        },
        "layout_widths": {
            "4K": "3200px",
            "2K": "2200px",
            "FHD": "1600px",
            "Standard": "1400px"
        }
    }
    
    st.json(test_json)
    
    # 进度条测试
    st.subheader("📈 进度条测试")
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
        if i % 20 == 0:
            st.write(f"进度: {i+1}% - 字体大小测试")
    
    # 标签页测试
    st.subheader("📑 标签页测试")
    
    tab1, tab2, tab3 = st.tabs(["标签页1", "标签页2", "标签页3"])
    
    with tab1:
        st.write("这是第一个标签页的内容，用于测试标签页字体大小")
    
    with tab2:
        st.write("这是第二个标签页的内容")
    
    with tab3:
        st.write("这是第三个标签页的内容")
    
    # 侧边栏测试
    with st.sidebar:
        # 添加Amazon Logo测试
        st.image("amazon.png", caption="Amazon Logo - 大小会根据分辨率调整")
        
        st.header("🎛️ 侧边栏测试")
        st.write("侧边栏内容字体大小测试")
        
        sidebar_option = st.radio(
            "选择选项",
            ["选项A - 测试长文本显示", "选项B - 中等长度", "选项C"]
        )
        
        if st.button("侧边栏按钮"):
            st.write("侧边栏按钮被点击")
        
        st.subheader("📏 侧边栏尺寸信息")
        st.markdown("""
        **不同分辨率下的侧边栏宽度：**
        - 4K: 450px, Logo: 200px
        - 2K: 360px, Logo: 160px  
        - FHD: 300px, Logo: 130px
        - 标准: 260px, Logo: 110px
        - 中等: 220px, Logo: 90px
        - 小屏: 200px, Logo: 70px
        - 超小: 180px, Logo: 50px
        """)
        
        st.selectbox("测试选择框", ["选项1", "选项2", "选项3"])
    
    # 日志诊断页面测试
    st.subheader("📊 日志诊断页面测试")
    
    if st.button("🧪 测试日志诊断页面响应式"):
        st.info("日志诊断页面响应式特性：")
        st.markdown("""
        **不同分辨率下的优化：**
        - **4K (3840px+)**: iframe高度1800px+，大字体(18px)
        - **2K (2560px)**: iframe高度1200px+，中字体(16px)  
        - **FHD (1920px)**: iframe高度900px+，标准字体(15px)
        - **标准 (1200px)**: iframe高度700px+，默认字体(14px)
        - **中等 (768px)**: iframe高度500px+，小字体(13px)
        - **小屏 (576px)**: iframe高度400px+，更小字体(12px)，隐藏侧边栏
        - **超小 (<576px)**: iframe高度300px+，最小字体(11px)，完全隐藏侧边栏
        
        **特殊功能：**
        - 自动检测屏幕分辨率并调整布局
        - 小屏幕设备自动隐藏侧边栏
        - 支持全屏模式
        - 工具栏按钮大小自适应
        """)
    
    # iframe测试
    st.subheader("🖼️ iframe嵌入测试")
    
    test_iframe_height = st.slider("测试iframe高度", 200, 1000, 400)
    
    st.markdown(f"""
    <iframe src="data:text/html,
    <html>
    <head>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                background: linear-gradient(45deg, #f0f2f6, #e8eaf6);
                margin: 0;
            }}
            .test-content {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            h2 {{ color: #1f77b4; }}
            .screen-info {{
                background: #e3f2fd;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
                border-left: 4px solid #2196f3;
            }}
        </style>
    </head>
    <body>
        <div class='test-content'>
            <h2>📊 日志诊断页面测试内容</h2>
            <div class='screen-info'>
                <strong>当前屏幕信息：</strong><br>
                分辨率: <span id='resolution'></span><br>
                DPR: <span id='dpr'></span><br>
                窗口大小: <span id='window-size'></span>
            </div>
            <p>这是一个模拟的日志诊断页面内容，用于测试不同分辨率下的显示效果。</p>
            <p>在实际的日志页面中，这里会显示系统日志、错误信息、性能指标等内容。</p>
            <div style='margin-top: 20px; padding: 10px; background: #f5f5f5; border-radius: 4px; font-family: monospace; font-size: 12px;'>
                [2024-06-17 09:00:00] INFO: 系统启动成功<br>
                [2024-06-17 09:00:01] INFO: 加载配置文件<br>
                [2024-06-17 09:00:02] INFO: 连接数据库<br>
                [2024-06-17 09:00:03] INFO: 启动Web服务器<br>
                [2024-06-17 09:00:04] INFO: 系统就绪，等待请求
            </div>
        </div>
        <script>
            document.getElementById('resolution').textContent = screen.width + 'x' + screen.height;
            document.getElementById('dpr').textContent = window.devicePixelRatio || 1;
            document.getElementById('window-size').textContent = window.innerWidth + 'x' + window.innerHeight;
        </script>
    </body>
    </html>" 
    width="100%" height="{test_iframe_height}" frameborder="0"></iframe>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
    # 页脚信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🖥️ 4K显示器优化测试页面</p>
        <p>如果字体和布局看起来合适，说明优化生效了！</p>
        <p>📊 日志诊断页面也已经过响应式优化</p>
    </div>
    """, unsafe_allow_html=True)
