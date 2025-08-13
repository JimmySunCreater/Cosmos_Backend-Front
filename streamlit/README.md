# Cosmos场景管理Web界面

这是Cosmos视频生成系统的Web管理界面，基于Streamlit构建，提供场景生成、管理、视频生成和日志诊断功能。

## 📁 文件结构

```
streamlit/
├── streamlit_app.py              # 主应用文件
├── config_streamlit.py           # 智能配置文件（动态IP检测）
├── responsive_layout.py          # 响应式布局组件
├── responsive_styles.py          # 响应式CSS样式
├── requirements_streamlit.txt    # Python依赖
├── start_streamlit.sh           # 启动脚本
├── amazon.png                   # Amazon Logo
├── cosmos-streamlit.service      # 系统服务配置
├── README.md                    # 本文件
└── STREAMLIT_README.md          # 详细使用说明
```

## 🚀 快速启动

### 推荐方式: 从streamlit目录启动
```bash
cd /home/ubuntu/cosmos_service/streamlit
./start_streamlit.sh
```

### 直接启动
```bash
cd /home/ubuntu/cosmos_service/streamlit
pip3 install -r requirements_streamlit.txt
streamlit run streamlit_app.py --server.port=5000 --server.address=0.0.0.0
```

### 系统服务方式
```bash
sudo systemctl start cosmos-streamlit
sudo systemctl enable cosmos-streamlit  # 开机自启
```

## 🌐 访问界面

启动后访问: `http://localhost:5000`

## 📋 主要功能

### 🎨 场景生成
- 输入简短场景描述
- 选择SingleView（单视角）或MultiView（多视角）
- AI自动生成详细场景描述
- 自动保存到DynamoDB场景库

### 📚 场景管理
- 查看所有场景列表（分页显示）
- 显示场景详细信息（UUID、类型、时间）
- 删除场景功能
- 支持多视角场景展示（使用Tabs）
- 响应式布局适配不同屏幕

### 🎥 视频生成
- 从场景库选择场景
- 提交视频生成任务
- 实时查询任务状态
- 系统状态监控（GPU使用率、队列状态）
- 任务进度跟踪

### 📊 日志诊断
- 实时日志查看
- 系统运行状态诊断
- 错误日志分析
- 全屏日志界面

## ⚙️ 智能配置系统

### 动态IP检测
配置文件 `config_streamlit.py` 具备智能IP检测功能：

```python
# 自动检测可用的Cosmos服务器
# 优先级：i-0bbe2d67c7493574f > i-07997436e1281b482
COSMOS_API_URL = "http://私有IP:8080"     # 用于API调用
COSMOS_LOG_URL = "http://公网IP:8080"     # 用于日志页面
```

### 主要配置项
```python
# API地址配置
ENHANCE_API_URL = "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/enhence"
LIBRARY_API_URL = "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/library"

# 场景类型配置
SCENE_TYPES = {
    "SingleView": {"name": "单视角", "estimated_time": "约1小时"},
    "MultiView": {"name": "多视角", "estimated_time": "约2小时"}
}
```

## 🎨 响应式设计

### 特性
- 自适应布局，支持桌面和移动设备
- 智能列布局（桌面2:1，移动端堆叠）
- 响应式字体和间距
- 移动端优化的交互体验

### 断点设置
- **大屏幕**: ≥1200px - 桌面显示器
- **中等屏幕**: 768-1199px - 平板横屏
- **小屏幕**: 576-767px - 平板竖屏
- **超小屏幕**: <576px - 手机

## 🔧 依赖要求

```txt
streamlit>=1.28.0
requests>=2.31.0
pandas>=2.0.0
boto3>=1.26.0
uuid
```

## 🛡️ 容错机制

### 智能故障转移
- 自动检测EC2实例状态
- 健康检查验证服务可用性
- AWS API调用失败时使用默认配置
- 详细的错误日志和用户提示

### 网络优化
- API调用使用私有IP（VPC内部，速度快）
- 日志页面使用公网IP（浏览器可访问）
- 超时设置和重试机制

## 🔄 维护和备份

### 重启服务
```bash
# 停止服务
pkill -f streamlit

# 重新启动
cd /home/ubuntu/cosmos_service/streamlit
./start_streamlit.sh
```

### 备份
```bash
# 创建备份
cd /home/ubuntu
tar -czf streamlit_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C cosmos_service streamlit/
```

## 📞 技术支持

- 详细使用说明请参考 `STREAMLIT_README.md`
- 日志文件位置: `streamlit.log`
- 系统服务状态: `sudo systemctl status cosmos-streamlit`
