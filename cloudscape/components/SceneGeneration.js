// 场景生成组件
function SceneGeneration({ onSceneGenerated }) {
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
        Textarea, 
        Select, 
        Button, 
        Alert, 
        Box,
        Checkbox,
        ExpandableSection,
        StatusIndicator
    } = CloudscapeDesignSystem;

function SceneGeneration({ onSceneGenerated }) {
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
        Textarea, 
        Select, 
        Button, 
        Alert, 
        Box,
        Checkbox,
        ExpandableSection,
        StatusIndicator
    } = CloudscapeDesignSystem;

    const [sceneDescription, setSceneDescription] = useState('');
    const [sceneType, setSceneType] = useState({ value: 'SingleView', label: '单视角' });
    const [useStreaming, setUseStreaming] = useState(false);
    const [isGenerating, setIsGenerating] = useState(false);
    const [generatedResult, setGeneratedResult] = useState(null);
    const [streamingContent, setStreamingContent] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const sceneTypeOptions = [
        { value: 'SingleView', label: '单视角' },
        { value: 'MultiView', label: '多视角' }
    ];

    const handleGenerate = async () => {
        if (!sceneDescription.trim()) {
            setError('请输入场景描述');
            return;
        }

        setIsGenerating(true);
        setError(null);
        setSuccess(null);
        setGeneratedResult(null);
        setStreamingContent('');

        try {
            if (useStreaming) {
                // 使用流式生成
                await apiClient.enhanceSceneStreaming(
                    sceneDescription.trim(),
                    sceneType.value,
                    (content) => {
                        // 进度回调
                        setStreamingContent(prev => prev + content);
                    },
                    (result) => {
                        // 完成回调
                        setGeneratedResult(result);
                        setSuccess('场景描述生成成功！');
                        setIsGenerating(false);
                        onSceneGenerated && onSceneGenerated();
                    },
                    (error) => {
                        // 错误回调
                        setError(error.message);
                        setIsGenerating(false);
                    }
                );
            } else {
                // 使用传统生成
                const result = await apiClient.enhanceScene(
                    sceneDescription.trim(),
                    sceneType.value
                );
                setGeneratedResult(result);
                setSuccess('场景描述生成成功！');
                onSceneGenerated && onSceneGenerated();
            }
        } catch (error) {
            setError(error.message);
        } finally {
            if (!useStreaming) {
                setIsGenerating(false);
            }
        }
    };

    return React.createElement(Container, {
        header: React.createElement(Header, {
            variant: "h2",
            description: "输入简短场景描述，AI将生成详细的场景描述"
        }, "场景描述生成")
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
                // 左侧输入区域
                React.createElement(SpaceBetween, { direction: "vertical", size: "m" },
                    React.createElement(FormField, {
                        label: "场景描述",
                        description: "请输入简短的场景描述，例如：雨后晚上的城市道路"
                    },
                        React.createElement(Textarea, {
                            value: sceneDescription,
                            onChange: (event) => setSceneDescription(event.detail.value),
                            placeholder: "例如：雨后晚上的城市道路",
                            rows: 4
                        })
                    ),

                    React.createElement(FormField, {
                        label: "场景类型"
                    },
                        React.createElement(Select, {
                            selectedOption: sceneType,
                            onChange: (event) => setSceneType(event.detail.selectedOption),
                            options: sceneTypeOptions,
                            placeholder: "选择场景类型"
                        })
                    ),

                    React.createElement(Checkbox, {
                        checked: useStreaming,
                        onChange: (event) => setUseStreaming(event.detail.checked),
                        description: "实时显示生成过程，可以看到内容逐步生成"
                    }, "启用流式生成"),

                    React.createElement(Button, {
                        variant: "primary",
                        onClick: handleGenerate,
                        loading: isGenerating,
                        disabled: !sceneDescription.trim()
                    }, "生成增强场景描述")
                ),

                // 右侧说明区域
                React.createElement(SpaceBetween, { direction: "vertical", size: "m" },
                    React.createElement(Box, { variant: "h3" }, "使用说明"),
                    
                    React.createElement(ExpandableSection, {
                        headerText: "场景类型说明",
                        defaultExpanded: true
                    },
                        React.createElement(SpaceBetween, { direction: "vertical", size: "s" },
                            React.createElement(Box, null,
                                React.createElement("strong", null, "SingleView (单视角)"),
                                React.createElement("ul", null,
                                    React.createElement("li", null, "单一视角场景"),
                                    React.createElement("li", null, "生成前方视角描述"),
                                    React.createElement("li", null, "适合简单场景"),
                                    React.createElement("li", null, "预计生成时间：约1小时")
                                )
                            ),
                            React.createElement(Box, null,
                                React.createElement("strong", null, "MultiView (多视角)"),
                                React.createElement("ul", null,
                                    React.createElement("li", null, "多视角场景"),
                                    React.createElement("li", null, "生成6个视角描述"),
                                    React.createElement("li", null, "适合复杂场景"),
                                    React.createElement("li", null, "预计生成时间：约2小时")
                                )
                            )
                        )
                    ),

                    React.createElement(ExpandableSection, {
                        headerText: "生成模式说明"
                    },
                        React.createElement(SpaceBetween, { direction: "vertical", size: "s" },
                            React.createElement(Box, null,
                                React.createElement("strong", null, "流式生成"),
                                React.createElement("ul", null,
                                    React.createElement("li", null, "实时显示生成过程"),
                                    React.createElement("li", null, "可以看到内容逐步生成"),
                                    React.createElement("li", null, "支持进度显示"),
                                    React.createElement("li", null, "使用WebSocket连接")
                                )
                            ),
                            React.createElement(Box, null,
                                React.createElement("strong", null, "传统生成"),
                                React.createElement("ul", null,
                                    React.createElement("li", null, "等待完成后显示结果"),
                                    React.createElement("li", null, "使用REST API"),
                                    React.createElement("li", null, "生成完成后一次性显示"),
                                    React.createElement("li", null, "稳定可靠")
                                )
                            )
                        )
                    ),

                    React.createElement(Box, { variant: "p" },
                        React.createElement("strong", null, "注意事项："),
                        React.createElement("ul", null,
                            React.createElement("li", null, "描述尽量具体清晰"),
                            React.createElement("li", null, "生成后自动保存到场景库")
                        )
                    )
                )
            ),

            // 生成结果显示区域
            (isGenerating || generatedResult || streamingContent) && React.createElement(
                ExpandableSection, {
                    headerText: "生成结果",
                    defaultExpanded: true
                },
                React.createElement(SpaceBetween, { direction: "vertical", size: "m" },
                    // 显示生成状态
                    isGenerating && React.createElement(Box, null,
                        React.createElement(StatusIndicator, { type: "loading" }, "正在生成场景描述...")
                    ),

                    // 显示UUID
                    generatedResult && React.createElement(Alert, {
                        type: "info"
                    }, `场景UUID: ${generatedResult.uuid}`),

                    // 显示流式内容或最终结果
                    (streamingContent || generatedResult) && React.createElement(FormField, {
                        label: "增强后的场景描述"
                    },
                        React.createElement(Textarea, {
                            value: streamingContent || (generatedResult ? generatedResult.description : ''),
                            readOnly: true,
                            rows: 10
                        })
                    )
                )
            )
        )
    );
}

window.SceneGeneration = SceneGeneration;
