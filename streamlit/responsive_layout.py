"""
响应式布局辅助函数
"""

import streamlit as st

def responsive_columns(ratios, gap="small"):
    """
    创建响应式列布局
    在小屏幕上自动调整列比例或堆叠显示
    
    Args:
        ratios: 列比例列表，如 [2, 1] 或 [1, 1, 1]
        gap: 列间距，"small", "medium", "large"
    
    Returns:
        列对象列表
    """
    # 检测屏幕大小的JavaScript代码
    screen_size_js = """
    <script>
    function getScreenSize() {
        return window.innerWidth;
    }
    </script>
    """
    
    # 根据列数调整小屏幕行为
    if len(ratios) > 2:
        # 3列或更多：在小屏幕上使用相等比例
        mobile_ratios = [1] * len(ratios)
    else:
        # 2列：在小屏幕上稍微调整比例
        if ratios == [2, 1]:
            mobile_ratios = [1.5, 1]
        else:
            mobile_ratios = ratios
    
    # 添加CSS来控制响应式行为
    responsive_css = f"""
    <style>
    @media (max-width: 768px) {{
        .row-widget.stColumns > div {{
            min-width: 0 !important;
            flex: 1 !important;
        }}
    }}
    
    @media (max-width: 576px) {{
        .row-widget.stColumns {{
            flex-direction: column !important;
        }}
        .row-widget.stColumns > div {{
            width: 100% !important;
            margin-bottom: 1rem !important;
        }}
    }}
    </style>
    """
    
    st.markdown(responsive_css, unsafe_allow_html=True)
    
    # 创建列
    return st.columns(ratios, gap=gap)

def responsive_metrics(metrics_data, columns_per_row=3):
    """
    创建响应式指标显示
    
    Args:
        metrics_data: 指标数据列表，每个元素为 (label, value, delta)
        columns_per_row: 每行显示的列数
    """
    # 响应式指标CSS
    metrics_css = """
    <style>
    @media (max-width: 768px) {
        .metric-container {
            flex-direction: column !important;
        }
    }
    
    @media (max-width: 576px) {
        .row-widget.stColumns {
            flex-direction: column !important;
        }
        .row-widget.stColumns > div {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }
    }
    </style>
    """
    
    st.markdown(metrics_css, unsafe_allow_html=True)
    
    # 分组显示指标
    for i in range(0, len(metrics_data), columns_per_row):
        group = metrics_data[i:i + columns_per_row]
        cols = st.columns(len(group))
        
        for j, (label, value, delta) in enumerate(group):
            with cols[j]:
                if delta is not None:
                    st.metric(label, value, delta)
                else:
                    st.metric(label, value)

def responsive_buttons(buttons_data, columns_per_row=2):
    """
    创建响应式按钮布局
    
    Args:
        buttons_data: 按钮数据列表，每个元素为 (label, key, callback)
        columns_per_row: 每行显示的按钮数
    """
    # 响应式按钮CSS
    buttons_css = """
    <style>
    @media (max-width: 576px) {
        .stButton > button {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }
        .row-widget.stColumns {
            flex-direction: column !important;
        }
        .row-widget.stColumns > div {
            width: 100% !important;
        }
    }
    </style>
    """
    
    st.markdown(buttons_css, unsafe_allow_html=True)
    
    # 分组显示按钮
    for i in range(0, len(buttons_data), columns_per_row):
        group = buttons_data[i:i + columns_per_row]
        cols = st.columns(len(group))
        
        for j, (label, key, callback) in enumerate(group):
            with cols[j]:
                if st.button(label, key=key):
                    if callback:
                        callback()

def mobile_friendly_dataframe(df, max_height=400):
    """
    创建移动端友好的数据框显示
    
    Args:
        df: pandas DataFrame
        max_height: 最大高度
    """
    # 移动端数据框CSS
    df_css = """
    <style>
    @media (max-width: 768px) {
        .dataframe {
            font-size: 11px !important;
            overflow-x: auto !important;
        }
        .dataframe th, .dataframe td {
            padding: 0.25rem !important;
            white-space: nowrap !important;
        }
    }
    
    @media (max-width: 576px) {
        .dataframe {
            font-size: 10px !important;
        }
        .dataframe th, .dataframe td {
            padding: 0.2rem !important;
        }
    }
    </style>
    """
    
    st.markdown(df_css, unsafe_allow_html=True)
    
    # 显示数据框
    st.dataframe(df, height=max_height, use_container_width=True)

def responsive_text_input(label, key=None, placeholder="", help=None):
    """
    创建响应式文本输入框
    """
    input_css = """
    <style>
    @media (max-width: 576px) {
        .stTextInput > div > div > input {
            font-size: 16px !important; /* 防止iOS缩放 */
        }
        .stTextArea > div > div > textarea {
            font-size: 16px !important; /* 防止iOS缩放 */
        }
    }
    </style>
    """
    
    st.markdown(input_css, unsafe_allow_html=True)
    
    return st.text_input(label, key=key, placeholder=placeholder, help=help)

def responsive_text_area(label, key=None, height=100, placeholder="", help=None):
    """
    创建响应式文本区域
    """
    # 根据屏幕大小调整高度
    area_css = f"""
    <style>
    @media (max-width: 768px) {{
        .stTextArea > div > div > textarea {{
            min-height: {max(80, height-20)}px !important;
        }}
    }}
    
    @media (max-width: 576px) {{
        .stTextArea > div > div > textarea {{
            min-height: {max(60, height-40)}px !important;
            font-size: 16px !important; /* 防止iOS缩放 */
        }}
    }}
    </style>
    """
    
    st.markdown(area_css, unsafe_allow_html=True)
    
    return st.text_area(label, key=key, height=height, placeholder=placeholder, help=help)
