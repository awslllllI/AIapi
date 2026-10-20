# Provider Demo 验证记录

> 日期：2026-10-19（UTC+8）

## 1. 修改/新增文件清单

| 路径 | 说明 |
| --- | --- |
| `gateway/app/*.py` | Provider 网关：配置、错误、限流、熔断、路由、FastAPI |
| `gateway/app/providers/*.py` | `MockWeb` / `DemoLocalWeb` / `OpenAICompatible` |
| `gateway/fixtures/demo_web_ai_server.py` | 自建允许自动化的 Demo Web AI（:4020） |
| `gateway/tests/*.py` | 单元 + ASGI E2E + Demo fixture 联调 |
| `gateway/requirements.txt` / `pytest.ini` / `scripts/*` | 依赖、测试与验证脚本 |
| `docs/web-provider-candidates.md` | 候选对比表 |
| `docs/provider-demo.md` | 启动与复现步骤 |
| `docs/verification-record.md` | 本文件 |
| `docs/verification-live-record.json` | 现场 chat 摘要 |
| `README.md` / `.env.example` / `litellm/config.yaml` | 文档与可选对接注释 |

未改动既有 LiteLLM 运行时默认行为（仅增加注释掉的可选 model）。

## 2. 候选对比

见 [`web-provider-candidates.md`](./web-provider-candidates.md)。

结论：**第三方 WebChat UI 不可合规程序化接入**；本 Demo 接入 Mock、自建 fixture、以及官方 OpenAI 兼容 API。

## 3. 命令与测试结果

```text
# 2026-10-20：在当前工作树重新验证（使用已有 .venv）
.\.venv\Scripts\python.exe -m pytest gateway\tests -q
→ 18 passed in 7.03s

.\.venv\Scripts\python.exe -m compileall -q gateway
→ exit code 0

git diff --check
→ exit code 0
```

本轮新增回归：流式首包发出后上游失败不得切换备用 Provider；超时与上游 429 应按配置切换到备用 Provider；未配置 `GATEWAY_MASTER_KEY` 时网关必须拒绝请求（fail closed）。此前 `test_gateway_rate_limit` 曾被环境变量覆盖 Settings，改为直接注入 `RateLimiter(1)` 后通过。

## 4. 完整验证链路（客户端 → Provider → 响应）

### 4.1 Demo Web（已验证）

1. 启动 `python -m gateway.fixtures.demo_web_ai_server`（:4020）  
2. 启动 `uvicorn gateway.app.main:app --port 4010`  
3. `POST /v1/chat/completions` model=`auto`，Bearer `sk-gateway-dev`  
4. 结果：

```text
provider=demo_web
content=[DemoLocalWebAI allowed fixture] You said: live-verify-ping
```

摘要文件：`docs/verification-live-record.json`

### 4.2 Mock failover（已验证，pytest）

`FORCE_UPSTREAM_ERROR` → 第一 Provider 失败 → `mock_web_b` 成功。

### 4.3 官方 OpenAI 兼容上游（已验证 / 部分失败有证据）

| 上游 | 结果 | 证据 |
| --- | --- | --- |
| 硅基流动 `Qwen/Qwen3.5-9B` | **成功** | `openai_compat` 返回 content 含 `OK` |
| 智谱 `glm-4.7-flash` | 失败 | HTTP 429「访问量过大」→ 错误类别 `rate_limit` |
| 魔搭 `Qwen/Qwen3.8-27B` | 失败 | `insufficient balance`（状态被归为 rate_limit/可 failover） |

→ **openai_compat Provider 实现可用**；具体上游是否有额度属账户状态，**不是**「接口未接通」。

## 5. 复现 Demo 步骤

见 [`provider-demo.md`](./provider-demo.md)。

最短路径（仅 Mock，无需 :4020）：

```powershell
cd D:\Project\ai-api
.\.venv\Scripts\Activate.ps1
$env:GATEWAY_MASTER_KEY="sk-gateway-dev"
$env:GATEWAY_ENABLE_DEMO_WEB="false"
$env:GATEWAY_ROUTE_AUTO="mock_web"
$env:PYTHONPATH="D:\Project\ai-api"
python -m uvicorn gateway.app.main:app --host 127.0.0.1 --port 4010
# 另开窗口：
curl http://127.0.0.1:4010/v1/chat/completions -H "Authorization: Bearer sk-gateway-dev" -H "Content-Type: application/json" -d "{\"model\":\"auto\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}]}"
```

## 6. 能力边界（勿把未完成说成可用）

| 能力 | 状态 |
| --- | --- |
| Provider 抽象 + 列表/非流式/流式 | **已验证** |
| 超时/限流/上游错误标准化 | **已验证**（Mock 注入 + 网关限流） |
| failover / 熔断 | **已验证**（单测） |
| 自建 Demo Web 接入 | **已验证**（现场 + 单测） |
| OpenAI 兼容真实上游 | **已验证**（硅基成功；智谱/魔搭账户侧失败有证据） |
| 健康快照 + quota=`unknown` | **已验证** |
| 第三方 WebChat2API（ChatGPT/Claude/Duck.ai…） | **因访问规则无法验证 / 不做**（Duck.ai：条款禁 automated querying；只读探针见 `docs/diagnostics/`） |
| LiteLLM docker 内一键转发到 gateway | **尚未验证**（仅配置注释；需 host 网络） |

## 7. 明确不做

- 伪装客户端、绕过登录/验证码、抓隐藏接口、复用未授权会话。  
- 将 Duck.ai 等「免登录网页」当作 API 后端而无官方授权。


## 8. 本轮独立 HTTP 冒烟验证（2026-10-20）

使用临时本地端口（Gateway 4011、fixture 4021）启动两个真实 Uvicorn HTTP 服务，验证后正常关闭；未依赖历史 JSON 摘要：

- `GET /v1/models`：HTTP 200，返回 5 个模型。
- 非流式 `POST /v1/chat/completions`：HTTP 200，`provider=demo_web`，正文为 `[DemoLocalWebAI allowed fixture] You said: http-live-check`。
- 流式 `POST /v1/chat/completions`：HTTP 200，收到 SSE 内容，包含 `stream-live-check`，并以 `[DONE]` 结束。

此验证只证明本地 Gateway 与自建 fixture 的 HTTP 链路，不代表第三方 Web AI 已接入，也不代表 LiteLLM Docker 到 Gateway 的转发已验证。


## 9. LiteLLM Docker → Gateway 联调（隔离测试容器，2026-10-20）

为避免改动正在运行的既有 LiteLLM 容器，本次使用临时配置启动独立 LiteLLM 测试容器（宿主机端口 4001），Gateway 监听宿主机端口 4010；测试配置与容器已在验证后删除/停止。

- Docker 通过 `host.docker.internal:4010/v1` 访问宿主机 Gateway，验证网络可达。
- `GET /health/liveliness`：HTTP 200。
- LiteLLM 转发普通请求：HTTP 200，响应由 `mock_web` Provider 返回，正文含 `litellm-docker-smoke`。
- LiteLLM 转发流式请求：HTTP 200，SSE 正文含 `litellm-docker-stream` 并包含 `[DONE]`。
- 测试后执行 `docker stop ai-api-litellm-smoke` 并移除临时配置文件。

**范围说明：** 这证明 LiteLLM 与 Gateway 的 Docker 网络及普通/流式转发可行；没有修改或重启原有 `ai-api-litellm` 容器，也没有将 `gateway-mock` 默认加入生产配置。正式启用仍需按 `litellm/config.yaml` 中的可选示例配置模型并提供一致的 `GATEWAY_MASTER_KEY`。


## 10. Browser UI Provider 本地浏览器集成验证（2026-10-20）

- 安装：在项目虚拟环境安装 Playwright 1.64.0，并安装 Chromium 156.0.8078.4。
- 测试方式：启动本地自建 HTML fixture 服务，使用真实 Chromium headless 浏览器执行导航、填写输入框、点击发送按钮、读取回答；未访问任何第三方站点。
- 多轮对话：同一个 user/session key 连续发两轮请求，fixture 回答计数从 1 增至 2，证明页面上下文在同一会话中被复用。
- 多站点配置：自动化测试从临时 JSON manifest 加载两个独立站点配置，验证 provider ID 和会话文件路径隔离，且默认禁用。
- 登录辅助脚本：新增 browser_login.py，使用可见浏览器由用户手动登录并保存 storage state；不处理或绕过 CAPTCHA/MFA。
- 最终完整测试：`.venv\\Scripts\\python.exe -m pytest gateway\\tests -q` → 26 passed in 8.94s。
- `python -m compileall -q gateway`：通过；`git diff --check`：通过。

范围限制：这只证明浏览器运行时可在本地 fixture 上执行交互，不代表任何真实第三方 AI 网站允许或已成功接入。真实站点仍需逐站核验授权与条款；Browser UI 暂不支持流式输出。
