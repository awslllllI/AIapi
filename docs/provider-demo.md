# Provider 网关 Demo 使用说明

本 Demo 扩展现有 LiteLLM 聚合站：新增 **Provider 抽象层**（`gateway/`），用合规方式验证「Web 形态服务 → 统一 OpenAI 接口」；**不做**第三方 WebChat 逆向。

## 组件

| 端口 | 进程 | 作用 |
| --- | --- | --- |
| 4000 | LiteLLM（原有） | 官方 Free API failover |
| 4010 | Provider Gateway | Mock / Demo Web / OpenAI-compat |
| 4020 | Demo Web fixture | 自建、允许自动化的本地 Web AI |

## 启动

```powershell
cd D:\Project\ai-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r gateway\requirements.txt

# 终端 A：自建 Demo Web（可选，测 demo 路由时需要）
python -m gateway.fixtures.demo_web_ai_server

# 终端 B：Provider 网关
$env:GATEWAY_MASTER_KEY = "sk-gateway-dev"
$env:GATEWAY_ENABLE_DEMO_WEB = "true"
$env:GATEWAY_ROUTE_AUTO = "demo_web,mock_web"
python -m uvicorn gateway.app.main:app --host 127.0.0.1 --port 4010
```

可选：把已有官方 Key 接到 `openai_compat`（**不要**写进仓库）：

```powershell
$env:OPENAI_COMPAT_BASE_URL = "https://api-inference.modelscope.cn/v1"
$env:OPENAI_COMPAT_API_KEY = $env:MODELSCOPE_API_KEY   # 从 litellm.env 自行加载
$env:OPENAI_COMPAT_MODEL = "Qwen/Qwen3.8-27B"
$env:GATEWAY_ROUTE_AUTO = "openai_compat,demo_web,mock_web"
```

## 调用

```powershell
curl http://127.0.0.1:4010/v1/chat/completions `
  -H "Authorization: Bearer sk-gateway-dev" `
  -H "Content-Type: application/json" `
  -d '{"model":"auto","messages":[{"role":"user","content":"ping"}]}'
```

预期（无 openai_compat / 仅 mock）：`choices[0].message.content` 含 `[MockWebProvider — NOT a real Web AI]`。  
预期（demo_web 优先且 4020 已起）：含 `[DemoLocalWebAI allowed fixture]`。

流式：

```powershell
curl http://127.0.0.1:4010/v1/chat/completions `
  -H "Authorization: Bearer sk-gateway-dev" `
  -H "Content-Type: application/json" `
  -d '{"model":"mock","stream":true,"messages":[{"role":"user","content":"hi"}]}'
```

健康：`GET http://127.0.0.1:4010/health`（含配额字段，缺官方接口时为 `unknown`）。

## 测试

```powershell
cd D:\Project\ai-api
.\.venv\Scripts\Activate.ps1
pytest gateway\tests -q
```

## 与 LiteLLM 关系

- **不破坏** 现有 `docker compose` / `litellm/config.yaml`。  
- Gateway 是并行扩展；可将 LiteLLM 某一 model 的 `api_base` 指到 `http://host.docker.internal:4010/v1`（需自行配置网络与 `GATEWAY_MASTER_KEY`）。  
- 逻辑模型：`auto` / `mock` / `demo` / `mock-web-echo` / `demo-web-local`。

## 能力边界

| 能力 | 状态 |
| --- | --- |
| Provider 接口 + 路由 failover | **已验证** |
| Mock 普通/流式/限流/上游错误 | **已验证** |
| 自建 Demo Web 接入 | **已验证**（ASGI fixture） |
| OpenAI 兼容真实上游 | **已实现**；需环境 Key 才算「真实可用」 |
| 第三方 WebChat2API | **无法验证 / 不做** |
