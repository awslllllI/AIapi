# 调研：免费 AI API 聚合与网页端自动化评估

> **核验日期**：2026-10-19（UTC+8）  
> **方法**：优先引用官方文档 / 定价页 / 速率限制页 / ToS；数值均附 URL。  
> **重要提示**：免费配额、模型名单、地区可用性变更极快；上线前请在各控制台「Limits / Billing」再核一次。标有 ⚠️ 的条目为易变或账户级差异项。

---

## 结论摘要

1. **纯 $0 + 可用于 Agent 聚合的「常驻免费」骨干**：Google Gemini API Free Tier（地区受限）、Groq Free、Cloudflare Workers AI（每日 10k Neurons）、智谱 GLM Flash 系列（定价页标「免费」）、硅基流动部分 ≤9B 免费模型、魔搭 ModelScope 日调用额度、OpenRouter `:free`（日请求极少）。  
2. **仅适合 overflow / 试用**：Cohere Trial（1k 次/月）、Cerebras Free Trial（$5 + 绑卡，30 天）、百炼 / 千帆 / 豆包 / Kimi / 混元等**新人试用额度**（有期限，用完即停或转付费）。  
3. **已关闭或不宜当作免费骨干**：GitHub Models（2026-07-30 退役）、Together AI（无 free trial，需预充值）、DeepSeek 官方 API（按量计费，无永久 free tier；新人赠送余额需自行确认）、SambaNova（文档仍有 Free Tier RPM/RPD，但 Plans 页要求绑卡购积分才能发请求——⚠️ 以控制台为准）。  
4. **网页端自动化当后端**：**技术上脆弱、ToS 风险高、生产可靠性差**；OpenAI / Anthropic 明文禁止对消费者网页做自动化抽取或非 API 自动化访问。产品建议：**只聚合官方 API**；网页自动化仅限个人研究玩具（若有），不进入生产路径。  
5. **推荐 0 费用策略**：多提供商 failover + 按日配额预算；CN 用户以智谱 Flash / 硅基免费 / ModelScope /（有额度时）百炼·豆包试用为骨干，海外以 Gemini Free + Groq + CF Workers AI + OpenRouter `:free` 为骨干。

---

## 1. 免费 API 服务清单

### 1.1 总览表

| Provider | 状态 | 注册摩擦 | OpenAI 兼容 | 适合角色 |
| --- | --- | --- | --- | --- |
| Google Gemini API | 常驻 Free Tier（地区限制） | Google 账号；无强制绑卡进 Free | 官方 SDK + 社区兼容层 | **骨干** |
| Groq | 常驻 Free Plan $0 | 邮箱；升级 Developer 需支付方式 | ✅ `api.groq.com/openai/v1` | **骨干**（低延迟） |
| OpenRouter `:free` | 常驻 0 价模型变体 | 账号；日限额极紧 | ✅ | **溢出 / 兜底** |
| Mistral Free mode | 含月度 included usage（非无限） | 账号；额度见控制台 | ✅ | **轻量试用** |
| Cloudflare Workers AI | 常驻 10k Neurons/日 | CF 账号 | REST / Workers binding（非标准 OpenAI 全集） | **骨干溢出** |
| NVIDIA build.nvidia.com | Trial / 评测（无永久 free SLA） | NVIDIA 账号 | 类 OpenAI chat | **评测 overflow** |
| Cohere Trial | Trial（非生产） | 无卡；Trial key 自动发放 | 自有 API（非完整 OpenAI） | **轻量 overflow** |
| Cerebras | Trial（$5，绑卡，30 天） | **需支付方式** | ✅ | **短期试用 only** |
| SambaNova | 文档 Free Tier；Plans 要求绑卡购积分 ⚠️ | 支付方式倾向强制 | ✅ 类 OpenAI | **不确定 / 慎用** |
| GitHub Models | **Dead**（2026-07-30） | — | — | 勿用 |
| DeepSeek 官方 | 按量；无永久 free | 可无卡注册；余额/赠送需自查 | ✅ | 低价付费，非 $0 |
| Together AI | **无 free trial** | 最低充值（官方：$5） | ✅ | 付费 |
| 智谱 BigModel Flash | 定价页「免费」模型 | 国内手机/实名常见 | ✅ `open.bigmodel.cn` | **CN 骨干** |
| SiliconFlow | 免费模型 + 实名券 | **实名强制**（2026-05-15 起） | ✅ | **CN 骨干** |
| ModelScope | 日免费调用 | 阿里云账号/实名 | ✅ Inference | **CN 日配额** |
| 阿里云百炼 DashScope | 新人试用（90 天） | 可无实名用免费额度 | ✅ | **试用 / 溢出** |
| 百度千帆 | 新人试用（约 3 个月） | 百度云账号 | 自有/兼容视模型 | **试用** |
| 腾讯混元 / TokenHub | 开通赠送资源包；旧平台迁 TokenHub | 实名 | TokenHub | **试用**（注意迁移） |
| Moonshot / Kimi API | ¥15 试用券（3 个月） | 国内手机 + 实名 | ✅ | **试用** |
| 火山方舟 / 豆包 | 新人免费推理额度 | 注册；安心模式防扣费 | ✅ | **试用** |
| Hugging Face Inference Providers | Free：**无**月额积分（需购积分或 PRO） | HF 账号 | ✅ `router.huggingface.co` | 付费为主 |
| Fireworks | 小额 signup credit（二次来源常写 $1）⚠️ | 账号 | ✅ | 忽略级试用 |
| DeepInfra | **无 free credit** | 付费 | ✅ | 付费 |

---

### 1.2 Google Gemini API / AI Studio Free Tier

| 字段 | 内容 |
| --- | --- |
| **状态** | 常驻 **Free** usage tier（非一次性 trial） |
| **注册摩擦** | Google 账号；**无**强制绑卡即可 Free。地区：仅 [available regions](https://ai.google.dev/gemini-api/docs/available-regions) 列表内（**中国大陆不在列表**）。年龄 ≥18。 |
| **模型** | Free 可访问「certain models」；具体名单与配额以 AI Studio 项目 Limits 为准（官方文档不再贴死固定 RPM 表） |
| **配额** | 维度：RPM / TPM（input）/ RPD（RPD 于太平洋时间午夜重置）。**数值账户级**：见 AI Studio。[Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) 明确：「View your active rate limits in AI Studio」「Specified rate limits are not guaranteed」。Tier：Free → Tier1（绑 billing）等见同页与 [Billing](https://ai.google.dev/gemini-api/docs/billing)。 |
| **API 形态** | 官方 Gemini API；社区大量 OpenAI-compat 代理。 |
| **Agent 稳定性** | 免费层无 SLA；高峰 429 常见；模型/配额常变。EEA/UK/CH 向终端用户提供 API Client 时条款要求用 Paid Services（[Terms](https://ai.google.dev/gemini-api/terms)）。 |
| **链接** | [Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Billing](https://ai.google.dev/gemini-api/docs/billing) · [Regions](https://ai.google.dev/gemini-api/docs/available-regions) · [Terms](https://ai.google.dev/gemini-api/terms) |

⚠️ 第三方博客仍贴「2.5 Flash 10 RPM / 500 RPD」等历史表，**不可当作 2026-10 权威数字**；以 AI Studio 为准。

---

### 1.3 Groq Free Plan

| 字段 | 内容 |
| --- | --- |
| **状态** | **Permanent free**：$0「Build and Test」Plan |
| **注册摩擦** | 注册即可 Free；升级 Developer 需支付方式（卡 / US bank / SEPA） |
| **模型** | 见 [Models](https://console.groq.com/docs/models)；生产与 Preview 模型会轮换下线 |
| **配额** | 组织级 RPM/RPD/TPM/TPD。公开文档表标注为 **Developer plan base limits**（例：`openai/gpt-oss-120b` 30 RPM / 1K RPD / 8K TPM / 200K TPD）。**Free 实际限额通常更低**，以 [Settings → Limits](https://console.groq.com/settings/limits) 为准。 |
| **API 形态** | ✅ OpenAI-compatible：`https://api.groq.com/openai/v1` |
| **Agent 稳定性** | 极快推理，适合短轮工具调用；Free 日请求/日 token 易触顶；Preview 模型可突然下线 |
| **链接** | [Plans](https://console.groq.com/settings/billing/plans) · [Rate limits](https://console.groq.com/docs/rate-limits) · [Billing FAQs](https://console.groq.com/docs/billing-faqs) |

---

### 1.4 OpenRouter `:free`

| 字段 | 内容 |
| --- | --- |
| **状态** | 常驻 **0 价模型变体**（`model:…:free`），非无限 |
| **注册摩擦** | 账号即可；账户余额为负时连 free 也可能 402 |
| **模型** | 仅目录中声明 free 变体者；列表变化快 → [models?max_price=0](https://openrouter.ai/models?max_price=0) |
| **配额** | Free 变体：|< $10 累计购积分 | 20 RPM / **50 RPD** | | ≥ $10 | 20 RPM / **1000 RPD** |。日计数 UTC 午夜重置。失败请求仍可能计日配额（OpenRouter 博客说明）。 |
| **API 形态** | ✅ OpenAI-compatible |
| **Agent 稳定性** | 上游 provider 抖动；模型轮换频繁；**不适合高 RPD agent**；适合 failover 末级 |
| **链接** | [Free variant](https://openrouter.ai/docs/guides/routing/model-variants/free) · [Limits](https://openrouter.ai/docs/api_reference/limits) |

---

### 1.5 Mistral（La Plateforme）Free mode

| 字段 | 内容 |
| --- | --- |
| **状态** | **Free mode**（默认）：含月度 included usage + 最低速率档；非「永久无限免费」 |
| **注册摩擦** | 账号；PAYG 需预充 credits |
| **模型** | 控制台可用模型；定价见 [API pricing](https://docs.mistral.ai/inference/pricing) |
| **配额** | TPM / RPS 等见 Admin → API → Limits；Help Center：Free mode 为 evaluation/prototyping 最低档 |
| **API 形态** | ✅ OpenAI-compatible |
| **Agent 稳定性** | included usage 耗尽且未开 PAYG 则停；适合轻量 |
| **链接** | [Usage and limits](https://docs.mistral.ai/admin/billing-usage/usage-limits) · [Subscriptions](https://docs.mistral.ai/admin/billing-usage/subscriptions) · [Help: rate limits](https://help.mistral.ai/en/articles/698531-why-am-i-hitting-api-rate-limits-and-how-do-i-increase-them) · [Pricing](https://mistral.ai/pricing/) |

⚠️ 月度 included 具体 token/$ 以控制台与 mistral.ai/pricing 实时页为准（变动频繁）。

---

### 1.6 Cloudflare Workers AI（Free Neurons）

| 字段 | 内容 |
| --- | --- |
| **状态** | **常驻免费额度**：10,000 Neurons / 日（Free 与 Paid 均含） |
| **注册摩擦** | Cloudflare 账号；超过日额度需 Workers Paid（$0.011 / 1k Neurons） |
| **模型** | 大量 `@cf/...`；部分 frontier（Kimi/GLM/DeepSeek 等）**要求 Paid 或 AI Gateway 预付** |
| **配额** | 10k Neurons/日，**00:00 UTC** 重置；文本生成默认约 300 RPM（Paid 模型更低，见 Limits） |
| **API 形态** | Workers binding / REST；可经 AI Gateway；**非**完整 OpenAI 生态一等公民 |
| **Agent 稳定性** | 日额度对大模型很快耗尽（Neurons≃算力）；适合小模型 / embedding / 溢出 |
| **链接** | [Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) · [Limits](https://developers.cloudflare.com/workers-ai/platform/limits/) |

**粗算示例（官方 Neurons 单价）**：`@cf/meta/llama-3.2-1b-instruct` ≈ 2457 neurons/M input + 18252/M output → 日 10k Neurons 仅支撑很小流量。

---

### 1.7 NVIDIA NIM / build.nvidia.com

| 字段 | 内容 |
| --- | --- |
| **状态** | **Trial / 评测体验**；官方论坛确认 **credits 体系已取消**，改为账户级请求速率限制 |
| **注册摩擦** | NVIDIA Developer 账号 |
| **模型** | API Catalog 上架 NIM；名单变 |
| **配额** | **不公开固定数字**；UI 右上角显示；社区常见约 ~40 RPM 量级（**非官方保证**）。无生产 SLA |
| **API 形态** | `integrate.api.nvidia.com` 类 OpenAI chat |
| **Agent 稳定性** | 差（评测定位）；不可作生产骨干 |
| **链接** | [build.nvidia.com](https://build.nvidia.com) · 论坛：[credits removed](https://forums.developer.nvidia.com/t/cannot-find-the-amount-of-credits-left-on-nim-api/337051/2) · [limits not published](https://forums.developer.nvidia.com/t/model-limits/331075) |

---

### 1.8 Cohere Trial

| 字段 | 内容 |
| --- | --- |
| **状态** | **Trial**（免费但限速；**禁止生产/商用**） |
| **注册摩擦** | 注册自动 Trial key；**无卡** |
| **模型** | Command 系列等（见 docs） |
| **配额** | Trial：**1,000 API calls / month**；Chat 多数 Command：**20 req/min**；Rerank 10/min；Embed 文本 2000 inputs/min 等 |
| **API 形态** | Cohere API（非完整 OpenAI） |
| **Agent 稳定性** | 月 1k 次对 agent 极紧；仅 PoC |
| **链接** | [Pricing FAQ](https://cohere.com/pricing) · [Rate limits](https://docs.cohere.com/docs/rate-limits) · [Pricing explained](https://docs.cohere.com/docs/how-does-cohere-pricing-work) |

---

### 1.9 Cerebras Inference

| 字段 | 内容 |
| --- | --- |
| **状态** | **Free Trial only**——官方 FAQ：「Is there a permanently free tier? **No.**」 |
| **注册摩擦** | **必须添加已验证支付方式** 才发 $5 积分；否则 Playground/API 不激活 |
| **模型** | Shared Inference 目录公开模型（如 `gpt-oss-120b`, `qwen-3.8-27b`） |
| **配额** | $5 credits，**发放后 30 天过期**。Free Trial 例：5 RPM；Uncached TPM 30K / Total TPM 90K；TPH/TPD 1M（见官方表） |
| **API 形态** | ✅ `https://api.cerebras.ai/v1` |
| **Agent 稳定性** | 试用结束后停；极速硬件适合压测，非 $0 长跑 |
| **链接** | [Rate limits](https://inference-docs.cerebras.ai/support/rate-limits) · [Pricing](https://www.cerebras.ai/pricing) |

---

### 1.10 SambaNova Cloud

| 字段 | 内容 |
| --- | --- |
| **状态** | ⚠️ **文档 vs 产品页冲突**：Rate Limits 仍定义 Free Tier（无支付方式）；[Plans](https://cloud.sambanova.ai/plans) 文案要求「Add a payment method and purchase credits to run your first requests」 |
| **注册摩擦** | 倾向 **绑卡 + 购积分** 才能真正发请求（2026-08 起二次观察） |
| **模型** | Free 文档列：`DeepSeek-V3.1`, `Meta-Llama-3.3-70B-Instruct`, `gpt-oss-120b` 等 |
| **配额（文档 Free）** | 每模型 **20 RPM / 20 RPD / 200K TPD** |
| **API 形态** | OpenAI-compatible |
| **Agent 稳定性** | 若仅 20 RPD，几乎不能跑 agent；以控制台实测为准 |
| **链接** | [Rate limits](https://docs.sambanova.ai/docs/en/models/rate-limits) · [Plans](https://cloud.sambanova.ai/plans) |

---

### 1.11 GitHub Models — **已退役**

| 字段 | 内容 |
| --- | --- |
| **状态** | **Dead**：2026-07-30 全面退休（playground / catalog / inference API / BYOK） |
| **替代** | Microsoft Foundry Models（付费 Azure）；GitHub Copilot 为另一产品 |
| **链接** | [Changelog: retired](https://github.blog/changelog/2026-07-30-github-models-is-now-retired/) · [Docs](https://docs.github.com/en/github-models) |

---

### 1.12 DeepSeek 官方 API / Together AI

#### DeepSeek（platform.deepseek.com）

| 字段 | 内容 |
| --- | --- |
| **状态** | **按量付费**；官方定价页**无永久 free tier**。账户可有 **granted balance**（促销/赠送）优先扣减——是否人人有、数额多少 **需登录自查**（二次来源称新人 500 万 tokens / 30 天，**非定价页硬编码**） |
| **配额/价** | 例：`deepseek-flash` off-peak cache miss $0.15/M in、$0.6/M out；peak 翻倍；并发上限文档：Flash 2500 / Pro 500 |
| **API** | ✅ `https://api.deepseek.com`（兼 Anthropic 格式） |
| **链接** | [Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing/) |

#### Together AI

| 字段 | 内容 |
| --- | --- |
| **状态** | **无 free trial**；需最低 **$5** 预充积分才可用 |
| **链接** | [KB: no free trial](https://support.together.ai/articles/1862638756-changes-to-free-tier-and-billing-july-2025) · [Pricing](https://www.together.ai/pricing) |

---

### 1.13 中国可访问免费 / 试用层（CN 用户重点）

#### 智谱 BigModel（GLM Flash）

| 字段 | 内容 |
| --- | --- |
| **状态** | 定价页对 **GLM-4.7-Flash / GLM-4-Flash-250414 / GLM-Z1-Flash** 及部分视觉 Flash **标「免费」**（长期 0 元，但有并发/速率） |
| **注册摩擦** | 国内开放平台常见手机号；控制台看权益等级 |
| **配额** | **账户级并发**，控制台「速率限制」查看；错误码 1302/1305/1308 |
| **API** | ✅ `https://open.bigmodel.cn/api/paas/v4/chat/completions` |
| **链接** | [定价](https://docs.bigmodel.cn/cn/guide/start/pricing) · [速率限制](https://docs.bigmodel.cn/cn/api/rate-limit) · [GLM-4.7-Flash](https://docs.bigmodel.cn/cn/guide/models/free/glm-4.7-flash) |

#### 硅基流动 SiliconFlow

| 字段 | 内容 |
| --- | --- |
| **状态** | **免费模型**（文档：实名后可用，账单显示 0）+ 实名 **¥16 代金券**（活动期至 2026-12-31，券 180 天，以官网活动为准） |
| **注册摩擦** | **2026-05-15 起未实名不可用**；实名前曾限 10 RPM |
| **配额** | 免费模型限流为固定值；付费模型按用量等级 L0–L5；账号级非 Key 级 |
| **API** | ✅ `https://api.siliconflow.cn/v1` |
| **链接** | [Rate limits](https://api-docs.siliconflow.cn/docs/userguide/faqs/rate-limit-and-upgradation) · 中国站 cloud.siliconflow.cn |

⚠️ 「≤9B 永久免费」等名单以控制台模型广场为准，社区文章易过期。

#### ModelScope 魔搭 API-Inference

| 字段 | 内容 |
| --- | --- |
| **状态** | 注册用户**日免费调用**（社区/二次核验常写：合计 **2000 次/日**，单模型 **500 次/日**，UTC+8 重置） |
| **注册摩擦** | 阿里云账号 + 实名常见 |
| **API** | OpenAI-compat：`https://api-inference.modelscope.cn/v1` |
| **链接** | [API-Inference 文档入口](https://www.modelscope.cn/docs/model-service/API-Inference) · 限额页 `/limits`（抓取时偶发 5xx，以站内为准） |

⚠️ 官方限额页本次抓取失败；数字标为 **待控制台复核**。

#### 阿里云百炼（DashScope / Model Studio）

| 字段 | 内容 |
| --- | --- |
| **状态** | **新人免费额度**（试用）：通常每模型约 **100 万 Token**，**90 天**；仅**华北 2（北京）** |
| **注意** | 已认证用户额度用完默认可转按量——务必开「用完即停」以免扣费 |
| **链接** | [新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota) · [限流](https://help.aliyun.com/zh/model-studio/rate-limit) |

#### 百度千帆

| 字段 | 内容 |
| --- | --- |
| **状态** | 首次开通赠送多模型各 **100 万 Tokens / 3 个月**（在线推理）；文档更新时间见页脚 |
| **链接** | [新用户免费额度](https://cloud.baidu.com/doc/qianfan/s/Imi2rpirg) |

#### 腾讯混元 → TokenHub

| 字段 | 内容 |
| --- | --- |
| **状态** | 首次开通赠送免费资源包（例：部分生文模型 **100 万 tokens / 1 年**）；**旧混元平台 2026-09-30 停服**，新用量走 **TokenHub** |
| **链接** | [迁移公告](https://cloud.tencent.com/announce/detail/2287) · 购买指南 PDF（含免费额度表） |

#### Moonshot / Kimi 开放平台

| 字段 | 内容 |
| --- | --- |
| **状态** | 国内手机号新用户实名后 **¥15 代金券 / 3 个月**；**不可**用于 Kimi K3 |
| **链接** | [免费试用说明](https://www.kimi.com/help/kimi-api/api-free-trial) |

#### 火山方舟 / 豆包

| 字段 | 内容 |
| --- | --- |
| **状态** | 新用户各模型免费推理额度；「安心体验模式」可限制只用赠送额度（文档示例提及 **50 万 token** 量级） |
| **链接** | [免费推理额度](https://docs.volcengine.com/docs/ark/free-inference-quota?lang=zh) · [开通管理](https://docs.volcengine.com/docs/ark/activation-management?lang=zh) |

---

### 1.14 Hugging Face Inference Providers

| 字段 | 内容 |
| --- | --- |
| **状态** | 官方定价（核验日）：**Free Users = None** 月额积分；需购积分或升 PRO（$2/月积分） |
| **说明** | 旧「Serverless Inference API 免费几百次/小时」叙事已过时；`hf-inference` 现偏 CPU 小任务 |
| **链接** | [Pricing](https://huggingface.co/docs/inference-providers/en/pricing) · [Hub rate limits](https://huggingface.co/docs/hub/rate-limits) |

---

### 1.15 Fireworks / DeepInfra

| Provider | 状态 | 说明 | 链接 |
| --- | --- | --- | --- |
| Fireworks | 预付积分；FAQ 提及 **$1** starter credit 耗尽后需加积分 | 对聚合几乎可忽略 | [Credits FAQ](https://docs.fireworks.ai/faq-new/billing-pricing/what-happens-when-i-finish-my-1-dollar-credit) · [Pricing](https://fireworks.ai/pricing) |
| DeepInfra | **无 free credit**（第三方 ledger 2026-09 核验） | 付费 | deepinfra.com |

---

## 2. 网页版 Agent 化评估

> **范围**：仅高层可行性与风险。不提供绕过登录、CAPTCHA、反爬或 ToS 规避的步骤/代码。

### 2.1 总评

| 维度 | 结论 |
| --- | --- |
| 生产可用性 | **几乎总是差**——DOM/流式协议易碎、会话失效、人机验证、IP/账号风控 |
| 法律 / ToS | 主流厂商 **High**；CN 产品亦普遍禁止未授权爬取/自动化 |
| 伦理/产品建议 | **优先官方 API**；网页自动化最多作为个人研究玩具，**不要**作为聚合后端 |

### 2.2 分产品评估

| 产品 | 技术可行性（高层） | ToS 风险 | 生产可靠性 | 账号/IP 风险 |
| --- | --- | --- | --- | --- |
| **ChatGPT Web** | 登录墙 + Cloudflare/反自动化；DOM 与流式事件常变；CAPTCHA/设备校验 | **High**：禁止自动/程序化抽取 Output；禁止干扰服务、绕过限制（[OpenAI Terms](https://openai.com/policies/row-terms-of-use/)） | 差 | 封号、限制、挑战页 |
| **Claude.ai** | 登录墙；强反自动化；订阅 OAuth 与 API 路径分离 | **High**：除 Anthropic API Key 或明示允许外，禁止 bot/script 等非人访问；禁 scrape（[Consumer Terms](https://www.anthropic.com/legal/consumer-terms) §3） | 差 | 明确打击第三方 harness |
| **Gemini Web** | 登录 + Google 风控；与 AI Studio/API 配额体系分离 | **Medium–High**：消费者产品 ToS / 自动化限制需单独核验；开发场景应走官方 API | 差 | 账号风控 |
| **Bing Copilot** | 微软账号 + 前端复杂；反爬 | **High**（典型禁止自动化抓取服务） | 差 | IP/账号节流 |
| **Poe** | 聚合前端；订阅额度；反自动化 | **High**（第三方自动化通常违约） | 差 | 订阅滥用封禁 |
| **Perplexity** | 搜索+生成混合 UI；强风控 | **High** | 差 | 速率与封禁 |
| **豆包 / Kimi / 元宝 / 通义 网页** | 登录/手机验证常见；国产站风控与验证码常见 | **Medium–High**（各产品用户协议通常禁爬虫与未授权自动化；以各站协议为准） | 差 | 设备/手机号风控 |

### 2.3 共性技术障碍（不下钻利用细节）

- **登录与会话**：Cookie / OAuth 短时有效，多因素与设备绑定。  
- **Bot 检测**：CDN（如 Cloudflare）、行为分析、验证码。  
- **DOM / 协议不稳定**：前端发版即断。  
- **流式输出**：非公开稳定 SSE 合同，难做可靠重试与工具调用。  
- **无 SLA**：消费者 UI 为交互设计，非机器吞吐。

### 2.4 产品建议

1. Agent / 聚合服务：**只接官方或明确允许的 API**。  
2. 需要「ChatGPT/Claude 质量」→ 付费 API 或合规代理，而不是网页。  
3. 网页自动化：**不**纳入架构图；文档与销售材料勿暗示支持。

---

## 3. 聚合架构建议（0 费用优先）

### 3.1 设计原则

1. **OpenAI-compatible 统一出口**：内部只实现一套 `chat.completions` + tool calling 适配层。  
2. **多提供商 failover**：429 / 5xx / 超时 → 下一 provider；记录原因做配额学习。  
3. **日配额预算器**：按 UTC 或各家重置时区维护「剩余 RPD/TPD/Neurons」；优先耗「会过期的试用」，常驻免费留作保底。  
4. **模型能力分级**：routing 按「工具调用 / 长上下文 / 中文 / 速度」选池，而不是死绑单一 model id。  
5. **绝不**把网页 UI 放进 failover 链。

### 3.2 推荐角色划分

| 角色 | 海外优先 | 中国大陆优先 |
| --- | --- | --- |
| **骨干（常驻 $0）** | Gemini Free（若在可用地区）、Groq Free、CF Workers AI（小模型） | 智谱 Flash、硅基免费模型、ModelScope 日额度 |
| **溢出** | OpenRouter `:free`、Mistral Free mode 剩余 included | 百炼/豆包/千帆**剩余试用**（开「用完即停」） |
| **短试用加速** | Cerebras $5（绑卡）、NVIDIA trial、Cohere 1k/月 | Kimi ¥15、混元资源包 |
| **明确排除** | GitHub Models、Together free、网页自动化 | 同上 |

### 3.3 日预算示意（逻辑，非保证数字）

```
每日开始：
  refresh_quotas(Gemini, Groq, CF, Zhipu, SiliconFlow, ModelScope, OpenRouter)
  prefer(expiring_trials)  # 百炼/豆包/千帆/Kimi 等
  then(backbone_free)
  then(openrouter_free)    # 50 RPD 极珍惜
Agent 请求：
  pick(providers capable of tools & locale)
  on 429 → backoff + failover
  never → browser_ui
```

### 3.4 可靠性预期（诚实）

- **$0 聚合无法提供商业 SLA**；目标应是「尽力而为的高可用」，接受降级模型。  
- 免费层常见：**RPM 先死、RPD 中午死、模型 id 半夜换**。  
- 监控：每 provider 成功率、429 率、日剩余配额；配额将尽时主动降级到更小模型。

### 3.5 合规提醒

- 遵守各 ToS：禁止将 Trial key 用于生产（Cohere）、禁止绕过速率与防护。  
- 密钥与公司服务器地址**禁止硬编码**（项目规范）；用环境变量/密钥管理。  
- CN 实名、海外地区限制（Gemini）决定账号策略，勿用违规「多号」对抗限额（易全军覆没）。

---

## 参考链接

### 海外 / 全球

- Gemini：[Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Billing](https://ai.google.dev/gemini-api/docs/billing) · [Regions](https://ai.google.dev/gemini-api/docs/available-regions) · [Terms](https://ai.google.dev/gemini-api/terms)  
- Groq：[Plans](https://console.groq.com/settings/billing/plans) · [Rate limits](https://console.groq.com/docs/rate-limits)  
- OpenRouter：[Free variant](https://openrouter.ai/docs/guides/routing/model-variants/free) · [Limits](https://openrouter.ai/docs/api_reference/limits)  
- Mistral：[Usage limits](https://docs.mistral.ai/admin/billing-usage/usage-limits) · [Pricing](https://mistral.ai/pricing/)  
- Cloudflare Workers AI：[Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) · [Limits](https://developers.cloudflare.com/workers-ai/platform/limits/)  
- Cerebras：[Rate limits](https://inference-docs.cerebras.ai/support/rate-limits)  
- SambaNova：[Rate limits](https://docs.sambanova.ai/docs/en/models/rate-limits) · [Plans](https://cloud.sambanova.ai/plans)  
- Cohere：[Rate limits](https://docs.cohere.com/docs/rate-limits) · [Pricing](https://cohere.com/pricing)  
- DeepSeek：[Pricing](https://api-docs.deepseek.com/quick_start/pricing/)  
- Together：[No free trial](https://support.together.ai/articles/1862638756-changes-to-free-tier-and-billing-july-2025)  
- GitHub Models retired：[Changelog](https://github.blog/changelog/2026-07-30-github-models-is-now-retired/)  
- Hugging Face：[Inference Providers pricing](https://huggingface.co/docs/inference-providers/en/pricing)  
- NVIDIA NIM trial（论坛）：[credits removed](https://forums.developer.nvidia.com/t/cannot-find-the-amount-of-credits-left-on-nim-api/337051/2)  

### 中国

- 智谱：[定价](https://docs.bigmodel.cn/cn/guide/start/pricing) · [速率限制](https://docs.bigmodel.cn/cn/api/rate-limit)  
- 硅基流动：[Rate limits](https://api-docs.siliconflow.cn/docs/userguide/faqs/rate-limit-and-upgradation)  
- ModelScope：[API-Inference](https://www.modelscope.cn/docs/model-service/API-Inference)  
- 阿里云百炼：[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)  
- 百度千帆：[新用户免费额度](https://cloud.baidu.com/doc/qianfan/s/Imi2rpirg)  
- 腾讯 TokenHub 迁移：[公告](https://cloud.tencent.com/announce/detail/2287)  
- Kimi：[免费试用](https://www.kimi.com/help/kimi-api/api-free-trial)  
- 火山方舟：[免费推理额度](https://docs.volcengine.com/docs/ark/free-inference-quota?lang=zh)  

### ToS（网页自动化相关）

- OpenAI：[Terms of Use](https://openai.com/policies/row-terms-of-use/)  
- Anthropic：[Consumer Terms](https://www.anthropic.com/legal/consumer-terms)  

---

*本文为调研笔记，不构成法律意见；配额数字请以各控制台实时页面为最终依据。*
