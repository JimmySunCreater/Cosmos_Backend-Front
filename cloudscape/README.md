# Cosmos CloudScape界面

这是Cosmos视频生成系统的CloudScape风格Web界面，基于AWS CloudScape Design System构建，提供现代化的用户体验。

## 📁 文件结构

```
cloudscape/
├── index.html                    # 主HTML文件
├── config.js                     # 配置文件
├── api.js                        # API工具函数
├── app.js                        # 主应用组件
├── styles.css                    # 自定义样式
├── start_server.sh              # 启动脚本
├── README.md                    # 本文件
└── components/                  # 组件目录
    ├── SceneGeneration.js       # 场景生成组件
    ├── SceneManagement.js       # 场景管理组件
    ├── VideoGeneration.js       # 视频生成组件
    └── LogDiagnosis.js          # 日志诊断组件
```

## 🚀 快速启动

### 推荐方式: 使用启动脚本
```bash
cd /home/ubuntu/cosmos_service/cloudscape
./start_server.sh
```

### 直接启动
```bash
cd /home/ubuntu/cosmos_service/cloudscape
python3 -m http.server 5001
```

## 🌐 访问界面

启动后访问: `http://localhost:5001`

## 🎨 设计特色

### CloudScape Design System
- 使用AWS官方设计系统
- 现代化的UI组件
- 一致的用户体验
- 响应式设计
- 无障碍访问支持

### 核心特性
- **单页应用**: 基于React构建的SPA
- **组件化架构**: 模块化的组件设计
- **响应式布局**: 适配各种屏幕尺寸
- **实时更新**: 支持数据实时刷新
- **错误处理**: 完善的错误提示和处理

## 📋 主要功能

### 🎨 场景生成
- 智能场景描述生成
- 支持单视角和多视角模式
- 流式生成和传统生成两种模式
- 实时进度显示
- 自动保存到场景库

### 📚 场景管理
- 场景列表展示和管理
- 详细信息查看
- 多视角内容展示（使用Tabs）
- 场景删除功能
- 视频状态显示

### 🎥 视频生成
- 场景选择和预览
- 视频生成任务提交
- 任务状态实时查询
- 系统状态监控
- 完成后视频链接展示

### 📊 日志诊断
- 嵌入式日志查看
- 响应式iframe高度调整
- 支持新窗口打开
- 系统状态诊断

## ⚙️ 技术架构

### 前端技术栈
- **React 18**: 用户界面库
- **CloudScape Design System**: AWS官方UI组件库
- **原生JavaScript**: 无需构建工具
- **CSS3**: 响应式样式设计

### API集成
- **REST API**: 传统HTTP请求
- **WebSocket**: 流式数据传输
- **AWS API Gateway**: 云端API服务
- **本地Cosmos API**: 视频生成服务

### 配置管理
```javascript
// 主要配置项
const CONFIG = {
    ENHANCE_API_URL: "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/enhence",
    WEBSOCKET_ENHANCE_URL: "wss://qopfrzscp0.execute-api.us-west-2.amazonaws.com/prod",
    LIBRARY_API_URL: "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/library",
    COSMOS_API_URL: "http://172.31.8.172:8080",
    API_KEY: "C2G4GCEdCP2KMKYKZlpxgaX28k2ud4sxY4gEa3Zh"
};
```

## 🎯 响应式设计

### 断点设置
- **超小屏幕**: <576px - 手机
- **小屏幕**: 576-767px - 平板竖屏
- **中等屏幕**: 768-1199px - 平板横屏
- **大屏幕**: ≥1200px - 桌面显示器
- **4K屏幕**: ≥3840px - 4K显示器

### 适配特性
- 自适应网格布局
- 响应式字体大小
- 移动端优化交互
- 4K屏幕特别优化
- 高对比度模式支持

## 🔧 开发说明

### 组件开发
每个组件都是独立的JavaScript文件，使用React函数组件：

```javascript
function ComponentName({ props }) {
    const [state, setState] = useState(initialValue);
    
    return React.createElement(CloudscapeComponent, {
        // props
    }, children);
}

window.ComponentName = ComponentName;
```

### API调用
使用统一的API客户端：

```javascript
// 调用API
const result = await apiClient.enhanceScene(description, type);

// 处理错误
try {
    const data = await apiClient.getScenes();
} catch (error) {
    console.error('API调用失败:', error.message);
}
```

### 状态管理
使用React Hooks进行状态管理：

```javascript
const [loading, setLoading] = useState(false);
const [data, setData] = useState([]);
const [error, setError] = useState(null);
```

## 🔄 与Streamlit版本的对比

| 特性 | Streamlit版本 | CloudScape版本 |
|------|---------------|----------------|
| 技术栈 | Python + Streamlit | React + CloudScape |
| 部署方式 | Python服务器 | 静态文件服务 |
| 用户体验 | 传统Web应用 | 现代SPA体验 |
| 响应式设计 | 基础响应式 | 完全响应式 |
| 组件复用 | 有限 | 高度模块化 |
| 性能 | 服务器渲染 | 客户端渲染 |
| 维护性 | Python依赖 | 纯前端代码 |

## 🛠️ 维护和部署

### 本地开发
```bash
# 启动开发服务器
cd /home/ubuntu/cosmos_service/cloudscape
./start_server.sh
```

### 生产部署
可以部署到任何静态文件服务器：
- Apache HTTP Server
- Nginx
- AWS S3 + CloudFront
- GitHub Pages

### 配置更新
修改 `config.js` 文件中的配置项：
```javascript
// 更新API地址
CONFIG.COSMOS_API_URL = "http://new-server:8080";

// 更新API密钥
CONFIG.API_KEY = "new-api-key";
```

## 🔒 安全考虑

- API密钥存储在客户端（开发环境）
- 生产环境建议使用环境变量或配置服务
- CORS配置确保跨域安全
- 输入验证和错误处理

## 📞 技术支持

- 基于原Streamlit版本的功能逻辑
- 保持与后端API的完全兼容
- 支持所有原有功能特性
- 提供更好的用户体验

## 🔮 未来规划

- [ ] 添加深色模式支持
- [ ] 实现离线缓存功能
- [ ] 添加用户认证系统
- [ ] 支持多语言国际化
- [ ] 添加数据可视化图表
- [ ] 实现实时通知系统
