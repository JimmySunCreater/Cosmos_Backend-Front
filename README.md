# Cosmos Predict API Service

这是一个用于处理Cosmos视频生成任务的API服务，支持智能队列管理、GPU资源管理、调用大模型实现prompt自动翻译和DynamoDB集成。

Nvidia Cosmos系列模型地址：https://github.com/nvidia-cosmos
NVIDIA Cosmos 是英伟达面向物理 AI（机器人 / 自动驾驶）的世界基础模型（WFM）系列，能按物理规则生成 / 预测逼真视频世界，用于仿真、合成数据与机器人决策。

作者：孙健-亚马逊云科技解决方案架构师，10+ 年汽车行业从业经验，从事汽车电子电器分析、自动驾驶解决方案相关领域，对自动驾驶、软件定义汽车等云架构设计及AI应用有丰富经验。

## 🚀 功能特性

- **智能队列管理**: 支持多个API调用，自动队列处理和任务调度
- **GPU智能分配**: MultiView使用全部8个GPU，SingleView使用单个GPU，支持并行处理
- **DynamoDB集成**: 自动读取场景数据和更新任务状态
- **多视图支持**: 支持MultiView和SingleView两种场景类型
- **自动翻译**: 使用AWS Bedrock Claude模型自动翻译中文提示词为英文
- **状态跟踪**: 实时更新任务状态（Translating → Waiting → Generating → Uploading → Finished/Failed）
- **健康检查**: 提供详细的服务健康状态和GPU使用情况监控
- **实时日志**: 支持SSE实时日志流和Web日志查看器
- **自动重启**: 服务崩溃自动重启，开机自动启动
- **详细日志**: 完整的操作日志记录和错误追踪

## 📋 当前配置

### 视频生成配置
- **MultiView视频**: 使用全部8个GPU并行生成，输出为 `{uuid}_grid.mp4`
- **SingleView视频**: 使用单个GPU生成，输出为 `{uuid}.mp4`
- **模型优化**: SingleView启用内存优化选项（offload模式）
- **视频存储**: 自动上传至S3 (documents-distrubution/cosmos-video/)
- **视频访问**: 通过CloudFront CDN (d3bb5kiveg9mt4.cloudfront.net)
- **GPU配置**: 8个GPU总计，智能分配和释放
- **服务端口**: 8080
- **绑定地址**: 0.0.0.0（支持外部访问）

### 系统要求
- Python 3.10+
- CUDA支持的GPU (8个GPU)
- AWS CLI配置
- DynamoDB访问权限
- Bedrock访问权限（用于翻译服务）

## 🛠️ 安装和配置

### 1. 环境准备

确保系统已安装必要的依赖：
```bash
# 安装Python依赖
pip install -r requirements.txt

# 配置AWS凭证
aws configure
```

### 2. DynamoDB表结构

确保DynamoDB中存在`SceneGeneration`表，包含以下字段：
- `uuid` (主键, String)
- `SceneType` (String) - 场景类型：MultiView 或 SingleView
- `PROMPT_FRONT` (String) - 前方视角提示词
- `PROMPT_FRONT_LEFT` (String) - 左前方视角提示词 (MultiView)
- `PROMPT_FRONT_RIGHT` (String) - 右前方视角提示词 (MultiView)
- `PROMPT_BACK` (String) - 后方视角提示词 (MultiView)
- `PROMPT_BACK_LEFT` (String) - 左后方视角提示词 (MultiView)
- `PROMPT_BACK_RIGHT` (String) - 右后方视角提示词 (MultiView)
- `PROMPT_FRONT_EN` (String) - 英文翻译结果
- `PROMPT_FRONT_LEFT_EN` (String) - 左前方英文翻译 (MultiView)
- `PROMPT_FRONT_RIGHT_EN` (String) - 右前方英文翻译 (MultiView)
- `PROMPT_BACK_EN` (String) - 后方英文翻译 (MultiView)
- `PROMPT_BACK_LEFT_EN` (String) - 左后方英文翻译 (MultiView)
- `PROMPT_BACK_RIGHT_EN` (String) - 右后方英文翻译 (MultiView)
- `generation_status` (String) - 任务状态
- `update_time` (String) - 更新时间
- `video_link` (String) - 视频链接

## 🚀 启动服务

### 方法1: 使用启动脚本（推荐）
```bash
./start_service.sh
```

### 方法2: 使用systemd服务（生产环境推荐）
```bash
# 启动服务
sudo systemctl start cosmos-api

# 查看服务状态
sudo systemctl status cosmos-api

# 查看服务日志
journalctl -u cosmos-api -f

# 重启服务
sudo systemctl restart cosmos-api
```

### 方法3: 直接启动
```bash
cd /home/ubuntu/cosmos_service
API_HOST=0.0.0.0 API_PORT=8080 nohup python3 cosmos_api_service_simple.py > cosmos_api.log 2>&1 &
```

## 📡 API端点

### 1. 健康检查
```http
GET /health
```

响应示例：
```json
{
    "status": "healthy",
    "queue_size": 0,
    "active_tasks": 1,
    "current_tasks": ["5a793b2f-4c9d-480b-8606-2c7f26c06666"],
    "available_gpus": 7,
    "occupied_gpus": 1,
    "gpu_status_detail": "7/8 GPUs available",
    "multiview_ready": false
}
```

### 2. 提交视频生成任务
```http
POST /generate
Content-Type: application/json

{
    "uuid": "5a793b2f-4c9d-480b-8606-2c7f26c06666"
}
```

**注意**: 
- 只需要提供UUID，SceneType会自动从DynamoDB中根据UUID读取
- 系统会自动获取场景类型和所有相关的prompt数据
- 系统会自动翻译中文提示词为英文

响应示例：
```json
{
    "message": "Task added to queue successfully",
    "uuid": "5a793b2f-4c9d-480b-8606-2c7f26c06666",
    "scene_type": "MultiView",
    "status": "Processing"
}
```

### 3. 查询任务状态
```http
GET /status/<uuid>
```

响应示例：
```json
{
    "uuid": "5a793b2f-4c9d-480b-8606-2c7f26c06666",
    "generation_status": "Generating",
    "update_time": "2025-06-10 13:00:00 BJT",
    "queue_size": 1,
    "active_tasks": 1,
    "video_link": "d3bb5kiveg9mt4.cloudfront.net/cosmos-video/5a793b2f-4c9d-480b-8606-2c7f26c06666_grid.mp4"
}
```

### 4. GPU状态查询
```http
GET /gpu-status
```

响应示例：
```json
{
    "gpu_manager_status": {
        "total_gpus": 8,
        "available_gpus": [0, 1, 2, 3, 4, 5, 6],
        "occupied_gpus": {"7": "task-uuid-123"},
        "gpu_memory_info": {
            "0": {"memory_used": 512, "memory_total": 24576, "utilization": 0}
        }
    },
    "queue_size": 0,
    "active_tasks": 1,
    "active_task_details": {
        "task-uuid-123": {
            "scene_type": "SingleView",
            "start_time": "2025-06-11T01:00:00+08:00",
            "status": "Generating",
            "allocated_gpus": [7]
        }
    }
}
```

### 5. 实时日志流 (SSE)
```http
GET /logs/stream
```

实时输出所有日志：
```bash
curl -N http://localhost:8080/logs/stream
```

### 6. 特定任务日志流
```http
GET /logs/stream/<uuid>
```

实时输出特定任务的日志：
```bash
curl -N http://localhost:8080/logs/stream/5a793b2f-4c9d-480b-8606-2c7f26c06666
```

### 7. 日志查看器页面
```http
GET /logs
```

提供友好的Web界面查看实时日志：
```
http://localhost:8080/logs
```

## 📊 任务状态说明

- **Translating**: 正在翻译中文提示词为英文
- **Waiting**: 任务已加入队列，等待处理
- **Generating**: 正在生成视频
- **Uploading**: 正在上传视频到S3
- **Finished**: 视频生成完成，视频已上传至S3并通过CloudFront提供访问
- **Failed**: 视频生成失败

## 📹 视频存储和访问

### S3存储
- **存储位置**: `documents-distrubution/cosmos-video/`
- **文件命名**:
  - SingleView: `{uuid}.mp4`
  - MultiView: `{uuid}_grid.mp4`
- **内容类型**: `video/mp4`

### CloudFront访问
- **域名**: `d3bb5kiveg9mt4.cloudfront.net`
- **访问URL**:
  - SingleView: `https://d3bb5kiveg9mt4.cloudfront.net/cosmos-video/{uuid}.mp4`
  - MultiView: `https://d3bb5kiveg9mt4.cloudfront.net/cosmos-video/{uuid}_grid.mp4`
- **视频链接**: 生成完成后通过`video_link`字段在API响应中返回

## 🔧 配置选项

服务支持以下环境变量配置：

```bash
export API_HOST="0.0.0.0"                    # 服务绑定地址
export API_PORT="8080"                       # 服务端口
export API_DEBUG="false"                     # 调试模式
export AWS_DEFAULT_REGION="us-west-2"        # AWS区域
export DYNAMODB_TABLE_NAME="SceneGeneration" # DynamoDB表名
export NUM_GPUS="8"                          # GPU数量
export NPROC_PER_NODE="8"                    # 每节点进程数
export COSMOS_BASE_PATH="/home/ubuntu/cosmos-predict1"  # Cosmos模型路径
export CONDA_ENV_PATH="/home/ubuntu/miniconda3/envs/cosmos-predict1"  # Conda环境路径
export LOG_FILE="/home/ubuntu/cosmos_service/cosmos_api.log"  # 日志文件路径
export MAX_QUEUE_SIZE="100"                  # 最大队列大小
export TASK_TIMEOUT="3600"                   # 任务超时时间（秒）
```

### 翻译服务配置
- **翻译模型**: AWS Bedrock Claude 3.5 Sonnet
- **翻译区域**: us-east-1
- **重试机制**: 最多5次重试，递增等待时间
- **限流处理**: 自动检测并处理API限流

## 📝 日志管理

### 日志位置
- **应用日志**: `/home/ubuntu/cosmos_service/cosmos_api.log`
- **系统日志**: `journalctl -u cosmos-api -f`
- **历史日志**: `/home/ubuntu/cosmos_service/logs/`

### 查看日志
```bash
# 查看实时应用日志
tail -f /home/ubuntu/cosmos_service/cosmos_api.log

# 查看系统服务日志
journalctl -u cosmos-api -f

# 查看最近的错误日志
journalctl -u cosmos-api --since "1 hour ago" -p err
```

## 🌐 Web管理界面

### Streamlit场景管理系统
提供友好的Web界面进行场景管理和视频生成：

```bash
# 启动Web界面
./start_web_ui.sh

# 访问地址
http://localhost:8501
```

**主要功能：**
- 🎨 **场景生成**: 输入描述，AI增强生成详细场景
- 📚 **场景管理**: 查看、编辑、删除场景库中的场景
- 🎥 **视频生成**: 选择场景，提交视频生成任务
- 📊 **状态监控**: 实时查看系统状态和任务进度

详细使用说明请参考: `streamlit/STREAMLIT_README.md`

## 🧪 测试

### 基本健康检查
```bash
curl -s http://localhost:8080/health | python3 -m json.tool
```

### 提交测试任务
```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "test-uuid-001"
  }'
```

### 手动上传视频
```bash
# 上传SingleView视频
python3 upload_to_s3.py test-uuid-001 SingleView

# 上传MultiView视频
python3 upload_to_s3.py test-uuid-001 MultiView
```

上传脚本会自动：
1. 检查本地视频文件是否存在
2. 上传视频到S3指定位置
3. 更新DynamoDB中的video_link字段
4. 返回CloudFront访问URL

## 🔍 监控和维护

### 服务监控
```bash
# 检查服务状态
sudo systemctl status cosmos-api

# 检查进程
ps aux | grep cosmos_api_service_simple

# 检查端口占用
ss -tlnp | grep :8080

# 检查GPU使用情况
nvidia-smi
```

### 性能监控
```bash
# 查看API响应
curl -s http://localhost:8080/health

# 监控日志
tail -f cosmos_api.log | grep -E "(ERROR|WARNING|Task.*completed)"
```

## 🚨 故障排除

### 1. 服务无法启动
```bash
# 检查服务状态
sudo systemctl status cosmos-api

# 查看详细错误
journalctl -u cosmos-api --no-pager

# 检查端口占用
sudo lsof -i :8080

# 手动启动测试
python3 cosmos_api_service_simple.py
```

### 2. 任务执行失败
```bash
# 检查GPU状态
nvidia-smi

# 查看错误日志
grep "ERROR\|Failed" cosmos_api.log

# 检查模型文件
ls -la /home/ubuntu/cosmos-predict1/checkpoints/

# 验证Conda环境
conda info --envs
```

### 3. DynamoDB连接问题
```bash
# 测试AWS连接
aws dynamodb describe-table --table-name SceneGeneration --region us-west-2

# 检查IAM权限
aws sts get-caller-identity

# 验证区域设置
echo $AWS_DEFAULT_REGION
```

### 4. 翻译服务问题
```bash
# 检查翻译日志
grep "Translation" cosmos_api.log

# 查看限流警告
grep "Rate limited" cosmos_api.log
```

## 🔗 集成示例

### Lambda函数集成
```python
import json
import requests

def lambda_handler(event, context):
    api_url = "http://your-server-ip:8080/generate"
    
    payload = {
        "uuid": event['uuid']
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        return {
            'statusCode': response.status_code,
            'body': json.dumps(response.json())
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### 批量处理脚本
```python
import requests
import time

def submit_batch_tasks(uuids):
    api_url = "http://localhost:8080/generate"
    
    for uuid in uuids:
        payload = {"uuid": uuid}
        response = requests.post(api_url, json=payload)
        print(f"Task {uuid}: {response.json()}")
        time.sleep(1)  # 避免过快提交
```

## 📈 性能优化

### GPU优化
- MultiView任务使用全部8个GPU以获得最佳性能
- SingleView任务使用单个GPU以支持并发处理
- 自动GPU资源管理，避免资源冲突

### 内存优化
- 模型自动卸载以节省GPU内存
- 临时文件自动清理
- 队列大小自动调整

### 网络优化
- 支持外部访问（0.0.0.0绑定）
- 翻译服务自动限流处理
- 健康检查轻量化设计

## 🔒 安全注意事项

1. **网络安全**: 
   - 建议在VPC内部使用
   - 配置适当的安全组规则
   - 考虑添加API认证

2. **资源安全**:
   - 设置适当的队列大小限制
   - 配置任务超时时间
   - 监控GPU资源使用

3. **数据安全**:
   - 避免在日志中记录敏感信息
   - 定期清理临时文件
   - 备份重要配置文件

## 📁 项目结构

```
/home/ubuntu/cosmos_service/
├── cosmos_api_service_simple.py    # 主服务文件
├── gpu_manager.py                  # GPU资源管理
├── translator.py                   # 翻译服务
├── config.py                       # 配置文件
├── start_service.sh               # 启动脚本
├── start_web_ui.sh                # Web界面启动脚本
├── cosmos-api.service             # systemd服务配置
├── requirements.txt               # Python依赖
├── upload_to_s3.py                # S3上传脚本
├── README.md                      # 项目文档
├── cosmos_api.log                 # 当前日志
├── logs/                          # 历史日志
├── backup/                        # 备份文件
├── utilities/                     # 实用工具脚本
│   ├── check_deployment.sh        # 部署状态检查
│   └── start_all_tasks.py         # 批量任务启动
├── streamlit/                     # Streamlit Web界面
│   ├── streamlit_app.py           # 主应用文件
│   ├── start_streamlit.sh         # Streamlit启动脚本
│   └── requirements_streamlit.txt # Streamlit依赖
├── templates/                     # Flask模板
│   └── logs.html                  # 日志查看器页面
└── static/                        # 静态文件
    └── css/
        └── logs.css               # 日志页面样式
```

## 🛠️ 实用工具

### 部署状态检查
```bash
./utilities/check_deployment.sh
```

检查内容包括：
- systemd服务状态
- 端口监听状态
- API健康状态
- GPU状态
- 服务日志
- 相关进程

### 批量任务启动
```bash
python3 utilities/start_all_tasks.py
```

功能：
- 扫描DynamoDB中的所有任务
- 批量提交视频生成任务
- 支持过滤和状态检查

## 📞 支持

如遇问题，请检查：
1. 服务日志：`tail -f cosmos_api.log`
2. 系统日志：`journalctl -u cosmos-api -f`
3. GPU状态：`nvidia-smi`
4. 服务状态：`curl http://localhost:8080/health`

---

**版本**: v3.0  
**更新时间**: 2025-06-11  
**支持**: MultiView + SingleView + 自动翻译 + GPU智能管理 + 实时日志 + Web界面
