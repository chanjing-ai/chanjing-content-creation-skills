# `chanjing-one-click-video-creation` 速用版（一键成片）

**层级**：L3 编排 · `skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/`  
**手册**：[chanjing-one-click-video-creation_SKILL.md](../skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation_SKILL.md)  
**长文与速查**：[README.md](../skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/README.md)、[`templates/`](../skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/templates/)  
**主编排脚本**：[scripts/run_render.py](../skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/scripts/run_render.py)（`--input` workflow JSON，`--output-dir` 输出目录）  
**字段契约**：[examples/workflow-contract.md](../skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/examples/workflow-contract.md)

**前置**：有效蝉镜凭据（见 [`chanjing-credentials-guard`](./chanjing-credentials-guard-best-practice.md)）；本机需 **ffmpeg / ffprobe**。非标准仓库布局时可设环境变量 **`CHAN_SKILLS_DIR`** 指向仓库根目录（详见包根 `SKILL.md`「运行时契约」）。

**与相近能力区分**：一键成片是「多镜编排 + 本地拼接一条 mp4」。若只要**单条数字人口播**，用 [`chanjing-video-compose`](./chanjing-video-compose-best-practice.md)；若只生成**无编排的 AI 视频片段**，用 [`chanjing-ai-creation`](./chanjing-ai-creation-best-practice.md)。

---

## 什么时候用

- 想要**一条完整短视频**：口播文案 + 部分镜用数字人、部分镜用 AI 画面，最后合成一个文件
- 你已经想好选题和分镜结构，或愿意让 Agent 按模板写出 `workflow.json`
- 能接受在本地指定目录产出 **`final_one_click.mp4`** 及 `work/` 中间文件

## 直接怎么说

- 「我想做一键成片：选题是【xxx】，竖屏口播风，5 个分镜，先给我一版 workflow 再渲染。」
- 「我已有口播全文和分镜意图，请按契约生成 `workflow.json` 并调用 `run_render` 输出到 `outputs/某任务名/`。」
- 「和上次一样一键成片，但换成【新选题】，数字人继续用上次那个形象。」

## 跟 OpenClaw 这样说，更容易触发

- 直接说「一键成片」「完整短视频编排」「workflow 成片」「run_render」。
- 说明是「只要选题」还是「已有 `full_script` / `scenes`」。
- 若有首选数字人与音色，可说「按 list_figures / list_voices 选与口播气质一致的」。

高概率说法：

- 「请按一键成片流程：选题【xxx】，先对齐 `workflow-contract.md`，再跑 `run_render.py`。」
- 「帮我从选题写到可执行的 `workflow.json`，并指定 `output-dir` 落盘。」

## 不要这么说

「帮我做个视频。」（未区分单能力还是整条流水线。）

## 这么说更好

「我要一键成片：竖屏、面向【人群】、风格【描述】。请先写分镜与口播，保证各镜 `voiceover` 拼接等于 `full_script`，首条数字人分镜口播不超过 20 字；再选 `person_id`/`audio_man` 并执行 `run_render.py --input ... --output-dir ...。」
