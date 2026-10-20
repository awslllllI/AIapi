# Duck.ai BrowserUIProvider 诊断报告

日期：2026-10-20  
范围：`gateway/app/providers/browser_ui.py`、站点策略、只读页面探针、本地替代 fixture

## 结论（先说清楚）

**未能完成一次真实 Duck.ai 端到端对话。**  
根因是 **服务条款明确禁止 automated querying**，不是 Playwright 装不上、也不是页面打不开。

只读探针显示：`https://duck.ai/` 返回 HTTP 200，存在可见 `textarea`，未命中 captcha/access denied 文案。因此失败阶段应归类为 **访问策略限制（policy）**，而不是导航失败或反爬挑战页。

## 证据

### 1. 政策（决定性）

Duck.ai Privacy Policy and Terms of Use（https://duckduckgo.com/duckai/privacy-terms）写明，禁止：

> Interfering with or negatively impacting Duck.ai … including circumventing rate limits, safeguards, or other restrictions, **or automated querying and developing or offering AI services**, such as training an AI model.

因此本仓库不会对真实 Duck.ai 执行填词、发送、抽取回答。

### 2. 只读页面探针（非对话）

命令：

```powershell
.\.venv\Scripts\python.exe gateway\scripts\diagnose_duckai_readonly.py
```

结果摘要（完整 JSON：`docs/diagnostics/duckai-readonly-probe.json`）：

| 项 | 结果 |
| --- | --- |
| final_url | `https://duck.ai/` |
| status | 200 |
| challenge_markers | 无 |
| textarea | count=1, visible |
| UI 信号 | 存在 Cancel / Tools / Fast；正文含同意 Privacy Policy and Terms 的 Ask 提示 |

说明：页面可加载；若无视条款强行自动化，下一风险点更可能是 **同意/欢迎层与选择器不稳定**，而不是首屏 access denied。本仓库仍拒绝继续提交 Prompt。

### 3. 官方 API 替代？

Duck.ai **没有**官方「把网页聊天当 API 后端」的文档接口。  
DuckDuckGo Instant Answer API 不是聊天补全接口，不能作为 Duck.ai 对话替代。

## 本轮代码改动

| 文件 | 作用 |
| --- | --- |
| `gateway/app/providers/browser_site_policy.py` | Duck.ai 主机/路径硬拒绝 |
| `gateway/app/providers/browser_ui.py` | 策略检查、分阶段错误、dismiss 选择器、脱敏日志 |
| `gateway/app/router.py` | 读取 `selectors.dismiss` |
| `gateway/fixtures/duck_ui_fixture_server.py` | **本地** Duck 风格 UI 替代路径 |
| `gateway/scripts/diagnose_duckai_readonly.py` | 只读诊断（不提交 Prompt） |
| `gateway/browser-sites.json` / `.example.json` | 增加禁用的 `duck_ai` 条目；保留 `rok_guest` |
| `gateway/tests/test_browser_ui_provider.py` | 策略、阶段分类、本地 fixture、ROK 共存回归 |
| `docs/diagnostics/*` | 探针结果与本报告 |

## 验收含义

- Duck.ai 真实对话：**未成功**（政策禁止，未伪报）。
- 诊断可复现：启用 `duck_ai` 会得到 `stage=policy` 的 `ProviderError`。
- 兼容替代：本地 `duck_ui_fixture` 可完成完整浏览器对话链路验证。
- ROK 站点配置与既有 fixture 测试应保持独立、不受 Duck 策略影响。

## 剩余可行方案

1. 需要真实模型能力时：改接官方 OpenAI 兼容 API（硅基/智谱/OpenRouter 等），不要自动化 Duck.ai。
2. 需要验证 BrowserUIProvider 管线：使用本地 fixture / 已获授权站点（如你方 ROK）。
3. 若 Duck.ai 未来提供官方 API 或书面授权自动化：再单独评估接入，并更新 `browser_site_policy.py`。
