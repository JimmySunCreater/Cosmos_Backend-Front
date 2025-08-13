# Cosmos Service 安装总结

## 安装完成状态 ✅

### 已安装的服务

1. **Cosmos API 服务**
   - 端口: 8080
   - 访问地址: http://localhost:8080
   - 健康检查: http://localhost:8080/health
   - 服务名: cosmos-api.service

2. **Streamlit Web UI**
   - 端口: 8501
   - 访问地址: http://localhost:8501
   - 服务名: cosmos-streamlit.service

### 自动启动配置

两个服务都已配置为系统启动时自动启动：
- `sudo systemctl enable cosmos-api.service` ✅
- `sudo systemctl enable cosmos-streamlit.service` ✅

### 服务管理

#### 使用管理脚本 (推荐)
```bash
cd /home/ubuntu/cosmos_service
./manage_services.sh {start|stop|restart|status|logs}
```

#### 使用 systemctl 命令
```bash
# 启动服务
sudo systemctl start cosmos-api.service
sudo systemctl start cosmos-streamlit.service

# 停止服务
sudo systemctl stop cosmos-api.service
sudo systemctl stop cosmos-streamlit.service

# 重启服务
sudo systemctl restart cosmos-api.service
sudo systemctl restart cosmos-streamlit.service

# 查看状态
sudo systemctl status cosmos-api.service
sudo systemctl status cosmos-streamlit.service

# 查看日志
sudo journalctl -u cosmos-api.service -f
sudo journalctl -u cosmos-streamlit.service -f
```

### 文件位置

- **主目录**: `/home/ubuntu/cosmos_service/`
- **API 服务**: `/home/ubuntu/cosmos_service/cosmos_api_service_simple.py`
- **Streamlit 应用**: `/home/ubuntu/cosmos_service/streamlit/streamlit_app.py`
- **服务配置文件**: 
  - `/etc/systemd/system/cosmos-api.service`
  - `/etc/systemd/system/cosmos-streamlit.service`
- **管理脚本**: `/home/ubuntu/cosmos_service/manage_services.sh`

### 依赖包

#### API 服务依赖
- Flask==2.3.3
- boto3==1.34.0
- botocore==1.34.0
- requests==2.31.0
- python-dateutil==2.8.2

#### Streamlit 依赖
- streamlit>=1.28.0
- requests>=2.31.0
- pandas>=2.0.0
- uuid

### 环境变量

#### API 服务环境变量
- `API_HOST=0.0.0.0`
- `API_PORT=8080`
- `AWS_DEFAULT_REGION=us-west-2`
- `NUM_GPUS=8`
- `NPROC_PER_NODE=8`

#### Streamlit 环境变量
- `STREAMLIT_SERVER_PORT=8501`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`

### 测试验证

1. **API 服务测试**:
   ```bash
   curl http://localhost:8080/health
   ```

2. **Streamlit 测试**:
   在浏览器中访问 `http://localhost:8501`

3. **服务状态检查**:
   ```bash
   ./manage_services.sh status
   ```

### 故障排除

1. **查看服务日志**:
   ```bash
   ./manage_services.sh logs
   ```

2. **检查端口占用**:
   ```bash
   ss -tlnp | grep -E ':(8080|8501)'
   ```

3. **重启服务**:
   ```bash
   ./manage_services.sh restart
   ```

### 安全注意事项

- 服务监听在 0.0.0.0，确保防火墙配置正确
- 建议在生产环境中使用反向代理 (如 nginx)
- 定期检查和更新依赖包

---

**安装时间**: 2025-06-16 04:52 UTC
**安装状态**: ✅ 成功
**服务状态**: ✅ 运行中
