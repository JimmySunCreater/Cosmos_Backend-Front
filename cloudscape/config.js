// 配置文件 - 基于Streamlit配置转换
const CONFIG = {
    // API配置
    ENHANCE_API_URL: "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/enhence",
    WEBSOCKET_ENHANCE_URL: "wss://qopfrzscp0.execute-api.us-west-2.amazonaws.com/prod",
    LIBRARY_API_URL: "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/library",
    API_KEY: "C2G4GCEdCP2KMKYKZlpxgaX28k2ud4sxY4gEa3Zh",
    
    // Cosmos服务器配置 - 动态获取
    COSMOS_PRIVATE_IP: "172.31.8.172", // 默认值，会被动态更新
    COSMOS_PUBLIC_IP: null,
    
    // 计算属性
    get COSMOS_API_URL() {
        return `http://${this.COSMOS_PRIVATE_IP}:8080`;
    },
    
    get COSMOS_LOG_URL() {
        return this.COSMOS_PUBLIC_IP ? 
            `http://${this.COSMOS_PUBLIC_IP}:8080` : 
            `http://${this.COSMOS_PRIVATE_IP}:8080`;
    },
    
    // 通用请求头
    COMMON_HEADERS: {
        "Content-Type": "application/json",
        "x-api-key": "C2G4GCEdCP2KMKYKZlpxgaX28k2ud4sxY4gEa3Zh"
    },
    
    // API超时设置
    API_TIMEOUT: {
        enhance: 120000,  // 场景增强API超时时间（毫秒）
        library: 30000,   // 场景库API超时时间（毫秒）
        cosmos: 30000     // Cosmos API超时时间（毫秒）
    },
    
    // 场景类型配置
    SCENE_TYPES: {
        "SingleView": {
            name: "单视角",
            description: "单一视角场景，生成前方视角描述，适合简单场景",
            estimatedTime: "约1小时"
        },
        "MultiView": {
            name: "多视角", 
            description: "多视角场景，生成6个视角描述，适合复杂场景",
            estimatedTime: "约2小时"
        }
    },
    
    // 多视角视角配置
    MULTIVIEW_ANGLES: [
        { name: "前方", key: "PROMPT_FRONT" },
        { name: "左前方", key: "PROMPT_FRONT_LEFT" },
        { name: "右前方", key: "PROMPT_FRONT_RIGHT" },
        { name: "后方", key: "PROMPT_BACK" },
        { name: "左后方", key: "PROMPT_BACK_LEFT" },
        { name: "右后方", key: "PROMPT_BACK_RIGHT" }
    ],
    
    // 状态映射
    STATUS_MAPPING: {
        "Waiting": { variant: "info", text: "等待中" },
        "Generating": { variant: "warning", text: "生成中" },
        "Finished": { variant: "success", text: "已完成" },
        "Failed": { variant: "error", text: "失败" }
    },
    
    // 目标实例ID列表，按优先级排序
    TARGET_INSTANCES: [
        "i-0bbe2d67c7493574f",
        "i-07997436e1281b482"
    ]
};

// 动态获取可用的Cosmos服务器IP地址
async function getAvailableCosmosServer() {
    try {
        // 这里应该调用AWS API获取实例信息
        // 由于浏览器环境限制，我们使用默认配置
        // 在实际部署中，可以通过后端API来获取这些信息
        console.log("使用默认Cosmos服务器配置");
        return {
            privateIp: "172.31.8.172",
            publicIp: null
        };
    } catch (error) {
        console.warn("获取服务器IP时出错:", error);
        return {
            privateIp: "172.31.8.172",
            publicIp: null
        };
    }
}

// 初始化配置
async function initializeConfig() {
    const serverInfo = await getAvailableCosmosServer();
    CONFIG.COSMOS_PRIVATE_IP = serverInfo.privateIp;
    CONFIG.COSMOS_PUBLIC_IP = serverInfo.publicIp;
    console.log("配置初始化完成:", {
        cosmosApiUrl: CONFIG.COSMOS_API_URL,
        cosmosLogUrl: CONFIG.COSMOS_LOG_URL
    });
}

// 页面加载时初始化配置
document.addEventListener('DOMContentLoaded', initializeConfig);
