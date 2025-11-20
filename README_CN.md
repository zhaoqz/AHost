# AI-App Host Platform 使用手册

## 1. 简介
这是一个轻量级的 Web 平台，用于托管和展示 AI 生成的 HTML 页面。支持 Zip 和 HTML 文件上传，自动生成展示页和二维码。

## 2. 快速开始 (Quick Start)

### 环境要求
- Python 3.12+
- `uv` 包管理器

### 安装与启动
1. **初始化依赖**:
   ```bash
   uv sync
   ```

2. **启动服务**:
   ```bash
   uv run main.py
   ```
   服务默认运行在 `http://127.0.0.1:8000`。

## 3. 使用指南 (User Guide)

### 上传应用
1. 访问首页 `http://127.0.0.1:8000`。
2. 填写 **App Name** (应用名称)。
3. 填写 **Author** (作者) 和 **Password** (上传密码，默认 `admin`)。
4. (可选) 填写 **Description** (描述) 和 **Custom Slug** (自定义路径)。
5. 上传 `.zip` 或 `.html` 文件。
   - **Zip 文件**: 建议包含 `index.html`。系统会自动解压并寻找入口。
   - **Html 文件**: 系统会自动将其重命名为 `index.html`。
6. 点击 **Deploy App**。
   - **版本更新**: 如果 Slug 已存在，系统会自动覆盖并备份旧版本。

### 查看展示页
上传成功后，会自动跳转到展示页 `/i/{slug}`。
- **展示卡片**: 显示应用名称、作者、描述、创建时间。
- **二维码**: 扫描即可在手机上访问应用。
- **Launch App**: 点击按钮直接打开应用交互页面。

### 访问应用
直接访问 `http://127.0.0.1:8000/{slug}` 即可使用应用。

## 4. 维护与配置 (Maintenance)

### 配置文件
修改 `config.json` 可调整系统配置：
```json
{
    "BASE_URL": "http://127.0.0.1:8000",  // 部署域名/IP
    "UPLOAD_DIR": "data/sites",           // 站点存储目录
    "DB_PATH": "data/db/app.db",          // 数据库路径
    "LOG_LEVEL": "INFO",                  // 日志级别
    "UPLOAD_PASSWORD": "admin"            // 上传密码
}
```

### 数据管理
- **站点文件**: 存储在 `data/sites/` 目录下。
- **数据库**: SQLite 文件位于 `data/db/app.db`。
- **日志**: 运行日志位于 `logs/app.log`。

### 常见问题
- **依赖安装失败**: 确保使用 `uv` 并正确引用带括号的包名，如 `uv add "qrcode[pil]"`。
- **端口冲突**: 在 `main.py` 中修改 `port=8000` 为其他端口。
