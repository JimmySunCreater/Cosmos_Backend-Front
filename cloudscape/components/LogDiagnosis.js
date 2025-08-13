// 日志诊断组件
function LogDiagnosis() {
    // 确保React和CloudScape已加载
    if (typeof React === 'undefined' || typeof CloudscapeDesignSystem === 'undefined') {
        return null;
    }
    
    const { useState, useEffect } = React;
    const { 
        Container, 
        Header, 
        SpaceBetween, 
        Button, 
        Alert, 
        Box,
        Link
    } = CloudscapeDesignSystem;

function LogDiagnosis() {
    const [error, setError] = useState(null);
    const [iframeHeight, setIframeHeight] = useState(800);

    // 计算iframe高度
    const calculateIframeHeight = () => {
        const screenWidth = window.screen.width;
        const screenHeight = window.screen.height;
        let height;
        
        if (screenWidth >= 3840 || screenHeight >= 2160) {
            // 4K屏幕
            height = Math.max(screenHeight - 200, 1800);
        } else if (screenWidth >= 2560) {
            // 2K屏幕
            height = Math.max(screenHeight - 160, 1200);
        } else if (screenWidth >= 1920) {
            // Full HD屏幕
            height = Math.max(screenHeight - 140, 900);
        } else if (screenWidth >= 1200) {
            // 标准大屏幕
            height = Math.max(screenHeight - 120, 700);
        } else if (screenWidth >= 768) {
            // 中等屏幕
            height = Math.max(screenHeight - 100, 500);
        } else if (screenWidth >= 576) {
            // 小屏幕
            height = Math.max(screenHeight - 80, 400);
        } else {
            // 超小屏幕
            height = Math.max(screenHeight - 60, 300);
        }
        
        return height;
    };

    // 初始化和窗口大小变化时更新高度
    useEffect(() => {
        const updateHeight = () => {
            setIframeHeight(calculateIframeHeight());
        };

        updateHeight();
        window.addEventListener('resize', updateHeight);
        
        return () => {
            window.removeEventListener('resize', updateHeight);
        };
    }, []);

    // 处理iframe加载错误
    const handleIframeError = () => {
        setError('无法加载日志页面，请检查服务是否正常运行');
    };

    // 刷新iframe
    const refreshIframe = () => {
        const iframe = document.getElementById('log-iframe');
        if (iframe) {
            iframe.src = iframe.src;
        }
        setError(null);
    };

    const logUrl = `${CONFIG.COSMOS_LOG_URL}/logs`;

    return React.createElement(Container, {
        header: React.createElement(Header, {
            variant: "h2",
            description: "实时查看系统日志和运行状态",
            actions: React.createElement(SpaceBetween, { 
                direction: "horizontal", 
                size: "xs" 
            },
                React.createElement(Button, {
                    onClick: refreshIframe
                }, "刷新日志"),
                React.createElement(Link, {
                    href: logUrl,
                    external: true
                }, "在新窗口打开")
            )
        }, "日志诊断")
    }, 
        React.createElement(SpaceBetween, { direction: "vertical", size: "m" },
            // 错误提示
            error && React.createElement(Alert, {
                type: "error",
                dismissible: true,
                onDismiss: () => setError(null),
                action: React.createElement(Button, {
                    onClick: () => window.open(logUrl, '_blank')
                }, "直接访问")
            }, error),

            // 日志iframe容器
            React.createElement(Box, {
                padding: "n"
            },
                React.createElement("div", {
                    style: {
                        width: '100%',
                        height: `${iframeHeight}px`,
                        border: '1px solid #e1e4e8',
                        borderRadius: '8px',
                        overflow: 'hidden',
                        backgroundColor: '#ffffff'
                    }
                },
                    React.createElement("iframe", {
                        id: "log-iframe",
                        src: logUrl,
                        style: {
                            width: '100%',
                            height: '100%',
                            border: 'none'
                        },
                        onError: handleIframeError,
                        title: "系统日志"
                    })
                )
            ),

            // 使用说明
            React.createElement(Alert, {
                type: "info"
            },
                React.createElement(SpaceBetween, { direction: "vertical", size: "s" },
                    React.createElement(Box, { variant: "h4" }, "日志诊断功能："),
                    React.createElement(Box, null,
                        React.createElement("ul", null,
                            React.createElement("li", null, "实时查看系统运行日志"),
                            React.createElement("li", null, "监控API请求和响应"),
                            React.createElement("li", null, "诊断系统错误和异常"),
                            React.createElement("li", null, "查看GPU使用情况"),
                            React.createElement("li", null, "监控任务队列状态")
                        )
                    ),
                    React.createElement(Box, null,
                        React.createElement("strong", null, "提示："),
                        "如果日志页面无法正常显示，请点击"直接访问"按钮在新窗口中打开，或检查Cosmos服务是否正常运行。"
                    )
                )
            )
        )
    );
}

window.LogDiagnosis = LogDiagnosis;
