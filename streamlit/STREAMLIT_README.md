# Cosmos视频生成场景管理系统 - Streamlit界面

## 🚀 快速开始

### 1. 安装依赖
```bash
pip3 install -r requirements_streamlit.txt
```

### 2. 启动应用
```bash
# 方法1: 使用启动脚本
./start_streamlit.sh

# 方法2: 直接启动
streamlit run streamlit_app.py --server.port=5000 --server.address=0.0.0.0
```

### 3. 访问界面
打开浏览器访问: `http://localhost:5000`

## 📋 功能说明

### 🎨 场景生成
1. **输入场景描述**: 输入简短的场景描述（如"雨后晚上的城市道路"）
2. **选择场景类型**: 
   - SingleView: 单视角场景
   - MultiView: 多视角场景（6个视角）
3. **生成增强描述**: 调用AI模型生成详细的场景描述
4. **自动保存**: 生成的场景自动保存到DynamoDB

### 📚 场景管理
1. **查看场景列表**: 显示所有已生成的场景
2. **场景详情**: 查看场景的详细描述信息
3. **编辑场景**: 修改场景描述（开发中）
4. **删除场景**: 删除不需要的场景

### 🎥 视频生成
1. **选择场景**: 从场景库中选择要生成视频的场景
2. **提交任务**: 提交视频生成任务到Cosmos API
3. **查询状态**: 实时查询任务执行状态
4. **系统监控**: 查看GPU使用情况和队列状态

### 📋 日志诊断
1. **实时日志查看**: 查看系统运行日志
2. **任务日志过滤**: 根据UUID查看特定任务日志
3. **嵌入式日志**: 在界面中直接查看日志
4. **快速链接**: 便捷访问各种日志端点
5. **常用UUID管理**: 保存常用的任务UUID

## 🔧 配置说明

### API配置
在 `config_streamlit.py` 中配置API地址和密钥：
```python
ENHANCE_API_URL = "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/enhence"
LIBRARY_API_URL = "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/library"
COSMOS_API_URL = "http://localhost:8080"
COSMOS_LOG_URL = "http://54.202.70.20:8080"  # 日志服务器地址
API_KEY = "your-api-key"
```

### 端口配置
默认端口: 5000
如需修改，编辑 `start_streamlit.sh` 中的端口设置

## 📊 使用流程

### 完整工作流程
1. **场景生成** → 输入描述 → AI增强 → 保存到库
2. **场景管理** → 查看/编辑/删除场景
3. **视频生成** → 选择场景 → 提交任务 → 监控进度

### 典型使用场景
```
用户输入: "雨后晚上的城市道路"
↓
AI增强生成详细的6视角场景描述
↓
保存到场景库
↓
选择场景提交视频生成任务
↓
监控任务状态直到完成
```

## 🚨 注意事项

1. **API限制**: 场景增强API有调用频率限制
2. **生成时间**: 
   - 场景增强: 1-2分钟
   - 视频生成: SingleView 1小时，MultiView 2小时
3. **网络要求**: 需要稳定的网络连接访问AWS API
4. **依赖服务**: 确保Cosmos API服务正在运行

## 🔍 故障排除

### 常见问题
1. **无法连接API**: 检查网络连接和API地址配置
2. **场景生成失败**: 检查API密钥和描述内容
3. **视频生成失败**: 确保Cosmos API服务运行正常
4. **页面加载慢**: 检查API响应时间和网络状态

### 日志查看
- Streamlit日志: 终端输出
- Cosmos API日志: http://localhost:8080/logs
- 系统状态: 界面中的"系统状态"功能

## 📞 支持

如遇问题，请检查：
1. 所有依赖服务是否正常运行
2. API配置是否正确
3. 网络连接是否稳定
4. 查看相关日志信息
