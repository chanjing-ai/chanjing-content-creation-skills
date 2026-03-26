---
name: orchestration-contract
description: >-
  L3 跨场景编排契约：协作顺序、渐进路由、outcome_code 与回退；不含具体产品 API 字段细则。
  执行各 scripts 前的网络/凭据/二进制/环境变量等共同前提见包根 ../SKILL.md「运行时契约」。
---

# 编排契约（`CONTRACT_SKILL.md`）

本文件服务于 **L3 编排层** 下各业务场景的共用约定：组合或路由多个 `products/` 能力时，遵守同一套**协作顺序、追问粒度、状态与回退**。  
各场景以 **`{场景目录名}_SKILL.md`** 为编排入口；**不**替代各 **`products/<名>/<名>_SKILL.md`** 中的字段、脚本路径与返回结构。

**入口索引**：[包根 `SKILL.md`](../SKILL.md) · 仓库结构约束见 [`rule.md`](../../../rule.md)

---

## 标准工作流（编排骨架）

1. **鉴权**：凡调蝉镜 API，先按 [`chanjing-credentials-guard_SKILL.md`](../products/chanjing-credentials-guard/chanjing-credentials-guard_SKILL.md) 校验/引导。
2. **定目标**：用包入口路由表 + 下文「冲突时」「渐进路由」确定 **L2** 或 **L3**；跨产品场景打开 **`orchestration/<scene>/<scene>_SKILL.md`**。
3. **补参**：在目标 **`…_SKILL.md`** 内收集 `required`（模糊时最多 **1～2** 个关键追问）。
4. **执行**：严格按手册中的命令或 **`scripts/cli_capabilities.py`** 所指脚本执行（路径形如 `…/products/<product>/scripts/…` 或 `…/orchestration/<scene>/scripts/…`）。**执行前**须已阅读包根 **[`SKILL.md`](../SKILL.md)「运行时契约」**：蝉镜 HTTPS、**`~/.chanjing/credentials.json`**（或 `CHANJING_CONFIG_DIR`）读写、CDN 下载、**`ffmpeg`/`ffprobe`**（成片类）、可能的浏览器引导等。  
   **通用性**：列表、鉴权、成片等能力与包内 CLI **一一对应**；编排 Agent **不得**为「再调一次同类 Open API」临时写平行脚本，应组合已有参数（如 `list_figures --tag-ids`、`list_tag_dict`）替代。  
   **持久化**：凭据与 Token 会写回配置文件；成片会写 **`final_one_click.mp4`**、**`workflow_result.json`**、**`work/`** 等——均属用户可通过路径与环境变量**预期并控制**的变更；**不**改写其它技能或全局 Agent 配置（详见 **`SKILL.md`「持久性变更范围与用户可控性」**）。
5. **归一输出**：交付 `task_id` / `url` / 本地路径 / 下一步建议；失败附带 **`outcome_code`**（见下节）。
6. **回退**：同产品内重试 → 仍失败则说明原因；**不得**自动切换产品，降级须**用户确认**。

---

## 冲突时怎么选

1. 「完整成片」→ **一键成片** [`chanjing-one-click-video-creation_SKILL.md`](chanjing-one-click-video-creation/chanjing-one-click-video-creation_SKILL.md)。
2. 「只要数字人口播视频」→ `chanjing-video-compose`。
3. 「已有真人视频只改口型」→ `chanjing-avatar`。
4. 「人设图 + 后续口播」→ `chanjing-text-to-digital-person`。
5. 仍不清 → 渐进路由 + 包入口路由表。

---

## `outcome_code`（摘要）

| 代码 | 含义 | 建议 |
|------|------|------|
| `ok` | 成功 | 交付结果 |
| `need_param` | 缺参 | 按 `_SKILL.md` 追问 |
| `auth_required` | 未鉴权 | 走 credentials-guard |
| `upstream_error` | 上游 API 失败 | 展示 `msg`，可重试 |
| `timeout` | 超时 | 说明可 `poll_task` 或稍后查 |

（各产品线可在自身 `_SKILL.md` 中扩展子状态；**以该产品手册为准**。）

---

## 渐进路由（用户说不清时）

1. 是否要**一条成片**（含口播 + 画面）？是 → L3 一键场景。  
2. 是否只要**数字人对着念**？是 → `chanjing-video-compose`。  
3. 是否**改已有视频的口型**？是 → `chanjing-avatar`。  
4. 否则按路由表关键词落到最近 L2。

---

## 编排文档红线

- 在 `orchestration/**/*.md` 中**不**实现蝉镜 HTTP、不内嵌与产品无关的可执行脚本逻辑。  
- **可执行命令**出现在各产品或场景的 **`scripts/`**（含 `cli_capabilities.py`）及产品 **`…_SKILL.md`** 中。
