# EC2公网IP自动配置功能

## 🌟 功能概述

该功能自动获取EC2实例 `i-0bbe2d67c7493574f` 的公网IP地址，并自动更新Streamlit配置文件中的API URL，无需手动维护IP地址。

## 📋 配置的URL

- **COSMOS_API_URL**: Cosmos视频生成API服务地址
- **COSMOS_LOG_URL**: Cosmos日志服务地址

两个URL都会自动使用EC2实例的当前公网IP地址。

## 🛠️ 工具脚本

### 1. get_ec2_ip.py
获取EC2实例信息和公网IP地址

```bash
# 查看实例信息
python3 utilities/get_ec2_ip.py --instance-id i-0bbe2d67c7493574f --region us-west-2

# 更新配置文件
python3 utilities/get_ec2_ip.py --instance-id i-0bbe2d67c7493574f --region us-west-2 --update-config

# JSON格式输出
python3 utilities/get_ec2_ip.py --instance-id i-0bbe2d67c7493574f --region us-west-2 --json
```

### 2. manage_ec2_ip.sh
综合管理脚本

```bash
# 检查EC2实例信息
./utilities/manage_ec2_ip.sh check

# 更新配置文件
./utilities/manage_ec2_ip.sh update

# 查看当前状态
./utilities/manage_ec2_ip.sh status

# 设置定时任务
./utilities/manage_ec2_ip.sh cron

# 查看更新日志
./utilities/manage_ec2_ip.sh logs
```

### 3. validate_deployment.sh
部署验证脚本

```bash
# 验证所有配置是否正确
./utilities/validate_deployment.sh
```

### 4. test_config.py
配置测试脚本

```bash
# 测试配置文件和API连接
python3 utilities/test_config.py
```

## ⚙️ 自动化配置

### 启动时自动更新
Streamlit启动脚本已配置为启动时自动更新IP地址：

```bash
./start_web_ui.sh
```

### 定时自动更新
设置定时任务，每30分钟自动检查和更新IP地址：

```bash
./utilities/manage_ec2_ip.sh cron
```

## 📊 配置文件结构

```python
# EC2实例配置
EC2_INSTANCE_ID = "i-0bbe2d67c7493574f"
EC2_REGION = "us-west-2"

# 自动获取公网IP
EC2_PUBLIC_IP = get_ec2_public_ip(EC2_INSTANCE_ID, EC2_REGION)

# API配置（自动使用获取的IP）
COSMOS_API_URL = f"http://{EC2_PUBLIC_IP}:8080"
COSMOS_LOG_URL = f"http://{EC2_PUBLIC_IP}:8080"
```

## 🔧 故障排除

### 1. IP获取失败
```bash
# 检查AWS凭证
aws sts get-caller-identity

# 检查EC2权限
aws ec2 describe-instances --instance-ids i-0bbe2d67c7493574f --region us-west-2
```

### 2. 配置更新失败
```bash
# 手动更新配置
./utilities/manage_ec2_ip.sh update

# 检查配置文件权限
ls -la streamlit/config_streamlit.py
```

### 3. API连接失败
```bash
# 测试API连接
python3 utilities/test_config.py

# 检查服务状态
curl http://$(python3 -c "import sys; sys.path.append('streamlit'); from config_streamlit import EC2_PUBLIC_IP; print(EC2_PUBLIC_IP)"):8080/health
```

## 📝 日志文件

- **IP更新日志**: `/home/ubuntu/cosmos_service/logs/ip_update.log`
- **应用日志**: `/home/ubuntu/cosmos_service/cosmos_api.log`

## 🚀 快速开始

1. **验证部署**:
   ```bash
   ./utilities/validate_deployment.sh
   ```

2. **设置定时任务**:
   ```bash
   ./utilities/manage_ec2_ip.sh cron
   ```

3. **启动服务**:
   ```bash
   ./start_web_ui.sh
   ```

4. **检查状态**:
   ```bash
   ./utilities/manage_ec2_ip.sh status
   ```

## 🔒 安全注意事项

1. 确保EC2实例有适当的IAM权限访问EC2 API
2. 定期检查日志文件，监控IP更新情况
3. 如果IP频繁变化，考虑使用Elastic IP

## 📞 支持

如遇问题，请：
1. 运行验证脚本检查配置
2. 查看日志文件了解详细错误
3. 检查AWS权限和网络连接
