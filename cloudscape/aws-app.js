// AWS风格应用JavaScript

// 配置信息
const CONFIG = {
    ENHANCE_API_URL: "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/enhence",
    LIBRARY_API_URL: "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/library",
    COSMOS_API_URL: "http://172.31.8.172:8080",
    COSMOS_LOG_URL: "http://35.86.89.178:8080",
    API_KEY: "C2G4GCEdCP2KMKYKZlpxgaX28k2ud4sxY4gEa3Zh"
};

// 通用请求头
const COMMON_HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": CONFIG.API_KEY
};

// 全局状态
let currentScenes = [];

// 工具函数
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function formatTime(timeString) {
    if (!timeString) return 'N/A';
    try {
        const date = new Date(timeString);
        return date.toLocaleDateString('zh-CN');
    } catch (error) {
        return timeString.substring(0, 10);
    }
}

function formatDescription(description, maxLength = 50) {
    if (!description) return 'No description';
    return description.length > maxLength ? 
        description.substring(0, maxLength) + '...' : 
        description;
}

// AWS风格消息显示
function showAWSMessage(message, type = 'info', container = null) {
    const alertTypes = {
        success: { icon: '✅', class: 'aws-alert-success' },
        error: { icon: '❌', class: 'aws-alert-error' },
        warning: { icon: '⚠️', class: 'aws-alert-warning' },
        info: { icon: 'ℹ️', class: 'aws-alert-info' }
    };
    
    const alertInfo = alertTypes[type] || alertTypes.info;
    
    const alertHtml = `
        <div class="aws-alert ${alertInfo.class}" style="margin-bottom: var(--aws-space-l);">
            <span class="aws-alert-icon">${alertInfo.icon}</span>
            <div>${message}</div>
        </div>
    `;
    
    // 找到目标容器
    const targetContainer = container || document.querySelector('.tab-content:not(.aws-hidden)');
    if (targetContainer) {
        // 移除旧的alert
        const oldAlerts = targetContainer.querySelectorAll('.aws-alert');
        oldAlerts.forEach(alert => alert.remove());
        
        // 添加新的alert
        targetContainer.insertAdjacentHTML('afterbegin', alertHtml);
        
        // 5秒后自动移除
        setTimeout(() => {
            const alert = targetContainer.querySelector('.aws-alert');
            if (alert) alert.remove();
        }, 5000);
    }
}

// 标签页切换
function showTab(tabName) {
    // 隐藏所有标签内容
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('aws-hidden');
    });
    
    // 移除所有按钮的active类
    document.querySelectorAll('.aws-tab').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示选中的标签内容
    document.getElementById(tabName).classList.remove('aws-hidden');
    
    // 激活对应按钮
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // 更新URL hash
    window.location.hash = tabName;
}

// 场景生成
async function generateScene() {
    const sceneDesc = document.getElementById('scene-desc').value.trim();
    const sceneType = document.getElementById('scene-type').value;
    const useStreaming = document.getElementById('use-streaming').checked;
    
    if (!sceneDesc) {
        showAWSMessage('请输入场景描述', 'error');
        return;
    }
    
    const sceneUuid = generateUUID();
    const payload = {
        scene_description: sceneDesc,
        uuid: sceneUuid,
        SceneType: sceneType
    };
    
    // 显示加载状态
    const resultDiv = document.getElementById('generation-result');
    const contentDiv = document.getElementById('result-content');
    
    resultDiv.classList.remove('aws-hidden');
    contentDiv.innerHTML = `
        <div class="aws-loading">
            <div class="aws-spinner"></div>
            <span>正在生成${sceneType === 'SingleView' ? '单视角' : '多视角'}场景描述，请稍候...</span>
        </div>
    `;
    
    try {
        const response = await fetch(CONFIG.ENHANCE_API_URL, {
            method: 'POST',
            headers: COMMON_HEADERS,
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            const result = await response.text();
            showAWSMessage('场景描述生成成功！', 'success');
            
            // 显示结果
            contentDiv.innerHTML = `
                <div class="aws-alert aws-alert-info">
                    <span class="aws-alert-icon">🆔</span>
                    <div><strong>场景UUID:</strong> ${sceneUuid}</div>
                </div>
                <div class="aws-form-group">
                    <label class="aws-form-label">增强后的场景描述</label>
                    <textarea class="aws-form-textarea" readonly rows="10">${result}</textarea>
                </div>
                <div style="margin-top: var(--aws-space-m);">
                    <button class="aws-btn aws-btn-outline" onclick="copyToClipboard('${sceneUuid}')">
                        <span>📋</span>
                        复制UUID
                    </button>
                </div>
            `;
        } else {
            throw new Error(`API调用失败: ${response.status} - ${response.statusText}`);
        }
    } catch (error) {
        showAWSMessage(`生成失败: ${error.message}`, 'error');
        contentDiv.innerHTML = `
            <div class="aws-alert aws-alert-error">
                <span class="aws-alert-icon">❌</span>
                <div>生成失败，请稍后重试</div>
            </div>
        `;
    }
}

// 加载场景列表
async function loadScenes() {
    const listDiv = document.getElementById('scenes-list');
    listDiv.innerHTML = `
        <div class="aws-loading">
            <div class="aws-spinner"></div>
            <span>正在加载场景列表...</span>
        </div>
    `;
    
    try {
        const response = await fetch(`${CONFIG.LIBRARY_API_URL}?limit=100`, {
            headers: COMMON_HEADERS
        });
        
        if (response.ok) {
            const data = await response.json();
            const scenes = data.data || [];
            currentScenes = scenes;
            
            if (scenes.length === 0) {
                listDiv.innerHTML = `
                    <div class="aws-alert aws-alert-info">
                        <span class="aws-alert-icon">ℹ️</span>
                        <div>暂无场景数据，请先生成一些场景</div>
                    </div>
                `;
                return;
            }
            
            // 渲染场景列表
            let html = '';
            scenes.forEach((scene, index) => {
                const sceneType = scene.SceneType || 'Unknown';
                const description = formatDescription(scene.scene_description, 80);
                const updateTime = formatTime(scene.update_time);
                const hasVideo = scene.video_link;
                
                html += `
                    <div class="aws-card" style="margin-bottom: var(--aws-space-m);">
                        <div style="display: flex; justify-content: between; align-items: flex-start; margin-bottom: var(--aws-space-m);">
                            <div style="flex: 1;">
                                <div style="display: flex; align-items: center; margin-bottom: var(--aws-space-s);">
                                    <span class="aws-status ${sceneType === 'SingleView' ? 'aws-status-info' : 'aws-status-warning'}">${sceneType === 'SingleView' ? '单视角' : '多视角'}</span>
                                    <span class="aws-status ${hasVideo ? 'aws-status-success' : 'aws-status-warning'}" style="margin-left: var(--aws-space-s);">
                                        ${hasVideo ? '已生成视频' : '未生成视频'}
                                    </span>
                                </div>
                                <h4 style="color: var(--aws-blue); margin-bottom: var(--aws-space-s);">${description}</h4>
                                <div style="color: var(--aws-gray-600); font-size: 14px; margin-bottom: var(--aws-space-s);">
                                    <strong>UUID:</strong> ${scene.uuid}<br>
                                    <strong>更新时间:</strong> ${updateTime}
                                </div>
                                ${hasVideo ? `
                                    <a href="https://${scene.video_link}" target="_blank" class="aws-btn aws-btn-outline" style="margin-top: var(--aws-space-s);">
                                        <span>🎥</span>
                                        查看视频
                                    </a>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            listDiv.innerHTML = html;
            
            // 更新视频生成页面的选择框
            updateVideoSceneSelect(scenes);
            
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        listDiv.innerHTML = `
            <div class="aws-alert aws-alert-error">
                <span class="aws-alert-icon">❌</span>
                <div>获取场景列表失败: ${error.message}</div>
            </div>
        `;
    }
}

// 更新视频场景选择框
function updateVideoSceneSelect(scenes) {
    const select = document.getElementById('video-scene-select');
    select.innerHTML = '<option value="">请选择场景</option>';
    
    scenes.forEach(scene => {
        const sceneType = scene.SceneType || 'Unknown';
        const description = formatDescription(scene.scene_description, 50);
        const option = document.createElement('option');
        option.value = scene.uuid;
        option.textContent = `${sceneType === 'SingleView' ? '单视角' : '多视角'} - ${description}`;
        select.appendChild(option);
    });
}

// 提交视频生成
async function submitVideoGeneration() {
    const sceneUuid = document.getElementById('video-scene-select').value;
    
    if (!sceneUuid) {
        showAWSMessage('请选择场景', 'error');
        return;
    }
    
    const resultDiv = document.getElementById('video-result');
    resultDiv.innerHTML = `
        <div class="aws-loading">
            <div class="aws-spinner"></div>
            <span>正在提交视频生成任务...</span>
        </div>
    `;
    
    try {
        const response = await fetch(`${CONFIG.COSMOS_API_URL}/generate`, {
            method: 'POST',
            headers: COMMON_HEADERS,
            body: JSON.stringify({ uuid: sceneUuid })
        });
        
        if (response.ok) {
            const result = await response.json();
            showAWSMessage('视频生成任务提交成功！', 'success');
            
            resultDiv.innerHTML = `
                <div class="aws-card" style="background: var(--aws-gray-50); margin: 0;">
                    <div class="aws-alert aws-alert-success">
                        <span class="aws-alert-icon">✅</span>
                        <div><strong>任务提交成功</strong></div>
                    </div>
                    <div class="aws-grid aws-grid-2">
                        <div>
                            <div style="margin-bottom: var(--aws-space-s);"><strong>任务UUID:</strong> ${sceneUuid}</div>
                            <div style="margin-bottom: var(--aws-space-s);"><strong>场景类型:</strong> ${result.scene_type || 'Unknown'}</div>
                            <div><strong>队列位置:</strong> ${result.queue_position || 'Unknown'}</div>
                        </div>
                        <div>
                            <button class="aws-btn aws-btn-outline" onclick="checkTaskStatus()">
                                <span>🔍</span>
                                查询状态
                            </button>
                        </div>
                    </div>
                </div>
            `;
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        showAWSMessage(`提交失败: ${error.message}`, 'error');
        resultDiv.innerHTML = '';
    }
}

// 查询任务状态
async function checkTaskStatus() {
    const sceneUuid = document.getElementById('video-scene-select').value;
    
    if (!sceneUuid) {
        showAWSMessage('请选择场景', 'error');
        return;
    }
    
    const resultDiv = document.getElementById('video-result');
    
    try {
        const response = await fetch(`${CONFIG.COSMOS_API_URL}/status/${sceneUuid}`);
        
        if (response.ok) {
            const status = await response.json();
            const statusText = status.generation_status || 'Unknown';
            
            let statusClass = 'aws-status-warning';
            let statusIcon = '⏳';
            if (statusText === 'Finished') {
                statusClass = 'aws-status-success';
                statusIcon = '✅';
            } else if (statusText === 'Failed') {
                statusClass = 'aws-status-error';
                statusIcon = '❌';
            } else if (statusText === 'Generating') {
                statusIcon = '🔄';
            }
            
            resultDiv.innerHTML = `
                <div class="aws-card" style="background: var(--aws-gray-50); margin: 0;">
                    <h4 style="color: var(--aws-blue); margin-bottom: var(--aws-space-m);">任务状态</h4>
                    <div style="display: flex; align-items: center; margin-bottom: var(--aws-space-m);">
                        <span style="font-size: 24px; margin-right: var(--aws-space-s);">${statusIcon}</span>
                        <span class="aws-status ${statusClass}">${statusText}</span>
                    </div>
                    ${status.video_link ? `
                        <div class="aws-alert aws-alert-success">
                            <span class="aws-alert-icon">🎥</span>
                            <div>
                                <strong>视频已生成完成！</strong><br>
                                <a href="https://${status.video_link}" target="_blank" class="aws-btn aws-btn-primary" style="margin-top: var(--aws-space-s);">
                                    <span>🎬</span>
                                    查看视频
                                </a>
                            </div>
                        </div>
                    ` : ''}
                    <details style="margin-top: var(--aws-space-m);">
                        <summary style="cursor: pointer; color: var(--aws-blue);">查看详细信息</summary>
                        <pre class="aws-code" style="margin-top: var(--aws-space-s);">${JSON.stringify(status, null, 2)}</pre>
                    </details>
                </div>
            `;
        } else if (response.status === 404) {
            showAWSMessage('任务未找到，请确认UUID是否正确', 'warning');
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        showAWSMessage(`查询失败: ${error.message}`, 'error');
    }
}

// 检查系统状态
async function checkSystemStatus() {
    const metricsDiv = document.getElementById('system-metrics');
    const infoDiv = document.getElementById('system-info');
    
    // 重置指标显示
    document.getElementById('active-tasks').textContent = '-';
    document.getElementById('available-gpu').textContent = '-';
    document.getElementById('queue-size').textContent = '-';
    
    infoDiv.innerHTML = `
        <div class="aws-loading">
            <div class="aws-spinner"></div>
            <span>正在检查系统状态...</span>
        </div>
    `;
    
    try {
        const response = await fetch(`${CONFIG.COSMOS_API_URL}/health`);
        
        if (response.ok) {
            const status = await response.json();
            const gpuStatus = status.gpu_status_detail || '0/8 GPUs available';
            const gpuCount = gpuStatus.split(' ')[0];
            
            // 更新指标
            document.getElementById('active-tasks').textContent = status.active_tasks || 0;
            document.getElementById('available-gpu').textContent = gpuCount;
            document.getElementById('queue-size').textContent = status.queue_size || 0;
            
            // 显示系统信息
            infoDiv.innerHTML = `
                <div class="aws-alert aws-alert-success">
                    <span class="aws-alert-icon">✅</span>
                    <div><strong>系统运行正常</strong></div>
                </div>
                <div style="margin-top: var(--aws-space-m);">
                    <h4 style="color: var(--aws-blue); margin-bottom: var(--aws-space-s);">GPU状态详情</h4>
                    <p style="color: var(--aws-gray-700);">${status.gpu_status_detail}</p>
                </div>
                <details style="margin-top: var(--aws-space-m);">
                    <summary style="cursor: pointer; color: var(--aws-blue);">查看完整状态</summary>
                    <pre class="aws-code" style="margin-top: var(--aws-space-s);">${JSON.stringify(status, null, 2)}</pre>
                </details>
            `;
            
            showAWSMessage('系统状态检查完成', 'success');
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        infoDiv.innerHTML = `
            <div class="aws-alert aws-alert-error">
                <span class="aws-alert-icon">❌</span>
                <div>无法连接到视频生成服务: ${error.message}</div>
            </div>
        `;
        showAWSMessage(`系统状态检查失败: ${error.message}`, 'error');
    }
}

// 打开日志页面
function openLogPage() {
    window.open(`${CONFIG.COSMOS_LOG_URL}/logs`, '_blank');
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAWSMessage('UUID已复制到剪贴板', 'success');
    }).catch(() => {
        showAWSMessage('复制失败，请手动复制', 'error');
    });
}

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('Amazon Cosmos AWS风格界面已加载');
    
    // 根据URL hash显示对应标签页
    const hash = window.location.hash.substring(1);
    if (hash && document.getElementById(hash)) {
        showTab(hash);
    }
    
    // 显示欢迎消息
    setTimeout(() => {
        showAWSMessage('欢迎使用 Amazon Cosmos 视频生成场景管理系统！', 'success');
    }, 1000);
    
    // 监听hash变化
    window.addEventListener('hashchange', function() {
        const hash = window.location.hash.substring(1);
        if (hash && document.getElementById(hash)) {
            showTab(hash);
        }
    });
});

// 导出全局函数
window.showTab = showTab;
window.generateScene = generateScene;
window.loadScenes = loadScenes;
window.submitVideoGeneration = submitVideoGeneration;
window.checkTaskStatus = checkTaskStatus;
window.checkSystemStatus = checkSystemStatus;
window.openLogPage = openLogPage;
window.copyToClipboard = copyToClipboard;
