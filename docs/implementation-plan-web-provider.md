# Web Provider Demo 后续实施计划

> 项目：D:\Project\ai-api
> 创建日期：2026-10-20
> 目的：对照用户的 Web AI 聚合中转站需求，先记录差距与执行顺序，再进行代码修改。本文是实施计划，不代表下列工作已完成。

## 1. 当前基线（根据仓库现有文档，尚待独立复验）

- 已有 Web AI 限制调研、候选服务表、Provider Demo 使用说明和验证记录。
- 已新增 gateway：Mock、自建 Demo Web fixture、OpenAI 兼容 Provider、路由、限流、熔断、指标和测试。
- 现有验证记录声称 `pytest gateway/tests -q` 为 14 passed；必须在当前工作树重新运行，不直接把历史记录视为当前结果。
- 第三方消费者 Web UI 自动化接入并未实现；本项目不会绕过登录、验证码、访问控制或自动化限制。
- 现有文档称 LiteLLM→Gateway Docker 联调尚未验证。

## 2. 实施原则

1. 不提交 Git、不重置、不覆盖用户已有未提交修改。
2. 先保存本计划，再检查实际源码、Git 差异、配置和测试。
3. 区分代码存在、自动化测试通过、真实上游调用成功三种证据。
4. 真实 Provider 只使用官方 API、公开文档接口或明确授权的自动化入口；无授权时使用清晰标注的 Mock / 自建 fixture。
5. 不将未公开额度写成保证值；未知配额明确记录为 unknown。
6. 尽量复用现有 LiteLLM，不破坏既有端口、模型名、配置和 API 兼容性。

## 3. 执行阶段

### 阶段 A：基线审查
- 检查 `git status`、`git diff`、新增文件清单；保护所有现有改动。
- 阅读 Provider 接口、各 Provider、路由、配置、限流、熔断、指标和测试源码。
- 运行现有测试，记录实际结果和失败。
- 检查 README、调研文档与实现是否一致，检查敏感配置是否被纳入跟踪。

### 阶段 B：修复最小可运行网关
- 验证模型列表、OpenAI 兼容普通请求、SSE 流式输出、错误标准化。
- 验证 Provider 路由、超时、限流、退避重试、熔断和 failover；区分可重试错误与不可重试错误。
- 确认并发限制及速率限制为可配置项，避免把重试用于规避上游限制。
- 确认无真实上游密钥时仍能使用 Mock / 本地 fixture 完成端到端测试。
- 修复实际发现的缺陷，并为每个修复增加回归测试。

### 阶段 C：真实上游与现有服务集成
- 检查 OpenAI-compatible Provider 的配置、认证、超时、错误映射和流式转发。
- 在存在有效且获准使用的 Key 时执行可选真实上游验证；没有 Key 时明确标记未验证，不伪造成功记录。
- 检查 LiteLLM 配置是否能安全地选择 Gateway Provider；验证 Docker 到宿主机的地址、认证和路由。
- 不改变原有默认路由；新增集成应可通过配置启用/关闭。

### 阶段 D：调研与交付文档
- 检查 Web AI 候选清单是否给每个关键结论提供官方来源链接，并区分官方事实、社区报告和推断。
- 将免登录服务纳入调研，但只有官方 API 或明确授权接口才能作为程序化 Provider。
- 更新文件清单、实际命令、测试结果、完整请求链路、失败证据和复现步骤。
- 将能力分为“已验证 / 仅实现未验证 / 尚未实现 / 因访问规则不验证”。

## 4. 验收标准

- [x] 实施前计划已保存。
- [x] 现有测试在当前工作树重新运行，实际结果已记录（18 passed）。
- [x] Mock 普通请求、流式请求、模型列表、限流、上游错误、超时和 failover 有自动化测试。
- [x] 自建 Web fixture 端到端调用有可复现证据。
- [ ] 可选真实 Provider 的结果只在实际请求成功时标为成功。
- [x] 已用隔离 LiteLLM Docker 测试容器验证到 Gateway 的普通/流式转发；既有运行容器与默认配置未被修改。正式启用仍需用户显式配置。
- [ ] 文档没有把 Web 免费使用误写成允许程序化调用。
- [ ] 未提交用户改动未被丢弃，未把密钥写入源码或提交记录。

## 5. 本次执行记录

- 以上为计划建立时的预期阶段；实际执行进展与未完成项以第 6 节为准。
- 当前整体状态：部分完成；真实外部 Provider 本轮验证与候选政策逐条复核仍待完成。


## 6. 本轮执行结果（2026-10-20）

- [x] 已在修改代码前保存本实施计划。
- [x] 重新运行原有测试基线：14 passed（4.99s）。
- [x] 发现并修复流式 failover 缺陷：首个 chunk 已发送后若上游报错，旧实现会捕获异常并切到备用 Provider，可能把两份回答拼在一起。现在只允许首包发出前 failover；首包发出后错误会向调用方传播，不重放备用流。
- [x] 增加回归测试，覆盖流式中途失败不 failover、超时 failover、上游 429 failover，以及未配置网关密钥时 fail closed。
- [x] 修复安全默认值：`GATEWAY_MASTER_KEY` 默认留空；未配置时受保护 API 返回 503，而不是跳过鉴权。
- [x] 更新后测试：18 passed（7.03s）。
- [x] `git diff --check` 通过；`python -m compileall -q gateway` 通过。
- [x] 实际启动本地 fixture 与 Gateway HTTP 服务完成冒烟验证：
  - `GET /v1/models`：200，列出 5 个模型。
  - 非流式 `POST /v1/chat/completions`：200，provider=`demo_web`，返回包含 `http-live-check` 的回复。
  - 流式请求：收到 SSE 数据块并正常结束于 `[DONE]`。
- [x] 使用隔离 LiteLLM Docker 容器完成 Gateway 普通与流式转发；原有容器及配置未修改。
- [ ] 当前没有重新执行真实外部 API Key 验证；此前文档里的硅基/智谱/魔搭结果仍是历史记录，不算本轮实时验证。
- [ ] 候选服务调研的每个政策细节与官方链接尚未逐条重新核验。

### 本轮新增/修改

- 修改：`gateway/app/router.py`
- 修改：`gateway/tests/test_router_failover.py`
- 新增：`docs/implementation-plan-web-provider.md`

状态：Demo 的核心链路与回归测试有了当前工作树的证据，但整体任务仍为“部分完成”，不能声称真实 WebChat2API 已接通，也不能声称 LiteLLM Docker 集成与全部政策调研已完成。


## 7. Browser UI Provider ???2026-10-20?

- ????????`docs/browser-provider-architecture.md`?
- ????? `BrowserUIProvider`??? Playwright ????????????????????????????????????? `BROWSER_AUTOMATION_AUTHORIZED=true`?
- ????? allowlist???? HTTPS ?????????RPM/min interval?????????????????????
- Browser UI ??????????????/?????????????????????????
- ?????? Provider ????????? fixture ???????????? Chromium ????????????????
- ???????????????????????????????? fixture ????????????????


### Browser UI Provider 本轮验证补充

- [x] Playwright 与 Chromium 已安装到本机项目虚拟环境/浏览器缓存。
- [x] 多站点 JSON manifest 可加载为独立 Provider，默认禁用；每站点使用独立会话状态路径。
- [x] 可见浏览器手动登录脚本已新增，按站点配置保存 storage state。
- [x] 本地 HTML fixture 浏览器自动化测试验证真实 Chromium 页面交互及两轮对话页面状态保留。
- [x] Browser UI Provider 要求请求携带 user 作为稳定的会话 ID，避免多个对话混用同一页面历史。
- [x] 最终完整测试：26 passed in 8.94s；compileall 和 git diff --check 均通过。
- [ ] 真实第三方站点仍未验证；未确认自动化授权前，不应启用对应站点配置。
- [ ] Browser UI 目前不支持流式响应，且不适合未经额外隔离审查就部署到公网多租户环境。
