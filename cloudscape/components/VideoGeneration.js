// 视频生成组件
function VideoGeneration({ refreshTrigger }) {
    // 确保React和CloudScape已加载
    if (typeof React === 'undefined' || typeof CloudscapeDesignSystem === 'undefined') {
        return null;
    }
    
    const { useState, useEffect } = React;
    const { 
        Container, 
        Header, 
        SpaceBetween, 
        Grid, 
        FormField,
        Select,
        Button, 
        Alert, 
        Box,
        Textarea,
        StatusIndicator,
        ExpandableSection,
        KeyValuePairs,
        ProgressBar
    } = CloudscapeDesignSystem;

function VideoGeneration({ refreshTrigger }) {
    const [scenes, setScenes] = useState([]);
    const [selectedScene, setSelectedScene] = useState(null);
    const [loading, setLoading] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [checking, setChecking] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [taskStatus, setTaskStatus] = useState(null);
    const [systemStatus, setSystemStatus] = useState(null);

    // 加载场景列表
    const loadScenes = async () => {
        setLoading(true);
        setError(null);
        try {
            const scenesData = await apiClient.getScenes();
            setScenes(scenesData);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    // 初始加载和刷新触发
    useEffect(() => {
        loadScenes();
    }, [refreshTrigger]);

    // 提交视频生成任务
    const handleSubmitGeneration = async () => {
        if (!selectedScene) {
            setError('请选择场景');
            return;
        }

        setSubmitting(true);
        setError(null);
        setSuccess(null);

        try {
            const result = await apiClient.submitVideoGeneration(selectedScene.value);
            setSuccess('视频生成任务提交成功！');
            
            // 显示任务信息
            const taskInfo = {
                uuid: selectedScene.value,
                sceneType: result.scene_type || 'Unknown',
                queuePosition: result.queue_position || 'Unknown'
            };
            setTaskStatus(taskInfo);
        } catch (error) {
            setError(error.message);
        } finally {
            setSubmitting(false);
        }
    };

    // 查询任务状态
    const handleCheckStatus = async () => {
        if (!selectedScene) {
            setError('请选择场景');
            return;
        }

        setChecking(true);
        setError(null);

        try {
            const status = await apiClient.getTaskStatus(selectedScene.value);
            setTaskStatus(status);
        } catch (error) {
            setError(error.message);
        } finally {
            setChecking(false);
        }
    };

    // 检查系统状态
    const handleCheckSystemStatus = async () => {
        setError(null);
        try {
            const status = await apiClient.getSystemStatus();
            setSystemStatus(status);
        } catch (error) {
            setError(error.message);
        }
    };

    // 格式化场景选项
    const sceneOptions = scenes.map(scene => ({
        value: scene.uuid,
        label: `${CONFIG.SCENE_TYPES[scene.SceneType]?.name || scene.SceneType} - ${apiClient.formatSceneDescription(scene.scene_description, 50)}`,
        scene: scene
    }));

    // 获取选中场景的详细信息
    const selectedSceneDetail = selectedScene ? 
        scenes.find(scene => scene.uuid === selectedScene.value) : null;

    // 渲染任务状态
    const renderTaskStatus = () => {
        if (!taskStatus) return null;

        const statusInfo = apiClient.getStatusInfo(taskStatus.generation_status);
        
        return React.createElement(ExpandableSection, {
            headerText: "任务状态",
            defaultExpanded: true
        },
            React.createElement(SpaceBetween, { direction: "vertical", size: "m" },
                React.createElement(StatusIndicator, { 
                    type: statusInfo.variant === 'success' ? 'success' : 
                          statusInfo.variant === 'warning' ? 'loading' :
                          statusInfo.variant === 'error' ? 'error' : 'info'
                }, statusInfo.text),

                React.createElement(KeyValuePairs, {
                    columns: 2,
                    items: [
                        { label: "任务UUID", value: taskStatus.uuid || selectedScene?.value },
                        { label: "场景类型", value: taskStatus.scene_type || taskStatus.sceneType },
                        { label: "队列位置", value: taskStatus.queue_position || taskStatus.queuePosition },
                        { label: "状态", value: statusInfo.text }
                    ].filter(item => item.value)
                }),

                // 如果任务完成且有视频链接
                taskStatus.generation_status === 'Finished' && taskStatus.video_link && 
                React.createElement(Alert, { type: "success" },
                    React.createElement(SpaceBetween, { direction: "vertical", size: "s" },
                        React.createElement(Box, null, "视频生成完成！"),
                        React.createElement(Box, null,
                            React.createElement("a", {
                                href: `https://${taskStatus.video_link}`,
                                target: "_blank",
                                rel: "noopener noreferrer"
                            }, "查看/下载视频")
                        )
                    )
                ),

                // 显示详细信息
                React.createElement(ExpandableSection, {
                    headerText: "详细信息"
                },
                    React.createElement("pre", {
                        style: { 
                            backgroundColor: '#f5f5f5', 
                            padding: '10px', 
                            borderRadius: '4px',
                            fontSize: '12px',
                            overflow: 'auto'
                        }
                    }, JSON.stringify(taskStatus, null, 2))
                )
            )
        );
    };

    // 渲染系统状态
    const renderSystemStatus = () => {
        if (!systemStatus) return null;

        const gpuStatusDetail = systemStatus.gpu_status_detail || '0/8 GPUs available';
        const gpuStatus = gpuStatusDetail.split(' ')[0]; // 获取"0/8"部分

        return React.createElement(SpaceBetween, { direction: "vertical", size: "m" },
            React.createElement(StatusIndicator, { type: "success" }, "系统运行正常"),
            
            React.createElement(Grid, {
                gridDefinition: [
                    { colspan: 4 },
                    { colspan: 4 },
                    { colspan: 4 }
                ]
            },
                React.createElement(Box, { textAlign: "center" },
                    React.createElement(Box, { variant: "h4" }, "活跃任务"),
                    React.createElement(Box, { 
                        fontSize: "display-l",
                        fontWeight: "bold"
                    }, systemStatus.active_tasks || 0)
                ),
                React.createElement(Box, { textAlign: "center" },
                    React.createElement(Box, { variant: "h4" }, "可用GPU"),
                    React.createElement(Box, { 
                        fontSize: "display-l",
                        fontWeight: "bold"
                    }, gpuStatus)
                ),
                React.createElement(Box, { textAlign: "center" },
                    React.createElement(Box, { variant: "h4" }, "队列任务"),
                    React.createElement(Box, { 
                        fontSize: "display-l",
                        fontWeight: "bold"
                    }, systemStatus.queue_size || 0)
                )
            ),

            React.createElement(ExpandableSection, {
                headerText: "详细状态"
            },
                React.createElement("pre", {
                    style: { 
                        backgroundColor: '#f5f5f5', 
                        padding: '10px', 
                        borderRadius: '4px',
                        fontSize: '12px',
                        overflow: 'auto'
                    }
                }, JSON.stringify(systemStatus, null, 2))
            )
        );
    };

    return React.createElement(Container, {
        header: React.createElement(Header, {
            variant: "h2",
            description: "选择场景并提交视频生成任务"
        }, "视频生成")
    }, 
        React.createElement(SpaceBetween, { direction: "vertical", size: "l" },
            // 错误和成功提示
            error && React.createElement(Alert, {
                type: "error",
                dismissible: true,
                onDismiss: () => setError(null)
            }, error),
            
            success && React.createElement(Alert, {
                type: "success",
                dismissible: true,
                onDismiss: () => setSuccess(null)
            }, success),

            // 主要内容区域
            React.createElement(Grid, {
                gridDefinition: [
                    { colspan: { default: 12, xs: 8 } },
                    { colspan: { default: 12, xs: 4 } }
                ]
            },
                // 左侧操作区域
                React.createElement(SpaceBetween, { direction: "vertical", size: "l" },
                    // 场景选择
                    React.createElement(Container, {
                        header: React.createElement(Header, { variant: "h3" }, "选择场景")
                    },
                        React.createElement(SpaceBetween, { direction: "vertical", size: "m" },
                            React.createElement(FormField, {
                                label: "选择要生成视频的场景"
                            },
                                React.createElement(Select, {
                                    selectedOption: selectedScene,
                                    onChange: (event) => setSelectedScene(event.detail.selectedOption),
                                    options: sceneOptions,
                                    placeholder: "请选择场景",
                                    loading: loading,
                                    loadingText: "加载场景列表中..."
                                })
                            ),

                            // 场景预览
                            selectedSceneDetail && React.createElement(SpaceBetween, { 
                                direction: "vertical", 
                                size: "s" 
                            },
                                React.createElement(Box, { variant: "h4" }, "场景预览"),
                                React.createElement(KeyValuePairs, {
                                    columns: 2,
                                    items: [
                                        { 
                                            label: "类型", 
                                            value: CONFIG.SCENE_TYPES[selectedSceneDetail.SceneType]?.name || selectedSceneDetail.SceneType 
                                        },
                                        { label: "UUID", value: selectedSceneDetail.uuid }
                                    ]
                                }),
                                React.createElement(FormField, {
                                    label: "场景描述"
                                },
                                    React.createElement(Textarea, {
                                        value: selectedSceneDetail.scene_description || '',
                                        readOnly: true,
                                        rows: 4
                                    })
                                )
                            ),

                            // 操作按钮
                            React.createElement(SpaceBetween, { 
                                direction: "horizontal", 
                                size: "xs" 
                            },
                                React.createElement(Button, {
                                    variant: "primary",
                                    onClick: handleSubmitGeneration,
                                    loading: submitting,
                                    disabled: !selectedScene
                                }, "提交视频生成任务"),
                                React.createElement(Button, {
                                    onClick: handleCheckStatus,
                                    loading: checking,
                                    disabled: !selectedScene
                                }, "查询任务状态")
                            )
                        )
                    ),

                    // 任务状态显示
                    renderTaskStatus()
                ),

                // 右侧系统状态和说明
                React.createElement(SpaceBetween, { direction: "vertical", size: "m" },
                    React.createElement(Container, {
                        header: React.createElement(Header, { 
                            variant: "h3",
                            actions: React.createElement(Button, {
                                onClick: handleCheckSystemStatus
                            }, "检查系统状态")
                        }, "系统状态")
                    },
                        systemStatus ? renderSystemStatus() : 
                        React.createElement(Box, {
                            textAlign: "center",
                            color: "text-status-inactive"
                        }, "点击按钮检查系统状态")
                    ),

                    React.createElement(Container, {
                        header: React.createElement(Header, { variant: "h3" }, "生成说明")
                    },
                        React.createElement(SpaceBetween, { direction: "vertical", size: "s" },
                            React.createElement(Box, { variant: "h4" }, "视频生成流程："),
                            React.createElement(Box, null,
                                React.createElement("ol", null,
                                    React.createElement("li", null, "选择已生成的场景"),
                                    React.createElement("li", null, "点击提交生成任务"),
                                    React.createElement("li", null, "系统自动处理视频生成"),
                                    React.createElement("li", null, "完成后可通过状态查询查看结果")
                                )
                            ),
                            React.createElement(Box, { variant: "h4" }, "注意事项："),
                            React.createElement(Box, null,
                                React.createElement("ul", null,
                                    React.createElement("li", null, "确保场景描述完整"),
                                    React.createElement("li", null, "生成过程中请勿重复提交"),
                                    React.createElement("li", null, "可通过状态查询查看进度")
                                )
                            )
                        )
                    )
                )
            )
        )
    );
}

window.VideoGeneration = VideoGeneration;
