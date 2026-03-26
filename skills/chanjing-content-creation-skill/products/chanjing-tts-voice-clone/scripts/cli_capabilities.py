from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-tts-voice-clone"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-tts-voice-clone_SKILL.md",
        operations=[
            {"name": "create_voice", "script": "create_voice"},
            {"name": "poll_voice", "script": "poll_voice"},
            {"name": "create_task", "script": "create_task"},
            {"name": "poll_task", "script": "poll_task"},
        ],
    )


def config():
    return config_contract(
        preconditions=["先通过 chanjing-credentials-guard", "参考音频必须为公开 URL"],
        required=["name", "url", "text"],
        optional=["language", "speed", "pitch"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-tts-voice-clone/scripts/create_voice --name '我的声音' --url 'https://example.com/ref.mp3'",
            "python skills/chanjing-content-creation-skill/products/chanjing-tts-voice-clone/scripts/poll_voice --voice-id <id>",
            "python skills/chanjing-content-creation-skill/products/chanjing-tts-voice-clone/scripts/create_task --audio-man <voice_id> --text '你好'",
        ],
        outputs=["voice_id / task_id / audio_url"],
    )


def create_voice(name: str, url: str, language: str | None = None):
    args = ["--name", name, "--url", url]
    if language:
        args += ["--language", language]
    return run_skill_script(SKILL_NAME, "create_voice", args=args)


def poll_voice(voice_id: str):
    return run_skill_script(SKILL_NAME, "poll_voice", args=["--voice-id", voice_id])


def create_task(audio_man: str, text: str, speed: float | None = None, pitch: float | None = None):
    args = ["--audio-man", audio_man, "--text", text]
    if speed is not None:
        args += ["--speed", str(speed)]
    if pitch is not None:
        args += ["--pitch", str(pitch)]
    return run_skill_script(SKILL_NAME, "create_task", args=args)


def poll_task(task_id: str):
    return run_skill_script(SKILL_NAME, "poll_task", args=["--task-id", task_id])

