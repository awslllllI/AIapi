# 服务雏形架构（LiteLLM Proxy）

## 为何用现有框架

| 候选 | 结论 |
| --- | --- |
| **LiteLLM Proxy**（采用） | MIT；OpenAI 兼容出口；原生 fallback / 重试；`config.yaml` 即可接 Groq、Gemini、自定义 OpenAI 兼容上游（智谱/硅基/魔搭）；适合给 Agent 当统一 base_url |
| New API | 渠道/令牌面板更强，但 AGPL；本期先不做分发计费 |
| One API | 维护偏慢；能力被 New API / LiteLLM 覆盖 |
| 自研网关 | 后期再加「日配额记账 / 智能选路」插件；雏形不重复造轮子 |

本期范围：**不接 Web2API**；只接「周期性免费额度 + 常驻免费模型」官方 API。

## 逻辑视图

```text
Agent / Cursor / 任意 OpenAI SDK
        │  base_url = http://localhost:4000/v1
        │  Authorization: Bearer <LITELLM_MASTER_KEY>
        ▼
┌───────────────────────────────────────┐
│  LiteLLM Proxy                         │
│  逻辑模型: auto / fast / reason / cn   │
│  fallback + num_retries                │
└───────────────┬───────────────────────┘
                │
    ┌───────────┼───────────┬────────────┐
    ▼           ▼           ▼            ▼
 智谱Flash   硅基免费     Groq        Gemini Free
 (可选)     ModelScope   OpenRouter:free   CF Workers AI
```

## 目录

```text
ai-api/
  docker-compose.yml      # 仅 LiteLLM（雏形不加 Postgres/Prometheus）
  litellm/config.yaml     # 模型组 + fallback
  .env.example
  docs/
    periodic-free-apis.md
    architecture.md
    research-free-ai-aggregation.md
```

## 后续可演进（未做）

1. Redis 令牌桶：按提供商 RPD/TPD/Neurons 记账，配额将尽时提前切上游。  
2. 健康探测 worker：定时最小 prompt，摘除坏渠道。  
3. 需要团队令牌分发时再评估 New API 作管理面。  
4. Postgres + LiteLLM UI（虚拟 Key / 用量看板）。
