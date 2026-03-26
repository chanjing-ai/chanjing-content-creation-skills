# chan-skills

面向电商内容创作的 Chan Openclaw 技能集合（实用 AI 工具与技能）。

English version: [CHANJING-README.md](CHANJING-README.md)

## 安装

```bash
# 列出可用的 Chan 技能
npx skills add chanjing-ai/chan-skills --list

# 安装全部 Chan 技能
npx skills add chanjing-ai/chan-skills

# 安装内容创作技能包
npx skills add chanjing-ai/chan-skills --skill chanjing-content-creation-skill -y
```

## 获取并设置 API Key（Chan Jing / 蝉镜）

**Agent 第一站：** [skills/chanjing-content-creation-skill/SKILL.md](../skills/chanjing-content-creation-skill/SKILL.md) — **仅**全局路由索引；L3 编排在 [`orchestration/`](../skills/chanjing-content-creation-skill/orchestration/README.md)；L2 产品在 [`products/`](../skills/chanjing-content-creation-skill/products/)。

在使用 Chan Jing（蝉镜）相关技能（TTS、数字人、声音复刻等）之前，需要先配置 **Access Key (`app_id`)** 和 **Secret Key (`secret_key`)**。详细说明见 [chanjing-credentials-guard](../skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/chanjing-credentials-guard_SKILL.md)。

### 获取 API Key

1. 打开蝉镜注册/登录页面以获取 AK/SK：
   ```bash
   python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/open_login_page
   ```
   或直接在浏览器中打开：<https://www.chanjing.cc/openapi/login>  
2. 注册或登录后，在控制台创建 API Key，并复制 **app_id** 和 **secret_key**。

### 设置 API Key

在终端中运行以下命令（将 `<your_app_id>` 和 `<your_secret_key>` 替换为你的实际值）：

```bash
python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing-config --ak <your_app_id> --sk <your_secret_key>
```

凭据会写入 `~/.chanjing/credentials.json`（也可通过环境变量 `CHANJING_CONFIG_DIR` 覆盖目录）。设置完成后，重新执行你原本要运行的操作即可。

查看当前配置状态：

```bash
python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing-config --status
```

## 可用技能

| 名称 | 说明 |
|------|------|
| *（入口）* | [skills/chanjing-content-creation-skill/SKILL.md](../skills/chanjing-content-creation-skill/SKILL.md) — 内容创作技能包入口，Agent 第一站。 |
| chanjing-content-creation-skill | 内容创作技能包：`SKILL.md` 仅全局路由索引；`orchestration/` 为 L3 编排与契约；`products/` 为 L2；`common/` 为 L1。 |
| chanjing-credentials-guard | 凭据守卫：在调用任何蝉镜 API 前校验 AK/SK 和 Token；缺失时引导登录和 Shell 配置。建议在其他蝉镜技能之前先运行。 |
| chanjing-tts | 使用内置音色进行中英文文本转语音。 |
| chanjing-tts-voice-clone | 使用用户提供的参考音色进行中英文 TTS。 |
| chanjing-avatar | 唇形驱动 / 数字人视频生成。 |
| chanjing-video-compose | 基于文本或音频合成数字人视频，支持任务轮询和可选本地下载。 |
| chanjing-customised-person | 基于上传源视频创建、查看、轮询和删除定制数字人。 |
| chanjing-text-to-digital-person | 通过提示词创建 AI 数字人形象，将其转成短口播视频，并可选执行 LoRA 任务。 |
| chanjing-ai-creation | 通用 AI 创作任务工具，支持已接入图像/视频模型的提交、列表、详情、轮询和下载流程。 |
| chanjing-one-click-video-creation | 一键成片：选题或工作流生成完整短视频（文案、分镜、数字人+AI 画面）。**L3 编排**（`orchestration/chanjing-one-click-video-creation/`）；由 `SKILL.md` 路由至 **`chanjing-one-click-video-creation_SKILL.md`**（细则见同目录 `README.md` / `templates/`）。 |

## 分层架构（Agent 视角）

```text
skills/
└── chanjing-content-creation-skill/
    ├── SKILL.md
    ├── common/
    ├── products/
    └── orchestration/
        ├── CONTRACT_SKILL.md
        └── chanjing-one-click-video-creation/
            ├── chanjing-one-click-video-creation_SKILL.md
            └── scripts/
                ├── cli_capabilities.py
                └── run_render.py
```

- `skills/chanjing-content-creation-skill/SKILL.md`：全局唯一入口——**路由** + 按 [`skills/rule.md`](../skills/rule.md) **§六** 写明的 **「运行时契约」**（环境变量、凭据、二进制、落盘等）；**业务细则**在各 **`{名}_SKILL.md`**。命中目标后打开对应手册。
- `skills/chanjing-content-creation-skill/common/`：L1（`base.py`、`exceptions.py`、`logger.py`），无产品业务逻辑。
- `skills/chanjing-content-creation-skill/products/<product>/<product>_SKILL.md`：L2 执行真值；**`scripts/`** 内含 `cli_capabilities.py` 与各 CLI。
- `skills/chanjing-content-creation-skill/orchestration/`：L3；每场景目录 **一个** `<scene>_SKILL.md` + `scripts/` 等；`CONTRACT_SKILL.md` 为共用契约。
