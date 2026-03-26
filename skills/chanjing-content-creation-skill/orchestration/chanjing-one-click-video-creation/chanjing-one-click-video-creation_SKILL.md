---
name: chanjing-one-click-video-creation
description: >-
  L3 一键成片：组合 TTS、数字人合成、AI 画面与本地 ffmpeg 拼接。
  须有效蝉镜凭据；依赖 ffmpeg/ffprobe；环境变量与持久化路径见包根 ../../SKILL.md「运行时契约」。
---

# 一键成片（`chanjing-one-click-video-creation_SKILL.md`）

## 场景定位

- **业务目标**：用户给选题或完整 `workflow.json`，得到**一条**口播 + 数字人 + AI 画面混剪后的 **mp4 成片**。
- **编排性质**：本文件给出 **跨产品边界** 与 **Agent 执行落点**；**篇首速查、§ 编号、`run_render` 字段与 ffmpeg 细则** 以同目录 [`README.md`](README.md) 与 [`templates/render_rules.md`](templates/render_rules.md) 为长文真源（避免重复维护）。
- **共用契约**：状态码、回退、追问见 [`../CONTRACT_SKILL.md`](../CONTRACT_SKILL.md)。
- **运行时总表**（HTTPS、**`~/.chanjing/credentials.json`**、`CHAN_SKILLS_DIR`、`FIRST_DIGITAL_HUMAN_MAX_CHARS`、`AI_VIDEO_PROMPT_MAX_CHARS`、**ffmpeg/ffprobe** 等）：包根 [`../../SKILL.md`](../../SKILL.md) **「运行时契约」**。

## 涉及产品（L2）

| 能力 | 产品目录 | 说明 |
|------|----------|------|
| 鉴权 | `chanjing-credentials-guard` | 任意蝉镜调用前 |
| TTS / 音频 | `chanjing-tts` | 由 `run_render` 子进程按工作流调用 |
| 数字人视频 | `chanjing-video-compose` | 音频驱动分镜 |
| 文生视频等 | `chanjing-ai-creation` | `ref_prompt` 分镜 |
| **确定性流水线** | 本目录 `scripts/run_render.py` | 编排子脚本 + 本地 ffmpeg |
| 编排侧 token 胶水 | 本目录 `scripts/_auth.py` | 与 L2 `products/*/scripts/_auth.py` 同形；`run_render` 进程内轮询 TTS 时取 `resolve_chanjing_access_token`（实现仍来自包根 `common/base.py`） |

## 编排与执行顺序（Agent）

1. **鉴权**：按 [`CONTRACT_SKILL.md`](../CONTRACT_SKILL.md) 与 [`chanjing-credentials-guard_SKILL.md`](../../products/chanjing-credentials-guard/chanjing-credentials-guard_SKILL.md) 完成凭据。
2. **内容层**（与行业/叙事无关）：按 `templates/` 产出选题、口播、`video_plan`、各镜 `ref_prompt` 等；可写入 JSON 任意**扩展键**供追溯——**仅**当键落在 [`examples/workflow-contract.md`](examples/workflow-contract.md) 表中时才被 `run_render` 消费。**首个数字人分镜**口播 **≤20 字**（默认，可调 `FIRST_DIGITAL_HUMAN_MAX_CHARS`），见 `render_rules.md` §4 与 `storyboard_prompt.md`。
3. **渲染层**：根级与分镜**必填/可选**以 [`examples/workflow-contract.md`](examples/workflow-contract.md) 为准（实现真源 `run_render.py`）。就绪后调用 [`scripts/run_render.py`](scripts/run_render.py)（或 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py)）；**禁止**在会话内重写列表类 API 包装或重复 ffmpeg 编排。
4. **输出**：`final_one_click.mp4`、`workflow_result.json`、`work/`；**`partial` / `fail`** 见 L2 手册与 **`CONTRACT_SKILL.md`**。

## 输入 / 输出（摘要）

| 类型 | 要点 |
|------|------|
| 输入 | `topic` 与 `workflow.json` 二选一（完整规则见 **`README.md`**）；`output_dir`；非标准布局时 `CHAN_SKILLS_DIR` |
| 输出 | `final_one_click.mp4`、`workflow_result.json`、`work/` |

**禁止**：在本文件重复粘贴 **`render_rules.md`** / **`storyboard_prompt.md`** 长条文——一律引用 `templates/` 与 **`README.md`**。

## 文档真源对照

| 主题 | 打开 |
|------|------|
| 速查表、§ 导航、环境、FAQ、Agent 通用模式 | [`README.md`](README.md) |
| **`workflow.json` 字段契约（题材无关）** | [`examples/workflow-contract.md`](examples/workflow-contract.md) |
| TTS / 切段 / ffmpeg / 硬性约束 | [`templates/render_rules.md`](templates/render_rules.md) |
| 分镜与 `ref_prompt` | [`templates/storyboard_prompt.md`](templates/storyboard_prompt.md)、[`templates/history_storyboard_prompt.md`](templates/history_storyboard_prompt.md) |

## 相关入口

- [包入口 `SKILL.md`](../../SKILL.md)
- [编排契约 `CONTRACT_SKILL.md`](../CONTRACT_SKILL.md)
