"""
4K显示器优化的响应式样式配置
专门针对高分辨率显示器进行优化
"""

def get_4k_optimized_css():
    """获取4K优化的响应式CSS样式"""
    return """
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
    
    /* 默认字体大小 - 适合普通屏幕 */
    html, body, [class*="css"] {
        font-size: 14px !important;
    }
    
    /* 标题字体 */
    h1 {
        font-size: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 1.6rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    h3 {
        font-size: 1.4rem !important;
        margin-bottom: 0.6rem !important;
    }
    
    /* 侧边栏默认设置 */
    .css-1d391kg {
        width: 240px !important;
    }
    
    /* 按钮默认设置 */
    .stButton > button {
        font-size: 14px !important;
        padding: 0.5rem 1rem !important;
        height: auto !important;
        min-height: 40px !important;
    }
    
    /* 输入框默认设置 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        font-size: 14px !important;
        padding: 0.5rem !important;
        min-height: 40px !important;
    }
    
    /* 表格默认设置 */
    .dataframe {
        font-size: 13px !important;
    }
    
    /* 信息框默认设置 */
    .stAlert {
        font-size: 14px !important;
        padding: 0.8rem !important;
    }
    
    /* 代码块默认设置 */
    .stCode {
        font-size: 13px !important;
    }
    
    /* 4K超大屏幕优化 (3840x2160及以上) */
    @media (min-width: 3840px), (min-height: 2160px) {
        .block-container {
            max-width: 3200px !important;
            margin: 0 auto !important;
            padding-left: 4rem !important;
            padding-right: 4rem !important;
        }
        
        .css-1d391kg {
            width: 450px !important; /* 4K屏幕侧边栏更宽 */
            padding: 2rem 1.5rem !important; /* 增加内边距 */
        }
        
        /* 4K屏幕Amazon Logo优化 */
        .css-1d391kg img[src*="amazon.png"], 
        .css-1d391kg img[alt*="Amazon"],
        .css-1d391kg img[alt*="amazon"] {
            width: 200px !important; /* 4K屏幕logo更大 */
            height: auto !important;
            margin-bottom: 2rem !important;
            margin-top: 1rem !important;
        }
        
        /* 侧边栏所有图片统一处理 */
        .css-1d391kg img {
            max-width: 200px !important;
            height: auto !important;
            margin-bottom: 1.5rem !important;
        }
        
        /* 4K屏幕字体大幅增大 */
        html, body, [class*="css"] {
            font-size: 20px !important;
        }
        
        h1 {
            font-size: 3.2rem !important;
            margin-bottom: 2rem !important;
        }
        
        h2 {
            font-size: 2.6rem !important;
            margin-bottom: 1.6rem !important;
        }
        
        h3 {
            font-size: 2.2rem !important;
            margin-bottom: 1.2rem !important;
        }
        
        /* 按钮在4K屏幕上更大 */
        .stButton > button {
            font-size: 18px !important;
            padding: 1rem 2rem !important;
            min-height: 60px !important;
        }
        
        /* 输入框在4K屏幕上更大 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            font-size: 18px !important;
            padding: 1rem !important;
            min-height: 60px !important;
        }
        
        /* 文本区域在4K屏幕上更高 */
        .stTextArea > div > div > textarea {
            min-height: 120px !important;
        }
        
        /* 表格在4K屏幕上更大 */
        .dataframe {
            font-size: 18px !important;
        }
        
        .dataframe th, .dataframe td {
            padding: 12px !important;
        }
        
        /* 信息框在4K屏幕上更大 */
        .stAlert {
            font-size: 18px !important;
            padding: 1.5rem !important;
        }
        
        /* 代码块在4K屏幕上更大 */
        .stCode {
            font-size: 16px !important;
            padding: 1rem !important;
        }
        
        /* 侧边栏内容在4K屏幕上优化 */
        .css-1d391kg .stRadio label {
            font-size: 18px !important;
            padding: 1rem 1.2rem !important;
            line-height: 1.4 !important;
            margin-bottom: 0.5rem !important;
        }
        
        .css-1d391kg .stRadio > div {
            gap: 0.8rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 2.2rem !important;
            margin-bottom: 1.5rem !important;
            margin-top: 1rem !important;
        }
        
        .css-1d391kg h3 {
            font-size: 1.8rem !important;
            margin-bottom: 1rem !important;
        }
        
        .css-1d391kg .stButton > button {
            font-size: 16px !important;
            padding: 1rem 1.5rem !important;
            min-height: 55px !important;
            width: 100% !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* 选择框在4K屏幕上优化 */
        .css-1d391kg .stSelectbox > div > div > select {
            font-size: 16px !important;
            padding: 1rem !important;
            min-height: 55px !important;
        }
        
        .css-1d391kg .stSelectbox label {
            font-size: 16px !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* 侧边栏文本优化 */
        .css-1d391kg p, .css-1d391kg div {
            font-size: 16px !important;
            line-height: 1.5 !important;
        }
        
        /* 侧边栏分隔线 */
        .css-1d391kg hr {
            margin: 2rem 0 !important;
            border-width: 2px !important;
        }
        
        /* 指标显示在4K屏幕上更大 */
        .metric-container {
            padding: 1.5rem !important;
        }
        
        .metric-container .metric-value {
            font-size: 2.5rem !important;
        }
        
        .metric-container .metric-label {
            font-size: 1.2rem !important;
        }
        
        /* 进度条在4K屏幕上更高 */
        .stProgress > div > div {
            height: 20px !important;
        }
        
        /* JSON显示在4K屏幕上优化 */
        .stJson {
            font-size: 16px !important;
            padding: 1rem !important;
        }
        
        /* 标签页在4K屏幕上优化 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 18px !important;
            padding: 1rem 2rem !important;
        }
    }
    
    /* 2K/QHD屏幕优化 (2560x1440) */
    @media (min-width: 2560px) and (max-width: 3839px) {
        .block-container {
            max-width: 2200px !important;
            margin: 0 auto !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }
        
        .css-1d391kg {
            width: 360px !important; /* 2K屏幕侧边栏适中 */
            padding: 1.5rem 1.2rem !important;
        }
        
        /* 2K屏幕Amazon Logo优化 */
        .css-1d391kg img[src*="amazon.png"], 
        .css-1d391kg img[alt*="Amazon"],
        .css-1d391kg img[alt*="amazon"] {
            width: 160px !important; /* 2K屏幕logo适中 */
            height: auto !important;
            margin-bottom: 1.5rem !important;
            margin-top: 0.8rem !important;
        }
        
        /* 侧边栏所有图片统一处理 */
        .css-1d391kg img {
            max-width: 160px !important;
            height: auto !important;
            margin-bottom: 1.2rem !important;
        }
        
        /* 2K屏幕字体适中增大 */
        html, body, [class*="css"] {
            font-size: 17px !important;
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
        
        /* 按钮在2K屏幕上适中 */
        .stButton > button {
            font-size: 16px !important;
            padding: 0.8rem 1.5rem !important;
            min-height: 50px !important;
        }
        
        /* 输入框在2K屏幕上适中 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            font-size: 16px !important;
            padding: 0.8rem !important;
            min-height: 50px !important;
        }
        
        /* 表格在2K屏幕上适中 */
        .dataframe {
            font-size: 15px !important;
        }
        
        /* 侧边栏内容在2K屏幕上优化 */
        .css-1d391kg .stRadio label {
            font-size: 15px !important;
            padding: 0.8rem 1rem !important;
            margin-bottom: 0.4rem !important;
        }
        
        .css-1d391kg .stRadio > div {
            gap: 0.6rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1.8rem !important;
            margin-bottom: 1.2rem !important;
            margin-top: 0.8rem !important;
        }
        
        .css-1d391kg h3 {
            font-size: 1.5rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        .css-1d391kg .stButton > button {
            font-size: 14px !important;
            padding: 0.8rem 1.2rem !important;
            min-height: 48px !important;
            margin-bottom: 0.6rem !important;
        }
        
        .css-1d391kg .stSelectbox > div > div > select {
            font-size: 14px !important;
            padding: 0.8rem !important;
            min-height: 48px !important;
        }
        
        .css-1d391kg p, .css-1d391kg div {
            font-size: 14px !important;
            line-height: 1.4 !important;
        }
    }
    
    /* Full HD屏幕优化 (1920x1080) */
    @media (min-width: 1920px) and (max-width: 2559px) {
        .block-container {
            max-width: 1600px !important;
            margin: 0 auto !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        .css-1d391kg {
            width: 300px !important; /* Full HD屏幕侧边栏 */
            padding: 1.2rem 1rem !important;
        }
        
        /* Full HD屏幕Amazon Logo优化 */
        .css-1d391kg img[src*="amazon.png"], 
        .css-1d391kg img[alt*="Amazon"],
        .css-1d391kg img[alt*="amazon"] {
            width: 130px !important; /* Full HD屏幕logo标准 */
            height: auto !important;
            margin-bottom: 1.2rem !important;
            margin-top: 0.6rem !important;
        }
        
        /* 侧边栏所有图片统一处理 */
        .css-1d391kg img {
            max-width: 130px !important;
            height: auto !important;
            margin-bottom: 1rem !important;
        }
        
        /* Full HD屏幕字体 */
        html, body, [class*="css"] {
            font-size: 15px !important;
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
        
        /* 按钮在Full HD屏幕上 */
        .stButton > button {
            font-size: 15px !important;
            padding: 0.6rem 1.2rem !important;
            min-height: 45px !important;
        }
        
        /* 输入框在Full HD屏幕上 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            font-size: 15px !important;
            padding: 0.6rem !important;
            min-height: 45px !important;
        }
        
        /* 侧边栏内容在Full HD屏幕上优化 */
        .css-1d391kg .stRadio label {
            font-size: 14px !important;
            padding: 0.6rem 0.8rem !important;
            margin-bottom: 0.3rem !important;
        }
        
        .css-1d391kg .stRadio > div {
            gap: 0.4rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1.6rem !important;
            margin-bottom: 1rem !important;
            margin-top: 0.6rem !important;
        }
        
        .css-1d391kg h3 {
            font-size: 1.3rem !important;
            margin-bottom: 0.6rem !important;
        }
        
        .css-1d391kg .stButton > button {
            font-size: 13px !important;
            padding: 0.6rem 1rem !important;
            min-height: 42px !important;
            margin-bottom: 0.5rem !important;
        }
        
        .css-1d391kg .stSelectbox > div > div > select {
            font-size: 13px !important;
            padding: 0.6rem !important;
            min-height: 42px !important;
        }
        
        .css-1d391kg p, .css-1d391kg div {
            font-size: 13px !important;
            line-height: 1.3 !important;
        }
    }
    
    /* 标准大屏幕 (1200px - 1919px) */
    @media (min-width: 1200px) and (max-width: 1919px) {
        .block-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
        }
        
        .css-1d391kg {
            width: 260px !important;
            padding: 1rem 0.8rem !important;
        }
        
        /* 标准大屏幕Amazon Logo优化 */
        .css-1d391kg img[src*="amazon.png"], 
        .css-1d391kg img[alt*="Amazon"],
        .css-1d391kg img[alt*="amazon"] {
            width: 110px !important;
            height: auto !important;
            margin-bottom: 1rem !important;
            margin-top: 0.5rem !important;
        }
        
        /* 侧边栏所有图片统一处理 */
        .css-1d391kg img {
            max-width: 110px !important;
            height: auto !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* 侧边栏内容优化 */
        .css-1d391kg .stRadio label {
            font-size: 13px !important;
            padding: 0.5rem 0.7rem !important;
            margin-bottom: 0.2rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1.4rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        .css-1d391kg .stButton > button {
            font-size: 12px !important;
            padding: 0.5rem 0.8rem !important;
            min-height: 38px !important;
        }
        
        /* 标准大屏幕字体 */
        html, body, [class*="css"] {
            font-size: 14px !important;
        }
    }
    
    /* 中等屏幕 (768px - 1199px) */
    @media (min-width: 768px) and (max-width: 1199px) {
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        .css-1d391kg {
            width: 220px !important;
            padding: 0.8rem 0.6rem !important;
        }
        
        /* 中等屏幕Amazon Logo优化 */
        .css-1d391kg img[src*="amazon.png"], 
        .css-1d391kg img[alt*="Amazon"],
        .css-1d391kg img[alt*="amazon"] {
            width: 90px !important;
            height: auto !important;
            margin-bottom: 0.8rem !important;
        }
        
        .css-1d391kg img {
            max-width: 90px !important;
            height: auto !important;
            margin-bottom: 0.6rem !important;
        }
        
        .css-1d391kg .stRadio label {
            font-size: 12px !important;
            padding: 0.4rem 0.5rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1.2rem !important;
            margin-bottom: 0.6rem !important;
        }
        
        /* 列布局调整 */
        .row-widget.stRadio > div {
            flex-direction: column !important;
        }
    }
    
    /* 小屏幕 (576px - 767px) */
    @media (min-width: 576px) and (max-width: 767px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .css-1d391kg {
            width: 200px !important;
            padding: 0.6rem 0.4rem !important;
        }
        
        /* 小屏幕Amazon Logo优化 */
        .css-1d391kg img[src*="amazon.png"], 
        .css-1d391kg img[alt*="Amazon"],
        .css-1d391kg img[alt*="amazon"] {
            width: 70px !important;
            height: auto !important;
            margin-bottom: 0.6rem !important;
        }
        
        .css-1d391kg img {
            max-width: 70px !important;
            height: auto !important;
            margin-bottom: 0.5rem !important;
        }
        
        .css-1d391kg .stRadio label {
            font-size: 11px !important;
            padding: 0.3rem 0.4rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1.1rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* 小屏幕字体减小 */
        html, body, [class*="css"] {
            font-size: 13px !important;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        h3 {
            font-size: 1.3rem !important;
        }
        
        /* 按钮适配 */
        .stButton > button {
            font-size: 13px !important;
            padding: 0.4rem 0.8rem !important;
            width: 100% !important;
        }
        
        /* 表格滚动 */
        .dataframe {
            font-size: 12px !important;
            overflow-x: auto !important;
        }
    }
    
    /* 超小屏幕 (< 576px) */
    @media (max-width: 575px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        .css-1d391kg {
            width: 180px !important;
            padding: 0.4rem 0.3rem !important;
        }
        
        /* 超小屏幕Amazon Logo优化 */
        .css-1d391kg img[src*="amazon.png"], 
        .css-1d391kg img[alt*="Amazon"],
        .css-1d391kg img[alt*="amazon"] {
            width: 50px !important;
            height: auto !important;
            margin-bottom: 0.4rem !important;
        }
        
        .css-1d391kg img {
            max-width: 50px !important;
            height: auto !important;
            margin-bottom: 0.3rem !important;
        }
        
        .css-1d391kg .stRadio label {
            font-size: 10px !important;
            padding: 0.2rem 0.3rem !important;
        }
        
        .css-1d391kg h2 {
            font-size: 1rem !important;
            margin-bottom: 0.4rem !important;
        }
        
        /* 超小屏幕字体最小 */
        html, body, [class*="css"] {
            font-size: 12px !important;
        }
        
        h1 {
            font-size: 1.6rem !important;
            text-align: center !important;
        }
        
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        /* 按钮全宽 */
        .stButton > button {
            font-size: 12px !important;
            padding: 0.3rem 0.6rem !important;
            width: 100% !important;
        }
        
        /* 输入框适配 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            font-size: 12px !important;
        }
        
        /* 表格适配 */
        .dataframe {
            font-size: 11px !important;
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
    
    /* 通用响应式设置 */
    img {
        max-width: 100% !important;
        height: auto !important;
    }
    
    .dataframe {
        width: 100% !important;
        overflow-x: auto !important;
    }
    
    .stTextArea > div > div > textarea {
        resize: vertical !important;
    }
    
    .stSelectbox > div > div {
        width: 100% !important;
    }
    
    .row-widget {
        width: 100% !important;
    }
    
    .stProgress > div > div {
        width: 100% !important;
    }
    
    .stAlert {
        margin: 0.5rem 0 !important;
    }
    
    .stCode {
        overflow-x: auto !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    
    .stJson {
        overflow-x: auto !important;
    }
    
    /* 移动设备触摸优化 */
    @media (hover: none) and (pointer: coarse) {
        .stButton > button {
            min-height: 44px !important;
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
    
    /* 高DPI显示器优化 */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
        /* 高DPI显示器下的图标和图片优化 */
        img {
            image-rendering: -webkit-optimize-contrast !important;
            image-rendering: crisp-edges !important;
        }
        
        /* 高DPI下的文本渲染优化 */
        * {
            -webkit-font-smoothing: antialiased !important;
            -moz-osx-font-smoothing: grayscale !important;
        }
    }
    </style>
    """

def get_screen_detection_script():
    """获取屏幕检测JavaScript脚本"""
    return """
    <script>
    (function() {
        function detectAndApplyScreenStyles() {
            const width = window.screen.width;
            const height = window.screen.height;
            const dpr = window.devicePixelRatio || 1;
            
            // 移除之前的屏幕类
            document.documentElement.classList.remove('screen-4k', 'screen-2k', 'screen-fhd', 'high-dpi');
            
            // 检测屏幕类型并添加相应类
            if (width >= 3840 || height >= 2160) {
                document.documentElement.classList.add('screen-4k');
                console.log('检测到4K显示器:', width + 'x' + height);
            } else if (width >= 2560 || height >= 1440) {
                document.documentElement.classList.add('screen-2k');
                console.log('检测到2K显示器:', width + 'x' + height);
            } else if (width >= 1920) {
                document.documentElement.classList.add('screen-fhd');
                console.log('检测到Full HD显示器:', width + 'x' + height);
            }
            
            // 高DPI显示器检测
            if (dpr >= 2) {
                document.documentElement.classList.add('high-dpi');
                console.log('检测到高DPI显示器, DPR:', dpr);
            }
            
            // 在页面标题中显示检测结果（调试用）
            const originalTitle = document.title;
            if (!originalTitle.includes('|')) {
                document.title = originalTitle + ' | ' + width + 'x' + height + ' (DPR:' + dpr + ')';
            }
        }
        
        // 页面加载时检测
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', detectAndApplyScreenStyles);
        } else {
            detectAndApplyScreenStyles();
        }
        
        // 窗口大小改变时重新检测
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(detectAndApplyScreenStyles, 250);
        });
        
        // 定期检查（防止某些情况下检测失败）
        setTimeout(detectAndApplyScreenStyles, 1000);
    })();
    </script>
    """

def get_log_diagnosis_responsive_css():
    """获取日志诊断页面的响应式CSS样式 - 简化版"""
    return """
    <style>
    /* 移除Streamlit默认的页面padding，让iframe占满空间 */
    .main > div {
        padding: 0rem !important;
    }
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    
    /* iframe基础样式 */
    iframe {
        width: 100% !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* 4K超大屏幕 - iframe更高，内容更大 */
    @media (min-width: 3840px), (min-height: 2160px) {
        iframe {
            height: calc(100vh - 150px) !important;
            min-height: 1800px !important;
        }
        
        /* 4K屏幕下iframe内的内容也要放大 */
        iframe {
            transform: scale(1.5) !important;
            transform-origin: top left !important;
            width: 66.67% !important; /* 1/1.5 = 0.6667 */
            height: calc((100vh - 150px) / 1.5) !important;
        }
    }
    
    /* 2K屏幕 - iframe适中大小 */
    @media (min-width: 2560px) and (max-width: 3839px) {
        iframe {
            height: calc(100vh - 120px) !important;
            min-height: 1200px !important;
        }
        
        /* 2K屏幕下适度放大内容 */
        iframe {
            transform: scale(1.3) !important;
            transform-origin: top left !important;
            width: 76.92% !important; /* 1/1.3 = 0.7692 */
            height: calc((100vh - 120px) / 1.3) !important;
        }
    }
    
    /* Full HD屏幕 - 标准大小 */
    @media (min-width: 1920px) and (max-width: 2559px) {
        iframe {
            height: calc(100vh - 100px) !important;
            min-height: 900px !important;
        }
        
        /* Full HD屏幕下轻微放大 */
        iframe {
            transform: scale(1.1) !important;
            transform-origin: top left !important;
            width: 90.91% !important; /* 1/1.1 = 0.9091 */
            height: calc((100vh - 100px) / 1.1) !important;
        }
    }
    
    /* 标准大屏幕 - 默认大小 */
    @media (min-width: 1200px) and (max-width: 1919px) {
        iframe {
            height: calc(100vh - 80px) !important;
            min-height: 700px !important;
        }
    }
    
    /* 中等屏幕 - 稍小 */
    @media (min-width: 768px) and (max-width: 1199px) {
        iframe {
            height: calc(100vh - 60px) !important;
            min-height: 500px !important;
        }
    }
    
    /* 小屏幕 - 隐藏侧边栏，iframe占满 */
    @media (min-width: 576px) and (max-width: 767px) {
        iframe {
            height: calc(100vh - 40px) !important;
            min-height: 400px !important;
        }
        
        /* 隐藏侧边栏以获得更多空间 */
        .css-1d391kg {
            display: none !important;
        }
        
        .main .block-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
    }
    
    /* 超小屏幕 - 完全隐藏侧边栏 */
    @media (max-width: 575px) {
        iframe {
            height: calc(100vh - 20px) !important;
            min-height: 300px !important;
        }
        
        /* 完全隐藏侧边栏 */
        .css-1d391kg {
            display: none !important;
        }
        
        .main .block-container {
            padding: 0 !important;
        }
    }
    
    /* 确保iframe内容可以正确缩放 */
    iframe[src*="/logs"] {
        overflow: hidden !important;
    }
    </style>
    """

def get_mobile_viewport_meta():
    """获取移动端视口meta标签"""
    return """
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """
