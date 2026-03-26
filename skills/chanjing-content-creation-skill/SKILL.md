---
name: chanjing-content-creation-skill
always: false
description: >-
  蝉镜内容创作技能包唯一顶层入口：路由与各层 `{名}_SKILL.md` 索引；本文件不写逐步业务算法。
  调用包内 scripts 即触发可执行逻辑：HTTPS 访问蝉镜 API、读写本地凭据文件、CDN 下载、子进程 ffmpeg/ffprobe（成片链路）、部分流程可打开浏览器引导登录。
  always:false 表示本技能不强制随会话默认加载，由用户/宿主按需启用。
  环境变量、二进制、凭据与工件持久化见篇内「运行时契约」。
---

# 蝉镜内容创作技能包（顶层入口）

本包遵循仓库 [`skills/rule.md`](../rule.md)：**§二～五** 约定 `SKILL.md` + `common/` + `products/` + `orchestration/` 为包内**仅有的根级对象**；**§六** 要求含 `scripts/` 的包在根 `SKILL.md` 写明「运行时契约」与注册元数据。**`rule.md` 不含本包业务逻辑**——蝉镜 API、路径、环境变量与成片产物等**真值以本文件与各 `_SKILL.md` 为准**。

**职责边界（须区分）**

- **本 `SKILL.md`**：只做 **路由、层级说明、运行时契约**；**不**写逐步 API 参数、状态码细则或成片算法。
- **`products/*/scripts/` 与 `orchestration/*/scripts/`**：含 **可执行代码**；被 Agent 按各手册调用时，会执行真实 **网络 I/O、本地读写、子进程、（可选）浏览器**。下文 **「运行时契约」** 统一声明这些行为与依赖，避免「入口只写路由」与「实际跑脚本」之间的信息缺口。

| 层级 | 路径 | 职责 |
|------|------|------|
| **顶层入口** | 本 `SKILL.md` | 全局路由、**运行时契约**；**不**承载各产品/场景的逐步业务算法（见各 `_SKILL.md` 与 `scripts/`） |
| **L1 公共基础** | [`common/`](common/) | `base.py`（鉴权、无 token 的 `request_json`、`poll_until`、脚本调度）、`exceptions.py`、`logger.py`；另有共享 **`open_api_client.py`**（带 `access_token` 的 JSON GET/POST）、**`file_upload.py`**（`create_upload_url` / PUT / `file_detail` 轮询）、**`asset_download.py`**（结果 URL 落盘）、**`open_ai_creation.py`** / **`open_aigc_person.py`**（域 API 封装）。**禁止**把产品线专属 CLI 与业务规则写进 common；各 `products/*/scripts/_auth.py` 仍为同目录脚本导入 `resolve_chanjing_access_token` 的薄入口（可选再收敛）。 |
| **L2 产品层** | [`products/`](products/) | 每产品一目录：`{产品目录名}_SKILL.md`（手册）+ [`scripts/`](products/chanjing-tts/scripts/)（含 `cli_capabilities.py` 与各 CLI 脚本） |
| **L3 编排层** | [`orchestration/`](orchestration/) | 每场景一目录：**仅一个** `{场景目录名}_SKILL.md`，描述跨 `products/` 的组合流程；**可**含 `scripts/`（如 `run_render.py`） |

**依赖原则**：自上而下可读；**products** 不依赖 **orchestration**；**common** 不依赖 products/orchestration。

---

## 运行时契约（注册表 / Agent 执行前必读）

以下适用于「按手册调用本包任意 `scripts/` 下脚本」的情形；**具体会触发哪些项取决于所调脚本**（例如仅 `list_voices` 则不需要 `ffmpeg`）。

### 凭据与本地持久化

| 项 | 说明 |
|----|------|
| **配置文件** | 默认 **`~/.chanjing/credentials.json`**（`app_id` / `secret_key` 与刷新后的 **`access_token`** 等）。目录可由环境变量 **`CHANJING_CONFIG_DIR`** 覆盖（文件名为 `credentials.json`）。 |
| **读写行为** | 鉴权与 Token 刷新会 **读取并写回** 该文件（含 `access_token`、`expire_in` 等）；首次配置见 [`chanjing-credentials-guard_SKILL.md`](products/chanjing-credentials-guard/chanjing-credentials-guard_SKILL.md)。 |
| **与 API 的关系** | 各产品脚本向 **`CHANJING_API_BASE`**（默认 `https://open-api.chanjing.cc`）发起 **HTTPS** 请求；**无有效凭据则无法正常调用**（guard 可能引导浏览器打开蝉镜登录/注册页）。 |

### 环境变量（常见）

| 变量 | 必需性 | 默认 / 说明 |
|------|--------|-------------|
| **`CHANJING_API_BASE`** | 可选 | 默认 `https://open-api.chanjing.cc`；自建/代理网关时覆盖。 |
| **`CHANJING_CONFIG_DIR`** | 可选 | 默认 `~/.chanjing`；决定 `credentials.json` 所在目录。 |
| **`CHAN_SKILLS_DIR`** | 视布局而定 | 脚本从路径上溯定位仓库根以解析 `skills/chanjing-content-creation-skill/...`。**整包放在标准 monorepo 布局时通常不必设**；仅拷贝 skill 目录、或根路径不在预期时 **应设为仓库根目录的绝对路径**（一键成片 `run_render.py`、`validate_ai_resolution.py`、部分 CLI 依赖）。 |
| **`FIRST_DIGITAL_HUMAN_MAX_CHARS`** | 可选 | 默认 **`20`**；一键成片 `run_render.py` 校验**首个数字人分镜** `voiceover` 最大字符数。 |
| **`AI_VIDEO_PROMPT_MAX_CHARS`** | 可选 | 默认 **`8000`**；`run_render.py` 中文生视频整段 `ref_prompt` 长度上限（与模板说明一致）。 |

### 外部二进制

| 二进制 | 必需性 | 用途 |
|--------|--------|------|
| **`ffmpeg`** | **一键成片等本地渲染路径必需** | 拼接、转码、封装音视频（`orchestration/.../scripts/run_render.py` 等）。仅调用纯 API、不跑 L3 成片时可不装。 |
| **`ffprobe`** | **同上** | 读取媒体分辨率、时长、旋转元数据等，用于与数字人轨对齐。 |

### 执行脚本时的典型副作用（按类）

| 类型 | 说明 |
|------|------|
| **出站 HTTPS** | 蝉镜 Open API、可能的 CDN **`video_url` / 素材下载**。 |
| **本地文件** | `outputs/`、`work/`、任务落盘、上传前的临时文件等（以各场景 `README` / `run_render` 为准）。 |
| **子进程** | `ffmpeg` / `ffprobe`；部分脚本 `subprocess` 调用同仓库下其它 Python CLI。 |
| **浏览器** | 凭据缺失或引导登录时，可能 **`webbrowser.open`** 或调用 `open_login_page`（见 `common/base.py` 与 credentials-guard）。 |

### 持久性变更范围与用户可控性

以下行为对本包而言是**预期内的副作用**；用户或宿主应知情，并可通过路径/环境变量**控制写入位置**，而非视为「隐式全局污染」。

| 类别 | 写入什么 | 典型位置 | 用户如何控制 |
|------|----------|----------|----------------|
| **凭据状态** | `app_id` / `secret_key`（若经配置脚本写入）、刷新后的 **`access_token`**、`expire_in` 等 | **`CHANJING_CONFIG_DIR/credentials.json`**（默认 `~/.chanjing/credentials.json`） | 设置 **`CHANJING_CONFIG_DIR`** 指向专用目录；或事后删除/迁移该文件；**勿**将秘钥提交版本库。 |
| **一键成片工件** | **`final_one_click.mp4`**、**`workflow_result.json`**、**`work/`**（中间音频、分段视频、concat 列表等） | 由 **`run_render.py --output-dir`** 指定（常见为仓库下某次任务的 `outputs/<任务名>/`） | 选用明确的 **`--output-dir`**；任务结束后按需保留或删除该目录。 |
| **其它下载类脚本** | 合成结果等到本地文件 | 如 `download_result` 默认相对**当前工作目录**下的 **`outputs/<产品线>/`**，或通过 **`--output`** 指定绝对路径 | 在预期 cwd 下执行，或始终传 **`--output`**。 |
| **临时/过程文件** | TTS 合并、切段、上传前缓存等 | 多在上述 **`work/`** 或脚本约定目录内 | 随 **`output_dir` / `work/`** 一并管理。 |

**本包脚本在校验范围内不会**：修改**其它技能**目录、**`.cursor/rules`**、**全局 Agent 配置文件**（如编辑器用户级 `settings.json`）等；仅操作蝉镜凭证路径、调用方指定的输出目录，以及相对 cwd 的默认 `outputs/...`（见各脚本 `--help`）。

---

## 导航与执行：顶层 → `{名}_SKILL.md`

- **路由落点**：本页链接指向各目录下的 **`{产品或场景目录名}_SKILL.md`**。  
- **执行依据**：Agent 打开该文件后，按其业务逻辑调度 **`scripts/cli_capabilities.py`** 与 **`scripts/`** 下其它脚本；**执行前**须已了解上文 **「运行时契约」**（网络、凭据、二进制、环境变量）。  
- **共用契约**：跨场景状态码与追问见 [`orchestration/CONTRACT_SKILL.md`](orchestration/CONTRACT_SKILL.md)。

### 编排与 Agent（通用约定）

适用于 **L3 一键成片** 及未来同类「内容 JSON + 确定性脚本」场景，**不绑定具体选题**：

1. **先读后跑**：打开对应 **`{场景}_SKILL.md`** 与同目录 **`README.md`**；成片输入字段以 [`orchestration/chanjing-one-click-video-creation/examples/workflow-contract.md`](orchestration/chanjing-one-click-video-creation/examples/workflow-contract.md) 与 `run_render.py` 为准。
2. **能力在脚本里**：鉴权、列表（音色/数字人/标签）、成片等 **只调** `products/*/scripts/` 与 `orchestration/*/scripts/` 已有 CLI；**不**为单次任务另写重复 HTTP/列表逻辑。
3. **分层**：策划文案、`video_plan`、`topic` 等与 **`run_render` 消费字段**分开维护；扩展键可保留在 JSON 中，未在契约表列出的键由宿主自行约定含义。

---

## 路由优先级

1. **AK/SK / Token / 登录** → [`products/chanjing-credentials-guard/chanjing-credentials-guard_SKILL.md`](products/chanjing-credentials-guard/chanjing-credentials-guard_SKILL.md)
2. **用户已点名某产品** → `products/<名>/<名>_SKILL.md`
3. **跨产品成片、选题→成片** → [`orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation_SKILL.md`](orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation_SKILL.md)（篇内 § 与速查见同目录 [`README.md`](orchestration/chanjing-one-click-video-creation/README.md)、[`templates/`](orchestration/chanjing-one-click-video-creation/templates/)）
4. **统一状态码、回退、追问** → [`orchestration/CONTRACT_SKILL.md`](orchestration/CONTRACT_SKILL.md)
5. **关键词歧义** → 下表 + `CONTRACT_SKILL.md`

---

## 路由映射表（意图 → 文档）

| 触发条件 / 关键词 | 目标文档 | 最小追问 |
|-------------------|----------|----------|
| 一键成片、完整短视频、口播+混剪、做一个 xxx 短视频 | [`chanjing-one-click-video-creation_SKILL.md`](orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation_SKILL.md) | 仅选题还是已有 `workflow.json` |
| 文字转语音、语音合成、固定音色声音合成、公共音色合成声音 | [`chanjing-tts_SKILL.md`](products/chanjing-tts/chanjing-tts_SKILL.md) | 文本、音色 |
| 声音克隆、音色复刻、声音极速复刻 | [`chanjing-tts-voice-clone_SKILL.md`](products/chanjing-tts-voice-clone/chanjing-tts-voice-clone_SKILL.md) | 参考音频 |
| 对口型、唇形驱动(用户提供视频素材) | [`chanjing-avatar_SKILL.md`](products/chanjing-avatar/chanjing-avatar_SKILL.md) | 视频 / 音频素材 |
| 公共数字人口播、公共数字人、预置形象数字人、一句话合成数字人、声音驱动公共数字人 | [`chanjing-video-compose_SKILL.md`](products/chanjing-video-compose/chanjing-video-compose_SKILL.md) | 公共 / 定制、字幕 |
| 海报、文生图、创意视频 | [`chanjing-ai-creation_SKILL.md`](products/chanjing-ai-creation/chanjing-ai-creation_SKILL.md) | 图 / 视频、模型 |
| 训练定制数字人 | [`chanjing-customised-person_SKILL.md`](products/chanjing-customised-person/chanjing-customised-person_SKILL.md) | 源视频 |
| 人设图、LoRA | [`chanjing-text-to-digital-person_SKILL.md`](products/chanjing-text-to-digital-person/chanjing-text-to-digital-person_SKILL.md) | 仅形象 / 还要视频 |
| 凭据、AK/SK | [`chanjing-credentials-guard_SKILL.md`](products/chanjing-credentials-guard/chanjing-credentials-guard_SKILL.md) | 首次配置 / 检查状态 |

**冲突提示**：完整成片 → L3 一键场景；仅数字人口播 → `chanjing-video-compose`；提供人像视频改口型 → `chanjing-avatar`（细则见 `CONTRACT_SKILL.md`）。

---

## L2 产品清单（`products/`）

| 目录 | 手册 | `scripts/` |
|------|------|------------|
| `chanjing-credentials-guard/` | `chanjing-credentials-guard_SKILL.md` | 含 `cli_capabilities.py` |
| `chanjing-tts/` | `chanjing-tts_SKILL.md` | 含 `cli_capabilities.py` |
| `chanjing-tts-voice-clone/` | `chanjing-tts-voice-clone_SKILL.md` | 含 `cli_capabilities.py` |
| `chanjing-avatar/` | `chanjing-avatar_SKILL.md` | 含 `cli_capabilities.py` |
| `chanjing-video-compose/` | `chanjing-video-compose_SKILL.md` | 含 `cli_capabilities.py` |
| `chanjing-ai-creation/` | `chanjing-ai-creation_SKILL.md` | 含 `cli_capabilities.py` |
| `chanjing-customised-person/` | `chanjing-customised-person_SKILL.md` | 含 `cli_capabilities.py` |
| `chanjing-text-to-digital-person/` | `chanjing-text-to-digital-person_SKILL.md` | 含 `cli_capabilities.py` |

（同目录若存在 `examples.md`、`reference.md`，视为手册附录，非 `rule.md` 强制枚举项。）

---

## L3 编排场景（`orchestration/`）

| 类型 | 文档 |
|------|------|
| 跨场景契约 | [`CONTRACT_SKILL.md`](orchestration/CONTRACT_SKILL.md) |
| 一键成片 | [`chanjing-one-click-video-creation_SKILL.md`](orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation_SKILL.md) |

新增场景时：在 `orchestration/<scene>/` 下**只**增 **`{scene}_SKILL.md`**（与目录名一致）+ 所需 `scripts/`；**不**增入口级路由脚本。
