# chan-skills

Chan Openclaw skills for E-Commerce content creation (practical AI tools and skills).

中文版本见 [CHANGJING-README.zh-CN.md](CHANGJING-README.zh-CN.md)。

## Install

```bash
# List available Chan skills
npx skills add chanjing-ai/chan-skills --list

# Install all Chan skills
npx skills add chanjing-ai/chan-skills

# Install the content-creation skill package
npx skills add chanjing-ai/chan-skills --skill chanjing-content-creation-skill -y
```

## Get and set API keys (Chan Jing / 蝉镜)

**Agent entry point (first stop):** [skills/chanjing-content-creation-skill/SKILL.md](../skills/chanjing-content-creation-skill/SKILL.md) — global routing index only. L3 orchestration lives under [`orchestration/`](../skills/chanjing-content-creation-skill/orchestration/README.md); L2 products under [`products/`](../skills/chanjing-content-creation-skill/products/).

Before using Chan Jing (蝉镜) skills (TTS, digital avatar, voice clone, etc.), configure **Access Key (app_id)** and **Secret Key (secret_key)**. See [chanjing-credentials-guard](../skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/chanjing-credentials-guard_SKILL.md) for details.

### Get API keys

1. Open the Chan Jing sign-up/login page to obtain AK/SK:
   ```bash
   python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/open_login_page
   ```
   Or open in a browser: <https://www.chanjing.cc/openapi/login>  
2. After signing up or logging in, create an API key in the console and copy **app_id** and **secret_key**.

### Set API keys

Run in your terminal (replace `<your_app_id>` and `<your_secret_key>` with your values):

```bash
python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing-config --ak <your_app_id> --sk <your_secret_key>
```

Credentials are written to `~/.chanjing/credentials.json` (override the directory with env `CHANJING_CONFIG_DIR`). After setting, re-run your intended action.

Check current config status:

```bash
python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing-config --status
```

## Available skills

| Name | Description |
|------|-------------|
| *(entry)* | [skills/chanjing-content-creation-skill/SKILL.md](../skills/chanjing-content-creation-skill/SKILL.md) — main entry for agents. |
| chanjing-content-creation-skill | Package entry: global index in `SKILL.md` only; L3 orchestration and contracts under `orchestration/`; L2 products under `products/`; L1 `common/`. |
| chanjing-credentials-guard | Credentials guard: validate AK/SK and Token before any Chanjing API; guide login and Shell config when missing. Run first before other Chanjing skills. |
| chanjing-tts | Bilingual text-to-speech using provided voices (Chinese and English). |
| chanjing-tts-voice-clone | Bilingual TTS using a user-provided reference voice. |
| chanjing-avatar | Lip-sync / digital avatar video generation. |
| chanjing-video-compose | Digital human video synthesis from text or audio, with task polling and optional local download. |
| chanjing-customised-person | Create, inspect, poll, and delete customised digital humans from uploaded source videos. |
| chanjing-text-to-digital-person | Create AI digital person images from prompts, turn them into short talking videos, and optionally run LoRA tasks. |
| chanjing-ai-creation | Generic AI creation task runner for supported image/video models, with submit, list, detail, polling, and download workflows. |
| chanjing-one-click-video-creation | One-click short video from a topic or workflow (script, storyboard, digital human + AI scenes, local mp4). **L3 orchestration** under `orchestration/chanjing-one-click-video-creation/`; route from `SKILL.md` to **`chanjing-one-click-video-creation_SKILL.md`**. |

## Layout (top index + L1 / L2 / L3)

- `skills/chanjing-content-creation-skill/SKILL.md`: global entry — **routing** plus **runtime contract** (env, credentials, binaries, persistence) per [skills/rule.md](../skills/rule.md) §6; product/scene **business** details live in each **`{name}_SKILL.md`**. After routing, open the target **`{name}_SKILL.md`**.
- `skills/chanjing-content-creation-skill/common/`: L1 shared foundation (`base.py`, `exceptions.py`, `logger.py`; no product business logic).
- `skills/chanjing-content-creation-skill/products/<product>/`: L2 products; each has **`<product>_SKILL.md`** + `scripts/` (including `cli_capabilities.py` and CLI scripts).
- `skills/chanjing-content-creation-skill/orchestration/`: L3 composes multiple L2 capabilities; each scene dir has **one** **`<scene>_SKILL.md`** + optional `scripts/`, plus shared `CONTRACT_SKILL.md`.
- `skills/chanjing-content-creation-skill/products/<product>/scripts/cli_capabilities.py`: L2 callable Python capability layer (same pattern under L3 `orchestration/<scene>/scripts/` where applicable).
