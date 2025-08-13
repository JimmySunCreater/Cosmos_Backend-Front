# CloudScape界面部署说明

## 🚀 快速部署

### 1. 启动服务
```bash
cd /home/ubuntu/cosmos_service/cloudscape
./start_server.sh
```

### 2. 访问界面
- 本地访问: http://localhost:5001
- 网络访问: http://YOUR_SERVER_IP:5001

## 🔧 配置说明

### API配置
编辑 `config.js` 文件中的配置项：

```javascript
const CONFIG = {
    // 场景增强API
    ENHANCE_API_URL: "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/enhence",
    
    // WebSocket流式API
    WEBSOCKET_ENHANCE_URL: "wss://qopfrzscp0.execute-api.us-west-2.amazonaws.com/prod",
    
    // 场景库API
    LIBRARY_API_URL: "https://olg7i626u1.execute-api.us-west-2.amazonaws.com/prod/library",
    
    // Cosmos服务器配置（会自动检测）
    COSMOS_PRIVATE_IP: "172.31.8.172",
    COSMOS_PUBLIC_IP: null,
    
    // API密钥
    API_KEY: "C2G4GCEdCP2KMKYKZlpxgaX28k2ud4sxY4gEa3Zh"
};
```

### 端口配置
默认端口: 5001
如需修改，编辑 `start_server.sh` 中的 `PORT` 变量。

## 🌐 生产环境部署

### 使用Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /home/ubuntu/cosmos_service/cloudscape;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    # API代理（可选）
    location /api/ {
        proxy_pass http://172.31.8.172:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 使用Apache
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /home/ubuntu/cosmos_service/cloudscape
    
    <Directory /home/ubuntu/cosmos_service/cloudscape>
        AllowOverride All
        Require all granted
    </Directory>
    
    # SPA路由支持
    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</VirtualHost>
```

### 使用PM2（Node.js进程管理）
```bash
# 安装PM2
npm install -g pm2

# 创建PM2配置文件
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'cosmos-cloudscape',
    script: 'python3',
    args: '-m http.server 5001',
    cwd: '/home/ubuntu/cosmos_service/cloudscape',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
EOF

# 启动服务
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 🔒 安全配置

### HTTPS配置
```bash
# 使用Let's Encrypt获取SSL证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 防火墙配置
```bash
# 开放端口
sudo ufw allow 5001/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### API密钥安全
生产环境建议：
1. 使用环境变量存储API密钥
2. 实现API密钥轮换机制
3. 限制API访问来源

## 📊 监控和日志

### 访问日志
```bash
# 查看Python HTTP服务器日志
tail -f /var/log/cosmos-cloudscape.log
```

### 性能监控
```bash
# 监控服务状态
ps aux | grep "python3.*http.server"

# 监控端口使用
netstat -tlnp | grep :5001
```

### 健康检查
```bash
# 创建健康检查脚本
cat > health_check.sh << 'EOF'
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001)
if [ $response -eq 200 ]; then
    echo "Service is healthy"
    exit 0
else
    echo "Service is unhealthy (HTTP $response)"
    exit 1
fi
EOF

chmod +x health_check.sh
```

## 🔄 更新和维护

### 更新代码
```bash
cd /home/ubuntu/cosmos_service/cloudscape
# 备份当前版本
cp -r . ../cloudscape_backup_$(date +%Y%m%d_%H%M%S)

# 更新代码文件
# ... 更新操作 ...

# 重启服务
pkill -f "python3.*http.server.*5001"
./start_server.sh
```

### 清理缓存
```bash
# 清理浏览器缓存（在浏览器中）
# Ctrl+Shift+R 或 Cmd+Shift+R

# 清理服务器缓存
sudo systemctl restart nginx  # 如果使用Nginx
```

## 🐛 故障排除

### 常见问题

1. **端口被占用**
```bash
# 查找占用进程
lsof -i :5001
# 终止进程
kill -9 PID
```

2. **API连接失败**
```bash
# 检查Cosmos服务状态
curl http://172.31.8.172:8080/health
# 检查网络连接
ping 172.31.8.172
```

3. **静态文件404**
```bash
# 检查文件权限
ls -la /home/ubuntu/cosmos_service/cloudscape/
# 修复权限
chmod -R 644 /home/ubuntu/cosmos_service/cloudscape/
chmod +x /home/ubuntu/cosmos_service/cloudscape/start_server.sh
```

4. **JavaScript错误**
- 打开浏览器开发者工具
- 查看Console标签页的错误信息
- 检查Network标签页的请求状态

### 日志分析
```bash
# 查看系统日志
journalctl -u cosmos-cloudscape -f

# 查看访问日志
tail -f /var/log/nginx/access.log

# 查看错误日志
tail -f /var/log/nginx/error.log
```

## 📈 性能优化

### 静态资源优化
1. 启用Gzip压缩
2. 设置缓存头
3. 使用CDN加速

### 代码优化
1. 压缩JavaScript和CSS
2. 优化图片资源
3. 减少HTTP请求数量

### 服务器优化
1. 调整服务器配置
2. 使用负载均衡
3. 监控资源使用情况

## 🔧 开发环境

### 本地开发
```bash
# 启动开发服务器
cd /home/ubuntu/cosmos_service/cloudscape
python3 -m http.server 5001

# 或使用Node.js服务器（如果安装了Node.js）
npx http-server -p 5001 -c-1
```

### 代码热重载
使用支持热重载的开发服务器：
```bash
# 使用live-server（需要Node.js）
npm install -g live-server
live-server --port=5001 --no-browser
```
