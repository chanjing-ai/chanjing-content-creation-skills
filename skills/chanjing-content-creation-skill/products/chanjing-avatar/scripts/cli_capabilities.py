from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-avatar"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-avatar_SKILL.md",
        operations=[
            {"name": "get_upload_url", "script": "get_upload_url"},
            {"name": "upload_file", "script": "upload_file"},
            {"name": "create_task", "script": "create_task"},
            {"name": "poll_task", "script": "poll_task"},
        ],
    )


def config():
    return config_contract(
        preconditions=["先通过 chanjing-credentials-guard"],
        required=["video_file_id", "audio_type"],
        optional=[
            "text",
            "audio_man_id",
            "audio_file_id",
            "screen_width",
            "screen_height",
            "model",
            "callback",
            "speed",
            "pitch",
        ],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-avatar/scripts/upload_file --service lip_sync_video --file ./my_video.mp4",
            "python skills/chanjing-content-creation-skill/products/chanjing-avatar/scripts/create_task --video-file-id <id> --text '你好' --audio-man-id <voice_id>",
            "python skills/chanjing-content-creation-skill/products/chanjing-avatar/scripts/poll_task --id <task_id>",
        ],
        outputs=["file_id / task_id / video_url"],
    )


def upload_file(service: str, file_path: str):
    return run_skill_script(SKILL_NAME, "upload_file", args=["--service", service, "--file", file_path])


def create_task(args: list[str]):
    return run_skill_script(SKILL_NAME, "create_task", args=args)


def poll_task(task_id: str):
    return run_skill_script(SKILL_NAME, "poll_task", args=["--id", task_id])

