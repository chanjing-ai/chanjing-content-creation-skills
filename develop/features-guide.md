# 功能引导

本文帮助开发者快速定位「该打开哪份手册、跑哪个脚本」。

---

## 1. 全局入口

| 资源 | 路径 | 说明 |
|------|------|------|
| 包路由与运行时契约 | [`skills/chanjing-content-creation-skill/SKILL.md`](../skills/chanjing-content-creation-skill/SKILL.md) | Agent/人类第一站：环境变量、凭据、ffmpeg、落盘等 |
| 编排总览 | [`skills/chanjing-content-creation-skill/orchestration/README.md`](../skills/chanjing-content-creation-skill/orchestration/README.md) | L3 列表与契约指针 |
| 跨场景契约 | [`skills/chanjing-content-creation-skill/orchestration/CONTRACT_SKILL.md`](../skills/chanjing-content-creation-skill/orchestration/CONTRACT_SKILL.md) | 执行顺序与契约引用 |

---

## 2. L2 产品索引（`products/`）

| 产品目录 | 手册 | 典型能力 |
|----------|------|----------|
| `chanjing-credentials-guard` | `chanjing-credentials-guard_SKILL.md` | 登录引导、配置 AK/SK、查看状态、`chanjing-get-token` |
| `chanjing-tts` | `chanjing-tts_SKILL.md` | 音色列表、合成、轮询 |
| `chanjing-tts-voice-clone` | `chanjing-tts-voice-clone_SKILL.md` | 克隆音色、合成 |
| `chanjing-avatar` | `chanjing-avatar_SKILL.md` | 口型/数字人视频任务 |
| `chanjing-video-compose` | `chanjing-video-compose_SKILL.md` | 数字人视频合成、上传、轮询、下载 |
| `chanjing-customised-person` | `chanjing-customised-person_SKILL.md` | 定制数字人创建/查询/删除 |
| `chanjing-text-to-digital-person` | `chanjing-text-to-digital-person_SKILL.md` | 文生形象、动作/LoRA 等 |
| `chanjing-ai-creation` | `chanjing-ai-creation_SKILL.md` | 通用 AI 创作提交/列表/详情/下载 |

每个产品下 **`scripts/cli_capabilities.py`** 提供机器可读 `list()` / `config()` / `usage()`；具体命令以各 `_SKILL.md` 与 `--help` 为准。

---

## 3. L3 编排场景

| 场景目录 | 手册 | 说明 |
|----------|------|------|
| `chanjing-one-click-video-creation` | `chanjing-one-click-video-creation_SKILL.md` | 选题或 `workflow.json` → TTS + 数字人 + AI 镜 + 本地 ffmpeg 成片 |

核心脚本：

- `scripts/run_render.py`：主编排入口（`--input` workflow、`--output-dir`）。  
- `scripts/cli_capabilities.py`：能力目录；`run_render()` 通过 `run_skill_script` 子进程调用 `run_render.py`。  
- `scripts/validate_ai_resolution.py`：分辨率等校验。  
- `examples/workflow-contract.md`：字段契约（实现真源与 `run_render` 对齐）。

---

## 4. 凭证与配置（开发自测）

1. 使用 guard 产品脚本配置 `~/.chanjing/credentials.json`（或 `CHANJING_CONFIG_DIR`）。  
2. 需要定位仓库根时，非标准布局可设 **`CHAN_SKILLS_DIR`**（一键成片等脚本依赖）。  
3. 详见包根 `SKILL.md`「运行时契约」表。

---

## 5. 仓库其它目录

| 路径 | 用途 |
|------|------|
| `docs/` | 使用者速用与最佳实践，入口 [`docs/README.md`](../docs/README.md)（与 L2/L3 目录对齐）；**不**替代 `_SKILL.md` 路由 |
| `develop/` | 本开发手册 |
| `outputs/` | 本地运行默认产物目录之一（勿提交密钥与大型媒体） |
