# Browser Provider 架构设计与实施计划

项目：D:\Project\ai-api
日期：2026-10-20
状态：设计与实施边界已确定；后续按阶段实现。本文件不代表浏览器 Provider 已经实现。

## 1. 目标

为聚合中转站提供可插拔的站点接入方式：优先官方 API / 明确授权接口；其次是站点允许的浏览器自动化；无可用上游时使用 Mock。对调用方统一提供模型列表、普通对话、流式能力（站点实际支持时）、错误映射和可观测性。

“模拟真人操控”指使用正常浏览器执行页面导航、输入、点击、等待和读取结果，不代表伪装指纹、规避检测或绕过服务方访问限制。

## 2. 重要边界

- 不实现代理/IP 轮换、浏览器指纹伪装、验证码自动求解、隐藏接口探测、盗取或跨账户复用 Cookie、封禁后自动换号重试等规避机制。
- 登录、验证码、MFA、访问拒绝、封禁提示、明确的自动化限制出现时，站点状态进入 NEEDS_HUMAN 或 BLOCKED，停止请求，不继续重试。
- 对服务条款不允许的自动化站点，不启用 Browser Provider；使用官方 API、获得授权的集成方式或 Mock。
- 所有限速用于遵守公开额度、降低误操作和控制负载，不作为躲避检测的手段。
- 账号密码、Cookie、storageState、API Key 不进 Git；使用环境变量或本地秘密存储，日志脱敏。

## 3. 接入策略：按能力分层

1. official_api：官方 API 或明确授权的程序化接口，首选。
2. browser_ui：站点允许的浏览器自动化，使用 Playwright 执行用户可见的页面操作。
3. mock：本地 fixture，用于开发、测试和无授权服务的替代验证。

每个站点一个 Provider 插件，但共享浏览器运行时、会话存储、任务状态机、限流、指标、错误映射和测试工具。避免每个站点复制一份浏览器生命周期代码。

## 4. 组件建议

- SiteManifest：站点 ID、模式、入口 URL、允许的域名、登录方式、输入框/发送按钮/回答区域定位器、提交方式、结果完成条件、流式策略、能力标记。
- ProviderRegistry：根据配置启用 Provider，禁止未配置或未审核的站点被动态访问。
- BrowserRuntime：管理 Playwright browser/context/page；每个站点、账户使用隔离的 context；设置导航与动作超时。
- AuthManager：支持手动登录后保存授权状态、环境变量凭证和登录过期检测。遇到 MFA/验证码时暂停并提示用户手动完成，不尝试自动绕过。
- ConversationExecutor：状态机 IDLE → NAVIGATING → AUTH_CHECK → SUBMITTING → WAITING_RESPONSE → EXTRACTING → COMPLETED；异常进入 RETRY_WAIT、NEEDS_HUMAN 或 BLOCKED。
- ResponseParser：先使用可访问性语义（role/label/test id），再使用站点配置的 CSS locator；不要依赖单一脆弱的 DOM 层级。
- PolicyGate：域名 allowlist、站点自动化许可状态、每站点并发与速率上限、熔断、挑战/封禁停止规则。
- SessionStore：持久化登录状态到本地受保护目录；默认禁止提交 Git；权限最小化、可撤销、支持过期清理。
- Telemetry：记录 provider、站点、耗时、错误类别、重试次数、登录状态和成功率；不记录密码、Cookie、完整敏感页面或未经脱敏的用户对话。

## 5. 配置模型

配置描述“接入方式、登录、可靠性、访问边界”，而不是反检测参数。

示例（仅示意，字段名后续按现有 Pydantic Settings 统一）：

```yaml
browser:
  enabled: false
  headless: false
  navigation_timeout_ms: 30000
  action_timeout_ms: 10000
  session_dir: .local/browser-sessions
  stop_on_challenge: true
  stop_on_access_denied: true
  redact_logs: true

sites:
  example_allowed_site:
    enabled: false
    mode: browser_ui
    automation_authorized: false
    base_url: https://example.invalid
    allowed_domains:
      - example.invalid
    auth:
      mode: manual_session
      username_env: EXAMPLE_USERNAME
      password_env: EXAMPLE_PASSWORD
      storage_state_path: .local/browser-sessions/example.json
    selectors:
      prompt: '[data-testid="prompt-input"]'
      submit: '[data-testid="send-button"]'
      answer: '[data-testid="assistant-message"]'
    limits:
      max_concurrency: 1
      min_interval_ms: 5000
      requests_per_minute: 6
      max_retries: 1
      retry_backoff_ms: [1000, 3000]
    challenge_policy: pause_for_human
    access_denied_policy: disable_provider
```

automation_authorized: false 和 enabled: false 是默认关闭策略；不能把示例域名或选择器当成真实服务适配器。

## 6. 认证和会话

- API Key / 用户名密码只从环境变量或 secret store 读取。
- 浏览器登录优先由用户在可见浏览器中完成，再把 Playwright storage state 保存到 .local/browser-sessions/；该目录加入 .gitignore。
- 如需通过表单登录，必须是服务允许的常规登录流程；不得绕过验证码、MFA、访问控制或自动化限制。
- 401/登录页重定向可触发一次重新认证提示；不要循环提交凭证。
- Cookie/storageState 是敏感凭证，日志中不输出其内容；支持删除、重新生成和按站点隔离。

## 7. 重试与“防封”配置的重新定义

可以配置：
- requests_per_minute、max_concurrency、min_interval_ms
- request_timeout_ms、navigation_timeout_ms、action_timeout_ms
- max_retries、retry_backoff_ms、retryable_errors
- circuit_breaker.failure_threshold、cooldown_seconds
- stop_on_challenge、stop_on_access_denied、disable_provider_on_block
- max_session_age_seconds、require_manual_reauth

不实现：
- 为规避封禁而轮换 IP、账号或设备指纹
- 模拟随机人类行为以骗过反机器人检测
- 自动解验证码、MFA 或绕过登录墙
- 触发封禁后自动换身份继续请求

若服务商返回 429，应遵循 Retry-After（若提供），减少调用并记录额度状态；若返回 403、CAPTCHA 或明确封禁提示，应暂停或禁用 Provider，而非持续重试。

## 8. 流式能力

浏览器 UI 逐步渲染回答，不等于存在稳定的 SSE 接口。建议：
- API Provider：原生支持 SSE 时直接流式转发。
- Browser Provider：默认等待回答完成后以普通响应返回。
- 只有在 UI 增量更新行为稳定、服务允许且测试覆盖时，才提供 best-effort streaming；中途失败不得切换 Provider 并拼接两份回答。
- 记录 streaming_supported / streaming_mode，不对未验证能力作承诺。

## 9. 测试与验收阶段

### B1：框架
- [ ] Playwright 依赖、BrowserRuntime、SiteManifest 和 ProviderRegistry。
- [ ] 默认关闭 Browser Provider，启动时不访问第三方网站。
- [ ] 使用本地 fixture 页面测试输入、提交、等待、提取与错误映射。
- [ ] 对登录过期、挑战页面、403/429、超时和页面结构变化有单元/集成测试。
- [ ] 认证状态目录在 .gitignore 中，配置示例不含真实凭证。

### B2：现有网关集成
- [ ] Browser Provider 接入现有路由，保留 API Provider 与 Mock。
- [ ] 请求与站点 allowlist、enabled、automation_authorized 同时校验。
- [ ] 站点级并发、限速、熔断和暂停策略生效。
- [ ] 普通响应成功；流式仅在能力被明确验证后开启。

### B3：单站点验证
- [ ] 选择一个明确允许自动化或提供授权测试环境的站点。
- [ ] 记录来源、权限依据、账号前提、成功/失败证据与维护成本。
- [ ] 若没有符合条件的真实站点，则以本地 fixture 验收框架，真实站点留待授权后验证。

## 10. 官方参考

- Playwright Authentication： https://playwright.dev/docs/auth
- Playwright Network： https://playwright.dev/docs/network
- Playwright BrowserContext： https://playwright.dev/docs/api/class-browsercontext
- OpenAI API rate limits： https://developers.openai.com/api/docs/guides/rate-limits

## 11. 当前状态

本文已确定建议架构与实施边界。除现有 Mock / 本地 fixture 能力外，本文所列 BrowserRuntime、SiteManifest、AuthManager 和 Browser Provider 均不应被描述为已经实现；后续按 B1→B2→B3 逐步实现和验证。


## 12. 第一阶段实现进度（2026-10-20）

已实现：
- 可选 Playwright BrowserUIProvider，默认关闭，需同时显式启用并授权。
- 支持单站点环境变量配置，以及本地 JSON 多站点配置；每个站点拥有独立 provider ID、域名 allowlist、选择器、会话状态路径、超时、并发和速率配置。
- 通过可见浏览器手动登录并保存 storage state 的辅助脚本。
- 按请求 user 字段隔离对话页面和会话状态；同一对话需每轮使用相同 user 值，不同对话使用不同值。
- 访问外部站点要求 HTTPS 和精确域名 allowlist；挑战/访问限制触发暂停，不做自动绕过。
- 真实浏览器已在本机对本地自建 HTML fixture 执行两轮对话测试，验证页面状态可跨轮保留。

尚未实现或验证：
- 尚未验证任何真实第三方 AI 网站；需先确认具体站点的自动化许可。
- 尚未为每个站点实现专用页面适配器；目前通过 manifest 中的选择器配置通用适配器。
- Browser UI 的流式输出仍明确不支持。
- 生产级多租户凭证隔离、会话清理、审计和管理员控制台尚未实现；当前定位是本地/自用 Gateway 的可选扩展，不应直接暴露到公网。
