# Web AI 候选服务对比（程序化接入视角）

> **核验日期**：2026-10-19  
> **原则**：区分「浏览器可免费用」与「允许作为程序化 API 后端」。  
> 详细额度/封号见 [`research-web-ai-limits.md`](./research-web-ai-limits.md)。本表只回答：**能不能合规接入本中转站**。

| 候选 | 浏览器免费？ | 官方 API / 文档化接口？ | 允许自动化打 Web UI？ | 登录/验证码 | 额度公开？ | **是否适合接入中转站** | 依据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT Web | 是（Free） | 有 **OpenAI API**（另计费/配额） | **否**（禁程序化抽取） | 通常需账号 | 工具限额产品内提示 | **否（Web）**；API 另接 | [Terms](https://openai.com/policies/row-terms-of-use/) |
| Claude.ai | 是（Free） | 有 **Anthropic API** | **否**（禁 bot/script，除非 API Key） | 需账号 | 5h 会话预算，无固定条数 | **否（Web）**；API 另接 | [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) |
| Gemini Apps | 是 | 有 **Gemini API** | 不应爬 Web | Google 账号 | 5h+周，算力型 | **否（Web）**；API 可接（现有 LiteLLM） | [Apps limits](https://support.google.com/gemini/answer/16275805) |
| Copilot 免费 | 可不登录 ⚠️ | Graph/企业 API 另论 | 未授权自动化高风险 | 可选登录 | 未公布条数 | **否** | Microsoft Support |
| Duck.ai | **免登录** | **无**官方「当 API 用」文档 | 未声明允许第三方 API 化 | 否 | 有日限额，数字未公开 | **否**（免登录≠API） | [Duck.ai limits](https://duckduckgo.com/duckduckgo-help-pages/duckai/usage-limits) |
| HuggingChat guest | 可游客 | HF Inference Providers（付费/积分） | Guest 可被压到 0；自动化易触发限制 | 游客可选 | 负载相关 | **否（Web guest）** | HF discussion |
| DeepSeek Chat Web | 免费需账号 | **有官方 API**（按量） | Web 未授权自动化 | 需账号 | Web 未公布硬顶 | **否（Web）**；API 可评估 | [API rate limit](https://api-docs.deepseek.com/quick_start/rate_limit/) |
| Perplexity Web | 有 Free | **Sonar API** | 勿爬 Web | 可选 | Pro Search 很少 | **否（Web）** | Pricing / Help |
| 智谱 / 硅基 / 魔搭 / Groq / OpenRouter | N/A（API） | **是** | 走官方 API | Key | 控制台可见 | **是**（现有 LiteLLM） | 各官方文档 |
| **自建 Demo Web fixture** | 是（本地） | 本仓库 OpenAPI | **是**（自有服务，明确允许） | 无 | 无限（本地） | **是（Demo）** | `gateway/fixtures/` |
| **MockWebProvider** | N/A | 进程内 | N/A | 无 | N/A | **是（架构验证）**；**不是真实 Web AI** | `gateway/app/providers/mock_web.py` |

## 本 Demo 实际接入

| Provider | 类型 | 状态 |
| --- | --- | --- |
| `mock_web` | 进程内 Mock | **已验证**（单测 + E2E） |
| `demo_web` | 自建合规 Web fixture | **已验证**（Provider↔fixture） |
| `openai_compat` | 官方 OpenAI 兼容 API | **已实现**；真实上游依赖环境变量 Key，**有 Key 才启用** |

**未验证 / 因规则无法验证**：对 ChatGPT/Claude/Duck.ai 等第三方 Web UI 的程序化抓取（本仓库明确不做）。

### Duck.ai BrowserUI 诊断补充（2026-10-20）

- 只读探针：页面可打开（HTTP 200，可见 textarea），**不是**首屏 access denied。
- 条款：`https://duckduckgo.com/duckai/privacy-terms` 明确禁止 **automated querying** 与将 Duck.ai 用于提供 AI 服务。
- 实现：`BrowserUIProvider` 对 `duck.ai` / `duck_ai` **硬拒绝**（`stage=policy`）；本地替代见 `gateway/fixtures/duck_ui_fixture_server.py`。
- 详细报告：`docs/diagnostics/duckai-browser-ui-report.md`。
