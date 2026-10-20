# Browser UI Provider 快速开始

> 只用于明确允许自动化的站点或你拥有/获授权的测试环境。此功能不会规避验证码、MFA、访问控制、封禁或反自动化限制。

## 1. 安装

在项目根目录运行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r gateway\requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

## 2. 创建站点配置

复制示例配置到本地文件（本地文件已加入 Git 忽略）：

```powershell
Copy-Item gateway\browser-sites.example.json gateway\browser-sites.json
```

编辑 sites 数组，为每个站点配置独立的 id、入口 URL、允许域名、登录状态路径、选择器和速率限制。默认示例是 disabled，且 automation_authorized=false；必须先确认站点允许这种自动化，再显式启用。不要只为了让它运行就随意把授权标记改为 true。

## 3. 手动建立登录状态

当站点确实允许浏览器自动化时，先在配置中设置：

- enabled: true
- automation_authorized: true
- base_url 和 allowed_domains 指向真实授权站点
- auth.storage_state_path 指向本地会话文件

然后运行：

```powershell
.\.venv\Scripts\python.exe gateway\scripts\browser_login.py --site-id YOUR_SITE_ID --config gateway\browser-sites.json
```

脚本会打开可见浏览器。由用户正常完成登录；如出现验证码或 MFA，只能按站点正常流程手动完成。脚本会将授权会话保存到 storage_state_path。会话文件相当于敏感凭证，不要发送给他人，也不要提交 Git。

## 4. 启动 Gateway

配置环境变量：

```powershell
$env:GATEWAY_MASTER_KEY = "your-local-dev-key"
$env:BROWSER_SITES_CONFIG = "gateway/browser-sites.json"
$env:GATEWAY_ROUTE_AUTO = "browser_ui_YOUR_SITE_ID,mock_web"
.\.venv\Scripts\python.exe -m uvicorn gateway.app.main:app --host 127.0.0.1 --port 4010
```

调用时将 model 设为对应的 provider/model ID，例如 browser_ui_YOUR_SITE_ID，并在请求中设置 user 字段作为稳定的会话 ID（同一对话每轮保持一致，不同对话使用不同值）。Browser UI Provider 强制要求该字段，避免不同对话共享页面历史。每个站点的 provider 名和会话文件独立。不要把需要授权的浏览器 Provider 加入公网服务，除非你已实现并审查了额外的账号隔离、租户授权、秘密管理和审计。

## 5. 限制

- Browser UI 当前是普通响应模式；流式接口明确返回不支持，不伪装成原生 SSE。
- 429 遵循站点允许的限速并降低请求频率；403、验证码、访问拒绝或封禁提示应暂停/禁用 Provider，不循环重试。
- 页面结构会变化，选择器需要维护；UI 自动化通常比官方 API 更脆弱。
- 当前真实第三方站点没有经过验证。仓库集成测试只访问本地自建 fixture。
- **Duck.ai**：服务条款禁止 automated querying。即使在 manifest 里写了 `duck_ai`，Provider 也会以 `stage=policy` 拒绝；不要把 `automation_authorized` 改成 true 试图强行接入。管线验证请用 `gateway/fixtures/duck_ui_fixture_server.py`。详见 `docs/diagnostics/duckai-browser-ui-report.md`。
