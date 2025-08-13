"""
响应式样式配置
提供自适应屏幕分辨率的CSS样式
"""

def get_responsive_css():
    """获取响应式CSS样式 - 针对4K显示器优化"""
    return """
    <style>
    /* JavaScript动态检测屏幕分辨率并应用样式 */
    <script>
    (function() {
        function applyScreenSpecificStyles() {
            const width = window.screen.width;
            const height = window.screen.height;
            const dpr = window.devicePixelRatio || 1;
            
            // 检测4K显示器
            if (width >= 3840 || height >= 2160) {
                document.documentElement.classList.add('screen-4k');
            } else if (width >= 2560 || height >= 1440) {
                document.documentElement.classList.add('screen-2k');
            } else if (width >= 1920) {
                document.documentElement.classList.add('screen-fhd');
            }
            
            // 高DPI显示器检测
            if (dpr >= 2) {
                document.documentElement.classList.add('high-dpi');
            }
        }
        
        // 页面加载时应用
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', applyScreenSpecificStyles);
        } else {
            applyScreenSpecificStyles();
        }
        
        // 窗口大小改变时重新应用
        window.addEventListener('resize', applyScreenSpecificStyles);
    })();
    </script>
    <style>
    /* 基础响应式设置 */
    .main > div {
        padding-top: 0rem !important;
        max-width: 100% !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    .stApp > header {
        height: 0rem;
    }
    
    /* 全局字体大小减小 */
    html, body, [class*="css"] {
        font-size: 13px !important; /* 原来14px，减小1px */
    }
    
    /* 标题字体调整 */
    h1 {
        font-size: 1.8rem !important; /* 减小 */
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important; /* 减小 */
        margin-bottom: 0.8rem !important;
    }
    
    h3 {
        font-size: 1.3rem !important; /* 减小 */
        margin-bottom: 0.6rem !important;
    }
    
    /* 侧边栏响应式 - 进一步缩窄 */
    .css-1d391kg {
        width: 180px !important; /* 从220px进一步减少到180px */
    }
    
    /* 按钮字体调整 */
    .stButton > button {
        font-size: 13px !important;
        padding: 0.4rem 0.8rem !important;
        height: auto !important;
    }
    
    /* 输入框字体调整 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        font-size: 13px !important;
    }
    
    /* 表格字体调整 */
    .dataframe {
        font-size: 12px !important;
    }
    
    /* 信息框字体调整 */
    .stAlert {
        font-size: 13px !important;
    }
    
    /* 代码块字体调整 */
    .stCode {
        font-size: 12px !important;
    }
    
    /* 响应式断点 - 4K超大屏幕 (2560px+) */
    @media (min-width: 2560px) {
        .block-container {
            max-width: 2200px !important;
            margin: 0 auto !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }
        
        .css-1d391kg {
            width: 320px !important; /* 4K屏幕侧边栏更宽 */
        }
        
        /* 4K屏幕字体大幅增大 */
        html, body, [class*="css"] {
            font-size: 18px !important;
        }
        
        h1 {
            font-size: 2.8rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        h2 {
            font-size: 2.2rem !important;
            margin-bottom: 1.2rem !important;
        }
        
        h3 {
            font-size: 1.8rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* 按钮在4K屏幕上更大 */
        .stButton > button {
            font-size: 16px !important;
            padding: 0.8rem 1.5rem !important;
            min-height: 50px !important;
        }
        
        /* 输入框在4K屏幕上更大 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            font-size: 16px !important;
            padding: 0.8rem !important;
            min-height: 50px !important;
        }
        
        /* 表格在4K屏幕上更大 */
        .dataframe {
            font-size: 16px !important;
        }
        
        /* 信息框在4K屏幕上更大 */
        .stAlert {
            font-size: 16px !important;
            padding: 1rem !important;
        }
        
        /* 代码块在4K屏幕上更大 */
        .stCode {
            font-size: 15px !important;
        }
        
        /* 侧边栏内容在4K屏幕上优化 */
        .css-1d391kg .stRadio label {
            font-size: 16px !important;
            padding: 0.6rem 0.8rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1.8rem !important;
            margin-bottom: 1rem !important;
        }
        
        .css-1d391kg .stButton > button {
            font-size: 14px !important;
            padding: 0.6rem 1rem !important;
        }
    }
    
    /* 响应式断点 - 2K大屏幕 (1920px - 2559px) */
    @media (min-width: 1920px) and (max-width: 2559px) {
        .block-container {
            max-width: 1800px !important;
            margin: 0 auto !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        .css-1d391kg {
            width: 280px !important; /* 2K屏幕侧边栏适中 */
        }
        
        /* 2K屏幕字体适中增大 */
        html, body, [class*="css"] {
            font-size: 16px !important;
        }
        
        h1 {
            font-size: 2.4rem !important;
            margin-bottom: 1.3rem !important;
        }
        
        h2 {
            font-size: 1.9rem !important;
            margin-bottom: 1rem !important;
        }
        
        h3 {
            font-size: 1.6rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* 按钮在2K屏幕上适中 */
        .stButton > button {
            font-size: 15px !important;
            padding: 0.6rem 1.2rem !important;
            min-height: 45px !important;
        }
        
        /* 输入框在2K屏幕上适中 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            font-size: 15px !important;
            padding: 0.6rem !important;
            min-height: 45px !important;
        }
        
        /* 表格在2K屏幕上适中 */
        .dataframe {
            font-size: 14px !important;
        }
        
        /* 侧边栏内容在2K屏幕上优化 */
        .css-1d391kg .stRadio label {
            font-size: 14px !important;
            padding: 0.5rem 0.7rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1.5rem !important;
            margin-bottom: 0.8rem !important;
        }
    }
    
    /* 响应式断点 - 标准大屏幕 (1200px - 1919px) */
    @media (min-width: 1200px) and (max-width: 1919px) {
        .block-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
        }
        
        .css-1d391kg {
            width: 240px !important; /* 标准大屏幕侧边栏 */
        }
        
        /* 标准大屏幕字体 */
        html, body, [class*="css"] {
            font-size: 15px !important;
        }
        
        h1 {
            font-size: 2.1rem !important;
            margin-bottom: 1.2rem !important;
        }
        
        h2 {
            font-size: 1.7rem !important;
            margin-bottom: 0.9rem !important;
        }
        
        h3 {
            font-size: 1.4rem !important;
            margin-bottom: 0.7rem !important;
        }
        
        /* 按钮在标准大屏幕上 */
        .stButton > button {
            font-size: 14px !important;
            padding: 0.5rem 1rem !important;
            min-height: 40px !important;
        }
        
        /* 输入框在标准大屏幕上 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            font-size: 14px !important;
            padding: 0.5rem !important;
            min-height: 40px !important;
        }
        
        /* 侧边栏内容在标准大屏幕上优化 */
        .css-1d391kg .stRadio label {
            font-size: 13px !important;
            padding: 0.4rem 0.6rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1.3rem !important;
            margin-bottom: 0.7rem !important;
        }
    }
    
    /* 响应式断点 - 中等屏幕 (768px - 1199px) */
    @media (min-width: 768px) and (max-width: 1199px) {
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        .css-1d391kg {
            width: 170px !important; /* 中等屏幕进一步缩窄 */
        }
        
        /* 列布局调整 */
        .row-widget.stRadio > div {
            flex-direction: column !important;
        }
    }
    
    /* 响应式断点 - 小屏幕 (576px - 767px) */
    @media (min-width: 576px) and (max-width: 767px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .css-1d391kg {
            width: 150px !important; /* 小屏幕更窄 */
        }
        
        /* 小屏幕字体进一步减小 */
        html, body, [class*="css"] {
            font-size: 12px !important;
        }
        
        h1 {
            font-size: 1.6rem !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        /* 按钮适配 */
        .stButton > button {
            font-size: 12px !important;
            padding: 0.3rem 0.6rem !important;
            width: 100% !important;
        }
        
        /* 表格滚动 */
        .dataframe {
            font-size: 11px !important;
            overflow-x: auto !important;
        }
    }
    
    /* 响应式断点 - 超小屏幕 (< 576px) */
    @media (max-width: 575px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        /* 侧边栏在小屏幕上收起 */
        .css-1d391kg {
            width: 140px !important; /* 超小屏幕最窄 */
        }
        
        /* 超小屏幕字体最小 */
        html, body, [class*="css"] {
            font-size: 11px !important;
        }
        
        h1 {
            font-size: 1.4rem !important;
            text-align: center !important;
        }
        
        h2 {
            font-size: 1.2rem !important;
        }
        
        h3 {
            font-size: 1rem !important;
        }
        
        /* 按钮全宽 */
        .stButton > button {
            font-size: 11px !important;
            padding: 0.3rem 0.5rem !important;
            width: 100% !important;
        }
        
        /* 输入框适配 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            font-size: 11px !important;
        }
        
        /* 表格适配 */
        .dataframe {
            font-size: 10px !important;
            overflow-x: auto !important;
        }
        
        /* 列布局在小屏幕上堆叠 */
        .row-widget > div {
            flex-direction: column !important;
        }
        
        /* 图片适配 */
        img {
            max-width: 100% !important;
            height: auto !important;
        }
    }
    
    /* 通用响应式图片 */
    img {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* 响应式表格 */
    .dataframe {
        width: 100% !important;
        overflow-x: auto !important;
    }
    
    /* 响应式文本区域 */
    .stTextArea > div > div > textarea {
        min-height: 80px !important;
        resize: vertical !important;
    }
    
    /* 响应式选择框 */
    .stSelectbox > div > div {
        width: 100% !important;
    }
    
    /* 响应式列布局 */
    .row-widget {
        width: 100% !important;
    }
    
    /* 响应式进度条 */
    .stProgress > div > div {
        width: 100% !important;
    }
    
    /* 响应式警告框 */
    .stAlert {
        margin: 0.5rem 0 !important;
        padding: 0.5rem !important;
    }
    
    /* 响应式代码块 */
    .stCode {
        overflow-x: auto !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    
    /* 响应式JSON显示 */
    .stJson {
        overflow-x: auto !important;
        font-size: 11px !important;
    }
    
    /* 侧边栏内容适配 - 针对更窄的侧边栏进一步优化 */
    .css-1d391kg .stRadio > div {
        gap: 0.1rem !important; /* 进一步减少间距 */
    }
    
    .css-1d391kg .stRadio label {
        font-size: 11px !important; /* 进一步减小字体 */
        line-height: 1.1 !important;
        padding: 0.25rem 0.4rem !important;
        word-wrap: break-word !important;
        white-space: normal !important;
    }
    
    /* 侧边栏标题优化 */
    .css-1d391kg h2 {
        font-size: 1rem !important; /* 进一步减小标题 */
        margin-bottom: 0.4rem !important;
        line-height: 1.2 !important;
    }
    
    /* 侧边栏图片适配 */
    .css-1d391kg img {
        max-width: 100% !important;
        height: auto !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* 侧边栏按钮优化 */
    .css-1d391kg .stButton > button {
        font-size: 10px !important;
        padding: 0.2rem 0.3rem !important;
        width: 100% !important;
    }
    
    /* 移动设备触摸优化 */
    @media (hover: none) and (pointer: coarse) {
        .stButton > button {
            min-height: 44px !important; /* 触摸友好的最小高度 */
        }
        
        .stSelectbox > div > div > select {
            min-height: 44px !important;
        }
    }
    
    /* 打印样式 */
    @media print {
        .css-1d391kg {
            display: none !important;
        }
        
        .block-container {
            max-width: 100% !important;
            padding: 0 !important;
        }
        
        .stButton {
            display: none !important;
        }
    }
    </style>
    """

def get_mobile_viewport_meta():
    """获取移动端视口meta标签"""
    return """
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """
