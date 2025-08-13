# Cosmos API服务代码备份

## 备份信息
- **备份时间**: 2025-06-15T23:29:45.997976
- **项目路径**: /home/ubuntu/cosmos_service
- **备份文件数**: 22

## 项目架构分析

### 核心组件
1. **API服务层**
   - `cosmos_api_service_simple.py`: 主API服务，处理视频生成请求
   - `gpu_manager.py`: GPU资源智能管理
   - `translator.py`: AWS Bedrock翻译服务
   - `config.py`: 服务配置管理

2. **Web界面层**
   - `streamlit/streamlit_app.py`: Streamlit Web管理界面
   - `streamlit/config_streamlit.py`: Web界面配置
   - 支持场景管理、任务监控、状态查看

3. **工具层**
   - `upload_to_s3.py`: S3视频上传工具
   - `utilities/`: 部署检查和批量任务工具
   - `templates/`: Web日志查看器

4. **配置层**
   - systemd服务配置
   - 启动脚本
   - 依赖管理

### 技术栈
- **后端**: Flask + Python 3.10+
- **前端**: Streamlit
- **GPU管理**: CUDA + 自定义GPU管理器
- **云服务**: AWS DynamoDB + S3 + Bedrock + CloudFront
- **翻译**: AWS Bedrock Claude 3.5 Sonnet
- **部署**: systemd + Ubuntu

### 主要功能
- 🎥 多视图视频生成 (MultiView/SingleView)
- 🔄 智能队列管理和GPU资源分配
- 🌐 自动中英文翻译
- 📊 实时状态监控和日志查看
- 🎨 Web界面场景管理
- ☁️ 自动S3上传和CloudFront分发

## 恢复说明

### 1. 环境准备
```bash
# 安装Python依赖
pip install -r requirements.txt
pip install -r streamlit/requirements_streamlit.txt

# 配置AWS凭证
aws configure
```

### 2. 服务部署
```bash
# 复制systemd服务文件
sudo cp cosmos-api.service /etc/systemd/system/
sudo cp streamlit/cosmos-streamlit.service /etc/systemd/system/

# 启用并启动服务
sudo systemctl enable cosmos-api cosmos-streamlit
sudo systemctl start cosmos-api cosmos-streamlit
```

### 3. 验证部署
```bash
# 检查API服务
curl http://localhost:8080/health

# 检查Web界面
curl http://localhost:8501
```

## 文件清单

### 核心API服务
- `cosmos_api_service_simple.py` (31.3 KB)
- `gpu_manager.py` (5.2 KB)
- `translator.py` (4.0 KB)
- `config.py` (2.7 KB)
- `upload_to_s3.py` (2.8 KB)
- `utilities/start_all_tasks.py` (6.2 KB)

### Streamlit Web界面
- `streamlit/streamlit_app.py` (22.2 KB)
- `streamlit/config_streamlit.py` (1.8 KB)
- `streamlit/start_streamlit.sh` (0.9 KB)
- `streamlit/requirements_streamlit.txt` (0.1 KB)
- `streamlit/amazon.png` (12.6 KB)
- `streamlit/cosmos-streamlit.service` (0.6 KB)
- `streamlit/README.md` (1.9 KB)
- `streamlit/STREAMLIT_README.md` (3.4 KB)

### 服务配置
- `cosmos-api.service` (0.4 KB)
- `start_service.sh` (0.7 KB)
- `start_web_ui.sh` (0.3 KB)
- `utilities/check_deployment.sh` (0.9 KB)

### 文档和依赖
- `requirements.txt` (0.1 KB)
- `README.md` (14.5 KB)

### Web资源
- `templates/logs.html` (15.6 KB)
- `static/css/logs.css` (1.2 KB)

---
**备份工具**: analyze_and_backup.py
**项目版本**: v3.0
