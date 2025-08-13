// 主应用组件
function App() {
    // 确保React和CloudScape已加载
    if (typeof React === 'undefined' || typeof CloudscapeDesignSystem === 'undefined') {
        return null;
    }
    
    const { useState, useEffect } = React;
    const { 
        AppLayout, 
        SideNavigation,
        TopNavigation,
        BreadcrumbGroup,
        SpaceBetween,
        Box,
        Alert
    } = CloudscapeDesignSystem;

function App() {
    const [activeHref, setActiveHref] = useState('#/scene-generation');
    const [navigationOpen, setNavigationOpen] = useState(true);
    const [refreshTrigger, setRefreshTrigger] = useState(0);

    // 导航项配置
    const navigationItems = [
        {
            type: "section",
            text: "场景管理",
            items: [
                {
                    type: "link",
                    text: "场景生成",
                    href: "#/scene-generation"
                },
                {
                    type: "link", 
                    text: "场景管理",
                    href: "#/scene-management"
                }
            ]
        },
        {
            type: "section",
            text: "视频处理",
            items: [
                {
                    type: "link",
                    text: "视频生成", 
                    href: "#/video-generation"
                }
            ]
        },
        {
            type: "section",
            text: "系统工具",
            items: [
                {
                    type: "link",
                    text: "日志诊断",
                    href: "#/log-diagnosis"
                }
            ]
        }
    ];

    // 面包屑配置
    const getBreadcrumbs = () => {
        const breadcrumbMap = {
            '#/scene-generation': [
                { text: "首页", href: "#/" },
                { text: "场景生成", href: "#/scene-generation" }
            ],
            '#/scene-management': [
                { text: "首页", href: "#/" },
                { text: "场景管理", href: "#/scene-management" }
            ],
            '#/video-generation': [
                { text: "首页", href: "#/" },
                { text: "视频生成", href: "#/video-generation" }
            ],
            '#/log-diagnosis': [
                { text: "首页", href: "#/" },
                { text: "日志诊断", href: "#/log-diagnosis" }
            ]
        };
        return breadcrumbMap[activeHref] || [{ text: "首页", href: "#/" }];
    };

    // 处理导航变化
    const handleNavigationChange = (event) => {
        const href = event.detail.href;
        setActiveHref(href);
        window.location.hash = href;
    };

    // 处理场景生成成功，触发其他组件刷新
    const handleSceneGenerated = () => {
        setRefreshTrigger(prev => prev + 1);
    };

    // 监听浏览器hash变化
    useEffect(() => {
        const handleHashChange = () => {
            const hash = window.location.hash || '#/scene-generation';
            setActiveHref(hash);
        };

        window.addEventListener('hashchange', handleHashChange);
        handleHashChange(); // 初始化

        return () => {
            window.removeEventListener('hashchange', handleHashChange);
        };
    }, []);

    // 渲染主要内容
    const renderContent = () => {
        switch (activeHref) {
            case '#/scene-generation':
                return React.createElement(window.SceneGeneration, {
                    onSceneGenerated: handleSceneGenerated
                });
            case '#/scene-management':
                return React.createElement(window.SceneManagement, {
                    refreshTrigger: refreshTrigger
                });
            case '#/video-generation':
                return React.createElement(window.VideoGeneration, {
                    refreshTrigger: refreshTrigger
                });
            case '#/log-diagnosis':
                return React.createElement(window.LogDiagnosis);
            default:
                return React.createElement(window.SceneGeneration, {
                    onSceneGenerated: handleSceneGenerated
                });
        }
    };

    return React.createElement(AppLayout, {
        navigation: React.createElement(SideNavigation, {
            activeHref: activeHref,
            header: {
                href: "#/",
                text: "Cosmos系统"
            },
            items: navigationItems,
            onFollow: handleNavigationChange
        }),
        navigationOpen: navigationOpen,
        onNavigationChange: ({ detail }) => setNavigationOpen(detail.open),
        breadcrumbs: React.createElement(BreadcrumbGroup, {
            items: getBreadcrumbs(),
            onFollow: (event) => {
                event.preventDefault();
                const href = event.detail.href;
                setActiveHref(href);
                window.location.hash = href;
            }
        }),
        content: renderContent(),
        toolsHide: true,
        contentType: "default"
    });
}

// 初始化应用
function initializeApp() {
    // 等待所有依赖加载完成
    if (typeof React === 'undefined' || 
        typeof ReactDOM === 'undefined' || 
        typeof CloudscapeDesignSystem === 'undefined') {
        console.log('等待依赖加载...');
        setTimeout(initializeApp, 100);
        return;
    }
    
    console.log('所有依赖已加载，初始化应用...');
    const root = ReactDOM.createRoot(document.getElementById('app'));
    root.render(React.createElement(App));
}

// 等待DOM加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}
