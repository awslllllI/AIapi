# 调研：主流 AI Web 版限制、封号条件与免登录 Web AI

> **核验日期**：2026-10-19（UTC+8）  
> **方法**：优先官方 Help / Pricing / Terms；数字未公开处标 ⚠️ 或不写死。  
> **范围**：消费者 **Web 聊天产品**（非开发者 API，除非对比需要）。  
> **边界**：本文只做公开政策与额度盘点。**不**提供登录绕过、会话劫持、反爬对抗、cookie 复用或 WebChat2API 实现步骤。对 ChatGPT / Claude 等需登录产品做程序化抽取，普遍违反 ToS，本仓库不纳入该路径。

---

## 结论摘要

1. **主流 Web 免费层几乎都不公布「固定条数」**：ChatGPT Free 宣称日常文本「unlimited（受滥用防护约束）」；Claude / Gemini 用 **算力型额度 + 约 5 小时滚动窗 + 周上限**；Grok Free / DeepSeek Web 多为 **best-effort**。精确数字以产品内 Settings → Usage 为准。  
2. **封号 / 停权高频触发**：账号共享、程序化抽取输出、绕过速率与安全护栏、未授权 bot/script 访问消费者 UI（Anthropic 明文禁止）、滥用内容策略。OpenAI 另单列「不当分享账号 / API Key」。  
3. **免登录可用**：Duck.ai（日限额）、Microsoft Copilot（官方称可不登录，但 ⚠️ 部分入口 reportedly 出现登录墙）、部分 HuggingChat guest（负载高时可 guest=0）、Brave Leo（浏览器内）。**免登录 ≠ 允许当 API 后端**；多数仍禁自动化。  
4. **对聚合项目的含义**：WebChat2API（逆向网页当 API）**不能**作为本仓库生产路径；扩展额度应走官方 Free API、公开 playground/API、或明确允许程序访问的服务。免登录 Web 若要纳入，仅限其 **官方公开接口** 或对方明确许可的集成，否则风险与「登录墙逆向」同类。

---

## 1. 主流需登录 / 强账号 Web 产品

### 1.1 总览表

| 产品 | 登录 | 验证 | 免费额度（官方口径） | 重置 | 自动化 / 分享相关风险 |
| --- | --- | --- | --- | --- | --- |
| **ChatGPT** | 通常需账号；访客能力随时间收紧 ⚠️ | 邮箱；部分地区/风控要手机 | 日常文本：**unlimited**（滥用防护）；上传/生图/语音/数据分析等**分工具限额**；产品内提示重置 | 工具限额以产品提示为准 | 禁止程序化抽取 Output；禁绕过限制；禁分享账号 |
| **Claude.ai** | 需账号 | 邮箱等 | **会话额度**，约 **每 5 小时**重置；条数随负载/长度/模型/功能变化，**无固定消息数**；Free **无**周额度/usage credits | 5h 滚动；付费另有周限额 | 除 API Key 或明示允许外，**禁止 bot/script**；禁 scrape；禁分享账号 |
| **Gemini Apps** | Google 账号 | Google 体系 | **算力型**标准限额；**每 5 小时**刷新，直至碰到**周上限**；无 AI plan 时 context **32k** | 5h + 周 | 消费者 UI ≠ API；开发请用 Gemini API |
| **Microsoft Copilot（免费）** | 官方：**可不登录**；登录解锁历史/更长对话等 | 微软账号可选 | 无公开固定条数；**受容量与限制约束**；触顶可升级或稍后再来 | 未公布精确表 | 企业侧有标准/优先访问；消费者自动化通常违约 |
| **Grok（grok.com）** | 需 X / 邮箱等 | 账号 | Free：**Limited** Chat / agent；**无**公开消息数；Settings → Usage | Free 与付费周池分开；付费为**周用量池** | 以 xAI ToS 为准；未把 Web 当稳定 API |
| **DeepSeek Chat** | 需账号 | 常见邮箱/手机 | Web **免费**、无「Plus」订阅墙；**未公布**日消息硬顶；高峰可能限速 | 未公布 | API 另计费；Web ≠ API SLA |
| **Perplexity** | 可轻量用；完整功能偏账号 | 可选 | Free：基础搜索近 unlimited；**Pro Search 很少**（历史文档曾写 5/日或 5/4h；现定价页写 limited weekly ⚠️） | 日/周随产品变 | 有官方 Sonar API；勿爬 Web |
| **Mistral Le Chat** | 登录后功能更全 | 账号 | Free：**各功能有日上限**（搜索/Canvas/生图/上传/代码解释器等），**官方不公布具体数字** | 按日（官方表述） | 开发走 Mistral API |
| **Poe / Character.AI** | 需账号 | 常见 | 订阅/积分驱动；免费层紧 | 产品内 | 第三方自动化高风险 |

### 1.2 ChatGPT（Web）

| 项 | 内容 | 来源 |
| --- | --- | --- |
| 模型 / 能力 | Free 默认模型会换代（核验时 FAQ 写 GPT-5.6 Luna 等）；联网、上传、GPTs、生图等可用但工具有独立限额 | [Free Tier FAQ](https://help.openai.com/en/articles/9275245-using-chatgpt-s-free-plan) · [Pricing](https://chatgpt.com/pricing/) |
| 文本聊天 | **Unlimited everyday text chats**，subject to abuse-prevention safeguards | 同上 |
| 工具限额 | 文件/图片上传、生图、语音、数据分析等**分别限流**；触顶后需等待；产品内显示重置时间 | Free Tier FAQ |
| 历史硬数字 | 旧版「某模型 10 条 / 5 小时」类说明会随模型替换失效 ⚠️，勿当现行 SLA | 旧 Help 文 |
| 封号相关 | 禁止：自动/程序化抽取 data 或 Output；绕过 rate limit / 防护；分享凭据；不当内容等 | [Terms of Use](https://openai.com/policies/row-terms-of-use/) · [Account sharing](https://help.openai.com/en/articles/10471989-openai-account-sharing-policy) · [Deactivation](https://help.openai.com/en/articles/10562188-why-was-my-openai-account-deactivated) |

**ToS 原文要点（OpenAI）**：不得 *Automatically or programmatically extract data or Output*；不得 *circumvent any rate limits or restrictions or bypass any protective measures*；不得分享账号凭据。

### 1.3 Claude.ai

| 项 | 内容 | 来源 |
| --- | --- | --- |
| Free | Web/桌面/手机聊天；Sonnet/Haiku 等（Opus 等常在付费）；Artifacts、联网等见定价表 | [Pricing](https://claude.com/pricing) |
| 用量 | **无固定消息数**；会话预算受长度、复杂度、模型、功能影响；**约每 5 小时**重置；Free **无** weekly limit / usage credits | [Usage & length limits](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work) · [Get started](https://support.claude.com/en/articles/8114491-get-started-with-claude) |
| Pro 对比 | 官方称 Pro 每 5h 会话用量至少约 Free 的 **5×**；另有**周限额** | Pricing FAQ |
| 封号相关 | 禁 scrape；禁逆向；**除 API Key 或明示允许外禁止 bot/script 等非人访问**；禁分享账号；禁转售/用服务训练竞品等 | [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) §3 |

**对 WebChat2API 的直接含义**：Anthropic 把「用脚本打 Claude.ai」与「用 Anthropic API Key」写成互斥路径；订阅 OAuth 给第三方 harness 也被官方与媒体报道点名违规。

### 1.4 Gemini Apps（gemini.google.com）

| 项 | 内容 | 来源 |
| --- | --- | --- |
| 计量 | Compute-based；与 prompt 复杂度、模型/功能、对话长度有关 | [Apps limits](https://support.google.com/gemini/answer/16275805) |
| 刷新 | **每 5 小时**刷新，直到碰到 **weekly limit** | 同上 |
| 无 AI plan | Standard limits；context window **32k tokens** | 同上 |
| AI Plus / Pro / Ultra | 约为标准的 2× / 4× /（相对 Pro 的 5× 或 20×） | 同上 |
| 触顶 | 可等刷新、升级；有订阅时可能落到 Flash-Lite 继续聊 | 同上 |
| 与 API 区别 | **Web Apps ≠ Gemini API Free Tier**；API 有 RPM/TPM/RPD，见 AI Studio | [API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) |

### 1.5 Microsoft Copilot（消费者）

| 项 | 内容 | 来源 |
| --- | --- | --- |
| 入口 | copilot.cloud.microsoft / Edge / 应用 | [Free vs M365](https://support.microsoft.com/en-us/microsoft-365-copilot/what-s-the-difference-between-microsoft-copilot-free-and-copilot-in-microsoft-365) |
| 登录 | **Sign in isn't required**；登录解锁历史、更长对话、语音等 | 同上 |
| 限额 | 免费聊天等 **subject to available capacity and limits**；触顶可升级或稍后再来；**无公开条数表** | [App updates](https://support.microsoft.com/en-us/microsoft-365-copilot/learning/changes-microsoft-copilot-app) |
| ⚠️ 客态 | 第三方报道部分 Edge/Bing/App 入口出现**登录墙**，与帮助中心「可不登录」不完全一致；以实际页面为准 | 社区报道，非正式公告 |
| M365 | 另有 AI credits / feature limits（订阅所有者不可分享权益） | [AI credits](https://support.microsoft.com/en-us/microsoft-365-copilot/ai-credits-and-limits-for-microsoft-365-subscriptions) |

### 1.6 Grok（xAI）

| 项 | 内容 | 来源 |
| --- | --- | --- |
| Free | Limited Chat / agent requests；**不公布**条数 | [Pricing](https://x.ai/pricing) · [FAQ](https://docs.x.ai/grok/faq) |
| 付费 | 跨 Chat / Imagine / Voice / Build（及部分 API）的**共享周用量池**；Settings → Usage | FAQ |
| 触顶后 | 付费周池用尽后仍可回落到 **Free 档 Chat/Voice**（与周池分开重置） | FAQ |

### 1.7 DeepSeek Chat（chat.deepseek.com）

| 项 | 内容 | 来源 |
| --- | --- | --- |
| Web | 个人免费；无消费者「Plus」解锁 Web | 产品事实 + 第三方整理；官方未发 Web 条数表 |
| 限额 | **无官方固定日消息数**；高峰可能限速；社区偶发短冷却 ⚠️ | 非官方观测 |
| API | 按量；并发上限按模型（如 flash 2500 / v4-pro 500 并发量级，以文档为准） | [API rate limit](https://api-docs.deepseek.com/quick_start/rate_limit/) |

### 1.8 Perplexity / Mistral Le Chat（摘要）

| 产品 | 官方要点 | 来源 |
| --- | --- | --- |
| Perplexity Free | 基础搜索近 unlimited；Pro Search **很少**；高级模型/生图等偏 Pro；定价页现写 limited weekly ⚠️ | [Pricing](https://www.perplexity.ai/hub/pricing) · Help/Blog 历史数字可能过时 |
| Le Chat Free | 联网、Canvas、生图、上传、Code Interpreter 等均有**每日上限**，**不公布数字** | [Free limitations](https://help.mistral.ai/en/articles/316384-what-are-the-features-and-limitations-of-le-chat-free) |

---

## 2. 封号 / 停权条件（跨厂商共性）

下列为多家官方反复出现的类别（非穷尽）：

| 类别 | 典型表述 | 代表来源 |
| --- | --- | --- |
| **程序化抽取 / 爬虫** | 自动或程序化提取 data/Output；crawl/scrape/harvest | OpenAI Terms；Anthropic Consumer Terms §3.4 |
| **非人访问消费者 UI** | bot / script / automated means（除非走官方 API Key 或明示允许） | Anthropic §3.7 |
| **绕过限制** | 规避 rate limit、安全护栏、保护措施 | OpenAI Terms；Anthropic「bypass protective measures」 |
| **账号共享 / 转售** | 分享凭据；把账号提供给他人；转售访问 | OpenAI Account Sharing；Anthropic Account；多家 Usage Policy |
| **内容违规** | 儿童剥削、暴力、诈骗、仇恨骚扰等 | OpenAI Usage Policies / 停用说明 |
| **安全可疑** | 盗号、异常流量 → 临时冻结 | OpenAI deactivation FAQ |

**工程推论（非操作指南）**：WebChat2API 类项目天然踩中「程序化抽取 + 非人访问 + 常伴随多账号/共享」——与「研究额度」目标冲突，封号概率高、且无 SLA。

---

## 3. 免登录 / 极低摩擦 Web AI（纳入范围）

> 「免登录」仅指浏览器可直接开聊；**不等于**允许无密钥批量调用。纳入聚合前必须核对对方 ToS / 是否提供公开 API。

| 产品 | 登录 | 额度（官方） | 备注 | 来源 |
| --- | --- | --- | --- | --- |
| **Duck.ai**（DuckDuckGo） | **不需要** | Free 有 **daily limit**（不公布具体条数）；Plus/Pro 提高；订阅另有日+周限额，日限 00:00 UTC，周限周日 00:00 UTC | 匿名代理到第三方模型；VPN/蜂窝可能误触限额 | [Usage limits](https://duckduckgo.com/duckduckgo-help-pages/duckai/usage-limits) · [Duck.ai](https://duckduckgo.com/duckduckgo-help-pages/duckai) |
| **Microsoft Copilot** | **可不登录**（⚠️ 部分入口可能改登录墙） | 容量与功能限制，无固定公开表 | 登录解锁更多能力 | Microsoft Support（上表） |
| **HuggingChat guest** | 可不登录 | Guest 限额随**服务器负载**调整；高峰可出现 **guest=0** | 官方维护者在讨论区说明 | [HF discussion](https://huggingface.co/spaces/huggingchat/chat-ui/discussions/610) |
| **Brave Leo** | 浏览器内，通常无需单独账号 | 日限额（以 Brave 帮助为准） | 绑在 Brave 浏览器 | Brave 文档（自行核验） |
| **部分「游客 ChatGPT」** | 历史上存在更开放的游客模式 | 限额极紧且常变 ⚠️ | 勿依赖 | 产品行为易变 |
| **LMSYS / 竞技场类** | 常可游客 | 队列与滥用防护；非稳定后端 | 评测导向 | 站点说明 |
| **Meta AI** | 常依赖 Meta 生态账号/应用 | 非真正「零身份」 | 与「纯网页免登录」不完全同类 | 产品页 |

### 3.1 免登录通道的聚合价值评估

| 维度 | 评估 |
| --- | --- |
| 额度 | 通常 **日限额 + IP/匿名指纹**；Duck.ai 明确日限且 VPN 易误伤 |
| 稳定性 | Guest 可被随时压到 0（HuggingChat） |
| 合规 | 仍可能禁止自动化；需单独读 ToS |
| Agent 适配 | 缺稳定 tool calling、流式合同、密钥隔离 → **不适合**当 Harness 主后端 |
| 合理用法 | 人工备用入口、或对方**提供官方 API/插件**时再接入 LiteLLM |

---

## 4. WebChat2API 路径判断（本仓库立场）

| 路径 | 是否建议 | 原因 |
| --- | --- | --- |
| 逆向 ChatGPT / Claude / Gemini **登录态** Web → 伪 API | **否** | 明文 ToS 禁止；风控与封号；协议易碎；毕设/生产均不可靠 |
| 用订阅 Cookie / OAuth 喂第三方 harness | **否** | Anthropic 等已公开打击；OpenAI 禁分享与程序化抽取 |
| 免登录页「无头浏览器刷接口」 | **否** | 仍属自动化滥用；额度按匿名身份聚合，一封全站 |
| **官方 Free / 试用 API** + failover | **是** | 与现有 LiteLLM 方案一致 |
| 仅调研额度/政策（本文） | **是** | 决策依据，不实现违规适配器 |

已有相关结论见：[`research-free-ai-aggregation.md`](./research-free-ai-aggregation.md) §2。

---

## 5. 若目标是「比免费 API 更宽」的合法扩展方向

1. **继续挖官方 Free API**：Gemini / Groq / CF Workers AI / 智谱 Flash / 硅基 / 魔搭 / OpenRouter `:free`（见现有 periodic-free 文档）。  
2. **低价按量**：DeepSeek API、国内云按量，比 Web 爬取更稳。  
3. **明确允许的公开接口**：厂商 bots、插件商店、官方「Connect」——只接文档化 endpoint。  
4. **自建开源模型**：本地 / 便宜 GPU，彻底摆脱 Web 额度与 ToS。  
5. **免登录产品**：仅当其发布 **API 或书面许可** 后再评估接入；否则只作人工备用。

---

## 参考链接

- ChatGPT Free FAQ：https://help.openai.com/en/articles/9275245-using-chatgpt-s-free-plan  
- ChatGPT Pricing：https://chatgpt.com/pricing/  
- OpenAI Terms：https://openai.com/policies/row-terms-of-use/  
- OpenAI Account Sharing：https://help.openai.com/en/articles/10471989-openai-account-sharing-policy  
- Claude Pricing：https://claude.com/pricing  
- Claude usage limits：https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work  
- Anthropic Consumer Terms：https://www.anthropic.com/legal/consumer-terms  
- Gemini Apps limits：https://support.google.com/gemini/answer/16275805  
- Copilot free vs M365：https://support.microsoft.com/en-us/microsoft-365-copilot/what-s-the-difference-between-microsoft-copilot-free-and-copilot-in-microsoft-365  
- Grok FAQ / Pricing：https://docs.x.ai/grok/faq · https://x.ai/pricing  
- DeepSeek API rate limit：https://api-docs.deepseek.com/quick_start/rate_limit/  
- Duck.ai limits：https://duckduckgo.com/duckduckgo-help-pages/duckai/usage-limits  
- Mistral Le Chat Free：https://help.mistral.ai/en/articles/316384-what-are-the-features-and-limitations-of-le-chat-free  
- Perplexity Pricing：https://www.perplexity.ai/hub/pricing  

---

*本文为调研笔记，不构成法律意见；限额以各产品内 Usage 页面与现行 ToS 为准。*
