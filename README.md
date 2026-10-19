# ai-api — 免费 AI API 聚合雏形

把**周期性免费额度**与**常驻免费模型**官方 API，聚合成一个 OpenAI 兼容入口，供 Agent 使用。  
**不做 Web2API。**

- 额度筛选：[`docs/periodic-free-apis.md`](docs/periodic-free-apis.md)
- 架构说明：[`docs/architecture.md`](docs/architecture.md)
- 完整调研：[`docs/research-free-ai-aggregation.md`](docs/research-free-ai-aggregation.md)

## 框架选型

使用 **[LiteLLM Proxy](https://docs.litellm.ai/docs/simple_proxy)**（MIT）：统一 `/v1/chat/completions`、配置化 fallback，避免自研网关。

## 快速启动

```powershell
cd D:\Project\ai-api
Copy-Item .env.example .env
# 编辑 .env：至少填 LITELLM_MASTER_KEY + 一个上游 Key（建议 ZHIPU 或 GROQ）

docker compose up -d
```

健康检查：`http://localhost:4000/health/liveliness`  
对外 Base URL：`http://localhost:4000/v1`

### 调用示例

```powershell
curl http://localhost:4000/v1/chat/completions `
  -H "Authorization: Bearer $env:LITELLM_MASTER_KEY" `
  -H "Content-Type: application/json" `
  -d '{"model":"auto","messages":[{"role":"user","content":"ping"}]}'
```

| 逻辑模型 | 含义 |
| --- | --- |
| `auto` | 智谱 → 硅基 → Groq → Gemini → 魔搭 → OpenRouter free |
| `cn` | 仅国内常驻免费 |
| `fast` | Groq 日额度优先 |
| `reason` | 智谱 Z1-Flash → Groq OSS-120B |

硅基 / 魔搭上的具体免费模型 ID 以各控制台为准，可在 `litellm/config.yaml` 中改 `model:` 字段。

## Agent 接入

将任意 OpenAI SDK / Cursor 自定义模型的：

- Base URL → `http://localhost:4000/v1`
- API Key → `.env` 里的 `LITELLM_MASTER_KEY`
- Model → `auto`（或 `cn` / `fast` / `reason`）
