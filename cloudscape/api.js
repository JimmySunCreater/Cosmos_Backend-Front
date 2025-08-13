// API工具函数
class ApiClient {
    constructor() {
        this.config = CONFIG;
    }

    // 通用请求方法
    async request(url, options = {}) {
        const defaultOptions = {
            headers: this.config.COMMON_HEADERS,
            ...options
        };

        try {
            const response = await fetch(url, defaultOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            // 处理不同的响应类型
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                return await response.text();
            }
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    }

    // 场景增强API
    async enhanceScene(sceneDescription, sceneType) {
        const sceneUuid = this.generateUUID();
        
        const payload = {
            scene_description: sceneDescription,
            uuid: sceneUuid,
            SceneType: sceneType
        };

        try {
            const response = await this.request(this.config.ENHANCE_API_URL, {
                method: 'POST',
                body: JSON.stringify(payload)
            });

            return {
                uuid: sceneUuid,
                description: response
            };
        } catch (error) {
            throw new Error(`场景增强失败: ${error.message}`);
        }
    }

    // 流式场景增强API (WebSocket)
    async enhanceSceneStreaming(sceneDescription, sceneType, onProgress, onComplete, onError) {
        const sceneUuid = this.generateUUID();
        
        try {
            const ws = new WebSocket(this.config.WEBSOCKET_ENHANCE_URL);
            
            ws.onopen = () => {
                const payload = {
                    action: "enhance",
                    scene_description: sceneDescription,
                    uuid: sceneUuid,
                    SceneType: sceneType
                };
                ws.send(JSON.stringify(payload));
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'progress') {
                        onProgress && onProgress(data.content);
                    } else if (data.type === 'complete') {
                        onComplete && onComplete({
                            uuid: sceneUuid,
                            description: data.content
                        });
                        ws.close();
                    } else if (data.type === 'error') {
                        onError && onError(new Error(data.message));
                        ws.close();
                    }
                } catch (parseError) {
                    onError && onError(new Error('解析响应数据失败'));
                }
            };

            ws.onerror = (error) => {
                onError && onError(new Error('WebSocket连接失败'));
            };

            ws.onclose = (event) => {
                if (event.code !== 1000) {
                    onError && onError(new Error('WebSocket连接异常关闭'));
                }
            };

            return ws;
        } catch (error) {
            onError && onError(new Error(`流式增强失败: ${error.message}`));
        }
    }

    // 获取场景库列表
    async getScenes(limit = 100) {
        try {
            const response = await this.request(`${this.config.LIBRARY_API_URL}?limit=${limit}`);
            return response.data || [];
        } catch (error) {
            throw new Error(`获取场景列表失败: ${error.message}`);
        }
    }

    // 删除场景
    async deleteScene(sceneUuid) {
        try {
            await this.request(`${this.config.LIBRARY_API_URL}/${sceneUuid}`, {
                method: 'DELETE'
            });
            return true;
        } catch (error) {
            throw new Error(`删除场景失败: ${error.message}`);
        }
    }

    // 提交视频生成任务
    async submitVideoGeneration(sceneUuid) {
        try {
            const response = await this.request(`${this.config.COSMOS_API_URL}/generate`, {
                method: 'POST',
                body: JSON.stringify({ uuid: sceneUuid })
            });
            return response;
        } catch (error) {
            throw new Error(`提交视频生成失败: ${error.message}`);
        }
    }

    // 查询任务状态
    async getTaskStatus(taskUuid) {
        try {
            const response = await this.request(`${this.config.COSMOS_API_URL}/status/${taskUuid}`);
            return response;
        } catch (error) {
            if (error.message.includes('404')) {
                throw new Error('任务未找到');
            }
            throw new Error(`查询任务状态失败: ${error.message}`);
        }
    }

    // 检查系统状态
    async getSystemStatus() {
        try {
            const response = await this.request(`${this.config.COSMOS_API_URL}/health`);
            return response;
        } catch (error) {
            throw new Error(`获取系统状态失败: ${error.message}`);
        }
    }

    // 生成UUID
    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // 格式化时间
    formatTime(timeString) {
        if (!timeString) return 'N/A';
        try {
            const date = new Date(timeString);
            return date.toLocaleDateString('zh-CN');
        } catch (error) {
            return timeString.substring(0, 10);
        }
    }

    // 格式化场景描述用于显示
    formatSceneDescription(description, maxLength = 50) {
        if (!description) return 'No description';
        return description.length > maxLength ? 
            description.substring(0, maxLength) + '...' : 
            description;
    }

    // 获取状态显示信息
    getStatusInfo(status) {
        return this.config.STATUS_MAPPING[status] || {
            variant: "info",
            text: status || "未知状态"
        };
    }
}

// 创建全局API客户端实例
const apiClient = new ApiClient();
