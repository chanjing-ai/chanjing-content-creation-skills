---
name: chanjing-video-compose
description: Use Chanjing video synthesis APIs to create digital human videos from text or audio, with optional background upload, task polling, and explicit download when the user asks to save the result locally.
---

# Chanjing Video Compose

## L2 Product Skill

本文件是 **L2 产品层**主手册（**Agent 执行真值**）。

- **本文件（`chanjing-video-compose_SKILL.md`）**：业务逻辑、追问与异常语义；据此调度 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py) 与 [`scripts/`](scripts/) 下脚本。
- **顶层入口** [`../../SKILL.md`](../../SKILL.md)：仅负责路由到本目录，**不**承载本产品执行细则。
- **跨场景契约** [`../../orchestration/CONTRACT_SKILL.md`](../../orchestration/CONTRACT_SKILL.md)；L3 编排层说明见 [`../../orchestration/README.md`](../../orchestration/README.md)。

## When to Use This Skill

当用户要做这些事时使用本 Skill：

* 创建数字人视频合成任务
* 用文本驱动数字人出镜
* 用本地音频驱动数字人视频
* 查询公共数字人或定制数字人形象
* 轮询视频合成结果
* 在用户明确要求时下载最终视频到本地

如果需求更接近“上传一段真人视频做对口型驱动”，优先使用 `chanjing-avatar`，不要混用。

## Preconditions

执行本 Skill 前，必须先通过 `chanjing-credentials-guard` 完成 AK/SK 与 Token 校验。

本 Skill 与 guard 共用：

* `~/.chanjing/credentials.json`
* `https://open-api.chanjing.cc`

无凭证时，脚本会自动打开蝉镜登录页，并提示配置命令。

## Standard Workflow

1. 先让用户明确选择数字人来源：`common`（公共数字人）或 `customised`（定制数字人）
2. **公共数字人（推荐更精准路径）**：先 `list_tag_dict --business-type 1 --json`（或人类可读默认输出）查看大类与子标签；大类含 **`name` / `business_type` / `weight` / `update_time` / `tag_list`**，子标签含 **`id` / `name` / `parent_id` / `level` / `weight`** 等。按选题从字典选出子标签 `id`，再 `list_figures --source common --tag-ids <逗号分隔> --fetch-all --page-size 80 --json` 在**服务端已 AND 过滤**的候选集上全局择优。**须全量覆盖当前筛选条件下的 `total_count`**（`--fetch-all`），禁止只看第一页。
3. **无标签筛选时**：仍调用 `list_figures --source common --fetch-all --page-size 80 --json`（或等价翻页直至 `total_count` 全部覆盖）。**禁止**在未合并全库前仅从第一页或前几页挑人。**禁止**未做全局比较就默认接口返回顺序最前几项。
4. **全局匹配与择优**：在**完整合并后的列表**上，结合当次 **`video_plan` / 选题 / 口播人设 / 场景气质**（年龄、职业感、国风/商务/教育等 `tag_names`，以及 `name`、`audio_name` 语义），对**每一条**人物及其 `figures[]` 做相关性评估；先筛出与场景**较相符的一批候选项**（通常 3～8 个），再在其中比较 **`figures[].width`/`height`**（竖屏成片优先与目标 9:16 一致）、`audio_man_id` 与后续 TTS 音色是否一致，最终选定 **`person_id` + `figure_type`**。一键成片等混剪场景还须考虑与 AI 分镜画幅一致，参见编排层 `render_rules.md` / `validate_ai_resolution.py`。
5. 定制数字人（`customised`）同样推荐 **`--fetch-all`** 或足够大的 `--max-pages`，避免漏人；选型逻辑与上类似，在**全量候选**上匹配场景。
6. 公共数字人须确认 `figure_type` 与所选 `figures[].type` 一致（如 `sit_body` / `whole_body` / `circle_view`）。**无用户特殊要求时默认偏好偏年轻、有活力**（名称/`audio_name` 体现青年、元气、学生等）；**仅当**选题、口播或 `video_plan.tone` 明确要求成熟、权威、中老年、历史叙事等气质时，再优先匹配对应标签与音色。
7. 若使用文本驱动，确定 `audio_man_id`
8. 在创建任务前，必须明确询问用户字幕偏好：`show`（保留字幕）或 `hide`（隐藏字幕）
9. 如果用户选择 `show` 但没有提出自定义样式或位置需求，直接使用官方文档推荐默认值；只有在用户明确想调整字幕位置或样式时，才继续追问 `subtitle_config` 参数
10. 若用户要定制字幕位置，说明坐标以左上角为原点，再补充 `subtitle_config` 相关参数
11. 若使用本地音频或背景图，先调用 `upload_file` 获取 `file_id`
12. 调用 `create_task` 创建视频合成任务，得到 `video_id`
13. 调用 `poll_task` 轮询直到成功，得到 `video_url`
14. 只有在用户明确要求保存到本地时，才调用 `download_result`

## Covered APIs

本 Skill 当前覆盖：

* `GET /open/v1/list_common_dp`
* `GET /open/v1/common/tag_list`
* `POST /open/v1/list_customised_person`
* `POST /open/v1/create_video`
* `GET /open/v1/video`
* `GET /open/v1/common/create_upload_url`
* `GET /open/v1/common/file_detail`

## Scripts

脚本目录：

* `skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/`

| 脚本 | 说明 |
|------|------|
| `_auth.py` | 读取凭证、获取或刷新 `access_token` |
| `list_tag_dict` | `GET /open/v1/common/tag_list`：业务大类（`name`/`business_type`/`weight`/`update_time`/`tag_list`）与子标签（`id`/`parent_id`/`level`/`weight` 等）；`--business-type 1` 常见为数字人；`--json` 完整输出 |
| `list_figures` | 按 `--source common|customised` 列出数字人；公共库可选 **`--tag-ids`**（AND）、**`--common-dp-source`**；**`--fetch-all`** 拉全量至当前条件下的 `total_count`；或 `--max-pages` 多页合并；建议 `--json` 与较大 `--page-size` |
| `upload_file` | 上传音频或背景素材，轮询到文件可用后输出 `file_id` |
| `create_task` | 创建视频合成任务；使用公共数字人时可补充 `--figure-type ...`，字幕支持 `--subtitle show|hide` 以及完整字幕配置参数 |
| `poll_task` | 轮询视频详情直到完成，默认输出 `video_url` |
| `download_result` | 下载最终视频到 `outputs/video-compose/` |

## Usage Examples

示例 1：公共数字人文本驱动

```bash
# 1. 先拉全量公共数字人，再在完整列表上做全局匹配选型（勿只用第一页）
python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/list_figures --source common --fetch-all --page-size 80 --json

# 2. 用公共数字人创建文本驱动视频
VIDEO_ID=$(python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/create_task \
  --person-id "C-ef91f3a6db3144ffb5d6c581ff13c7ec" \
  --figure-type "sit_body" \
  --audio-man "C-0ae461135d8a4eb2b59c853162ea9848" \
  --subtitle "show" \
  --subtitle-x 31 \
  --subtitle-y 1521 \
  --subtitle-width 1000 \
  --subtitle-height 200 \
  --subtitle-font-size 64 \
  --subtitle-stroke-width 7 \
  --text "你好，这是一个蝉镜视频合成测试。")

# 3. 轮询到完成，拿到 video_url
python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/poll_task --id "$VIDEO_ID"
```

示例 2：定制数字人上传本地音频驱动

```bash
python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/list_figures --source customised

AUDIO_FILE_ID=$(python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/upload_file \
  --service make_video_audio \
  --file ./input.wav)

VIDEO_ID=$(python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/create_task \
  --person-id "C-ef91f3a6db3144ffb5d6c581ff13c7ec" \
  --subtitle "hide" \
  --audio-file-id "$AUDIO_FILE_ID")

python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/poll_task --id "$VIDEO_ID"
```

示例 3：显式下载最终视频

```bash
python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/download_result \
  --url "https://example.com/output.mp4"
```

## Download Rule

下载是显式动作，不是默认动作：

* `poll_task` 成功后应先返回 `video_url`
* 不要自动下载结果文件
* 只有当用户明确表达“下载到本地”“保存到 outputs”“帮我落盘”时，才执行 `download_result`

## Figure Selection Rule

选择数字人时遵循这条规则：

* 如果用户要用平台已有人物库，先走公共数字人：`list_figures --source common --fetch-all --page-size 80 --json`，在**全量列表**上全局匹配后再写 `person_id` / `figure_type`
* 如果用户要用自己训练或上传生成的人物，先走定制数字人：`list_figures --source customised`
* 使用公共数字人创建视频时，可按所选形态传 `--figure-type <type>`
* 使用定制数字人时，不需要 `figure_type`

## Subtitle Rule

字幕遵循这条规则：

* 不要默认假设用户要字幕或不要字幕
* 创建任务前，必须先明确询问用户选择：`show` 或 `hide`
* 若由 **`chanjing-one-click-video-creation`** 的 **`run_render.py`** 调用 `create_task`，以当次 **`workflow.json` 根级 `subtitle_required`** 为准（**默认 false** → `--subtitle hide`；**true** → `show` 及推荐样式），**无需**为该一键成片路径再单独追问字幕开关，除非用户在需求里明确要求改字幕策略
* 用户选择保留字幕时，调用 `create_task --subtitle show`
* 若用户未指定字幕位置或样式，直接使用官方推荐默认值；`create_task` 在未传 `--subtitle-color` 时默认白字 `color=#FFFFFF`：1080p 为 `x=31 y=1521 width=1000 height=200 font_size=64 stroke_width=7 asr_type=0`；4K 画布为 `x=80 y=2840 width=2000 height=1000 font_size=150 stroke_width=7 asr_type=0`（两组均含 `color=#FFFFFF`）
* 用户选择隐藏字幕时，调用 `create_task --subtitle hide` 或兼容旧用法 `--hide-subtitle`
* 若用户要求调整字幕位置或样式，可继续传 `--subtitle-x` / `--subtitle-y` / `--subtitle-width` / `--subtitle-height` / `--subtitle-font-size` / `--subtitle-color` / `--subtitle-stroke-color` / `--subtitle-stroke-width` / `--subtitle-font-id` / `--subtitle-asr-type`
* 坐标基于左上角原点；字幕区域不能超出 `screen_width` / `screen_height`
* 如果用户只说“要字幕”但没指定位置，不必再追问具体数值；除非用户明确要调位置，否则直接走默认值

## Output Convention

默认本地输出目录：

* `outputs/video-compose/`

## Additional Resources

更多接口细节见：

* `skills/chanjing-content-creation-skill/products/chanjing-video-compose/reference.md`
* `skills/chanjing-content-creation-skill/products/chanjing-video-compose/examples.md`
