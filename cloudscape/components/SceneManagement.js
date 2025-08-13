// 场景管理组件
function SceneManagement({ refreshTrigger }) {
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
        Table,
        Button, 
        Alert, 
        Box,
        Modal,
        FormField,
        Textarea,
        Tabs,
        StatusIndicator,
        Badge,
        Link
    } = CloudscapeDesignSystem;

function SceneManagement({ refreshTrigger }) {
    const [scenes, setScenes] = useState([]);
    const [selectedScene, setSelectedScene] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [sceneToDelete, setSceneToDelete] = useState(null);

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

    // 删除场景
    const handleDeleteScene = async () => {
        if (!sceneToDelete) return;

        try {
            await apiClient.deleteScene(sceneToDelete.uuid);
            setSuccess('场景删除成功！');
            setShowDeleteModal(false);
            setSceneToDelete(null);
            setSelectedScene(null);
            await loadScenes();
        } catch (error) {
            setError(error.message);
        }
    };

    // 表格列定义
    const columnDefinitions = [
        {
            id: "sceneType",
            header: "类型",
            cell: item => React.createElement(Badge, {
                color: item.SceneType === 'SingleView' ? 'blue' : 'green'
            }, CONFIG.SCENE_TYPES[item.SceneType]?.name || item.SceneType),
            width: 100
        },
        {
            id: "description",
            header: "场景描述",
            cell: item => apiClient.formatSceneDescription(item.scene_description, 60),
            width: 300
        },
        {
            id: "uuid",
            header: "UUID",
            cell: item => React.createElement(Box, { 
                fontSize: "body-s",
                color: "text-status-info"
            }, item.uuid?.substring(0, 8) + '...'),
            width: 100
        },
        {
            id: "updateTime",
            header: "更新时间",
            cell: item => apiClient.formatTime(item.update_time),
            width: 120
        },
        {
            id: "videoStatus",
            header: "视频状态",
            cell: item => item.video_link ? 
                React.createElement(StatusIndicator, { type: "success" }, "已生成") :
                React.createElement(StatusIndicator, { type: "pending" }, "未生成"),
            width: 100
        },
        {
            id: "actions",
            header: "操作",
            cell: item => React.createElement(SpaceBetween, { 
                direction: "horizontal", 
                size: "xs" 
            },
                React.createElement(Button, {
                    variant: "inline-link",
                    onClick: () => setSelectedScene(item)
                }, "查看"),
                React.createElement(Button, {
                    variant: "inline-link",
                    onClick: () => {
                        setSceneToDelete(item);
                        setShowDeleteModal(true);
                    }
                }, "删除")
            ),
            width: 120
        }
    ];

    // 渲染多视角内容
    const renderMultiViewContent = (scene) => {
        const tabs = CONFIG.MULTIVIEW_ANGLES.map(angle => ({
            label: angle.name,
            id: angle.key,
            content: React.createElement(FormField, {
                label: angle.key
            },
                React.createElement(Textarea, {
                    value: scene[angle.key] || '',
                    readOnly: true,
                    rows: 6
                })
            )
        }));

        return React.createElement(Tabs, { tabs });
    };

    return React.createElement(Container, {
        header: React.createElement(Header, {
            variant: "h2",
            description: "管理已生成的场景描述",
            actions: React.createElement(Button, {
                onClick: loadScenes,
                loading: loading
            }, "刷新列表")
        }, "场景库管理")
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
                // 左侧场景列表
                React.createElement(Table, {
                    columnDefinitions,
                    items: scenes,
                    loading: loading,
                    loadingText: "加载场景列表中...",
                    empty: React.createElement(Box, {
                        textAlign: "center",
                        color: "inherit"
                    },
                        React.createElement("b", null, "暂无场景数据"),
                        React.createElement(Box, {
                            variant: "p",
                            color: "inherit"
                        }, "请先生成场景描述")
                    ),
                    header: React.createElement(Header, {
                        counter: `(${scenes.length})`
                    }, "场景列表")
                }),

                // 右侧场景详情
                React.createElement(Container, {
                    header: React.createElement(Header, { variant: "h3" }, "场景详情")
                },
                    selectedScene ? React.createElement(SpaceBetween, { 
                        direction: "vertical", 
                        size: "m" 
                    },
                        // 基本信息
                        React.createElement(SpaceBetween, { direction: "vertical", size: "s" },
                            React.createElement(Box, null,
                                React.createElement("strong", null, "UUID: "),
                                selectedScene.uuid
                            ),
                            React.createElement(Box, null,
                                React.createElement("strong", null, "类型: "),
                                CONFIG.SCENE_TYPES[selectedScene.SceneType]?.name || selectedScene.SceneType
                            ),
                            React.createElement(Box, null,
                                React.createElement("strong", null, "更新时间: "),
                                apiClient.formatTime(selectedScene.update_time)
                            )
                        ),

                        // 原始描述
                        React.createElement(FormField, {
                            label: "原始场景描述"
                        },
                            React.createElement(Textarea, {
                                value: selectedScene.scene_description || '',
                                readOnly: true,
                                rows: 3
                            })
                        ),

                        // 增强后的描述
                        selectedScene.SceneType === 'SingleView' ? 
                            React.createElement(FormField, {
                                label: "前方视角描述"
                            },
                                React.createElement(Textarea, {
                                    value: selectedScene.PROMPT_FRONT || '',
                                    readOnly: true,
                                    rows: 6
                                })
                            ) :
                            React.createElement(Box, null,
                                React.createElement(Box, { variant: "h4" }, "多视角描述"),
                                renderMultiViewContent(selectedScene)
                            ),

                        // 视频信息
                        selectedScene.video_link && React.createElement(SpaceBetween, { 
                            direction: "vertical", 
                            size: "s" 
                        },
                            React.createElement(Box, { variant: "h4" }, "视频信息"),
                            React.createElement(StatusIndicator, { type: "success" }, "视频已生成完成"),
                            React.createElement(Link, {
                                href: selectedScene.video_link.startsWith('http') ? 
                                    selectedScene.video_link : 
                                    `https://${selectedScene.video_link}`,
                                external: true
                            }, "查看/下载视频")
                        ),

                        // 操作按钮
                        React.createElement(Button, {
                            variant: "normal",
                            onClick: () => {
                                setSceneToDelete(selectedScene);
                                setShowDeleteModal(true);
                            }
                        }, "删除场景")
                    ) : React.createElement(Box, {
                        textAlign: "center",
                        color: "text-status-inactive"
                    }, "请从左侧选择场景查看详情")
                )
            ),

            // 删除确认对话框
            React.createElement(Modal, {
                visible: showDeleteModal,
                onDismiss: () => setShowDeleteModal(false),
                header: "确认删除",
                footer: React.createElement(Box, { float: "right" },
                    React.createElement(SpaceBetween, { 
                        direction: "horizontal", 
                        size: "xs" 
                    },
                        React.createElement(Button, {
                            variant: "link",
                            onClick: () => setShowDeleteModal(false)
                        }, "取消"),
                        React.createElement(Button, {
                            variant: "primary",
                            onClick: handleDeleteScene
                        }, "确认删除")
                    )
                )
            },
                sceneToDelete && React.createElement(SpaceBetween, { 
                    direction: "vertical", 
                    size: "m" 
                },
                    React.createElement(Box, null, "确定要删除这个场景吗？此操作无法撤销！"),
                    React.createElement(Box, null,
                        React.createElement("strong", null, "场景类型: "),
                        CONFIG.SCENE_TYPES[sceneToDelete.SceneType]?.name || sceneToDelete.SceneType
                    ),
                    React.createElement(Box, null,
                        React.createElement("strong", null, "场景描述: "),
                        apiClient.formatSceneDescription(sceneToDelete.scene_description, 100)
                    )
                )
            )
        )
    );
}

window.SceneManagement = SceneManagement;
