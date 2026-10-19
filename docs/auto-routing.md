# `auto` 路由评估与排序（2026-10-19）

原则：**周期额度 > 同档性能 > 定额（价=0）**

## 性能粗排（本池相对）

| 档位 | 模型 | 类型 | 相对性能 | 本机实测 |
| --- | --- | --- | --- | --- |
| A | 魔搭 `Qwen/Qwen3.8-27B` | 日额度 | 最强（约 LiveCodeBench ~90） | 200 OK |
| A- | 魔搭 `Qwen/Qwen3.5-27B` | 日额度 | 强（约 ~80） | 200 OK |
| B | Gemini `gemini-2.0-flash` | 日额度 | 强，多模态好 | 国内常超时 |
| C | OpenRouter `:free` | 日 50 次 | 不稳定（路由抽签） | 200 但质量差 |
| C | Groq `gpt-oss-20b` | 日额度 | 中上、很快 | 无 Key / 难登录 |
| B | 智谱 `glm-4.7-flash` | 定额价=0 | 中上（~30B 免费档） | 高峰 429 |
| C | 硅基 `Qwen3.5-9B` | 定额价=0 | 中（LCB ~65） | 200 OK |
| D | 硅基 `Qwen2.5-7B` | 定额价=0 | 弱 | 200 OK |

## 当前 `auto` 顺序

1. 魔搭 Qwen3.8-27B  
2. 魔搭 Qwen3.5-27B  
3. Gemini 2.0 Flash  
4. OpenRouter free  
5. Groq gpt-oss-20b  
6. 智谱 glm-4.7-flash  
7. 硅基 Qwen3.5-9B  
8. 硅基 Qwen2.5-7B  
