from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-credentials-guard"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-credentials-guard_SKILL.md",
        operations=[
            {"name": "open_login_page", "script": "open_login_page"},
            {"name": "status", "script": "chanjing-config --status"},
            {"name": "set_credentials", "script": "chanjing-config --ak ... --sk ..."},
            {"name": "run_print_access_token_script", "script": "chanjing-get-token"},
        ],
    )


def config():
    return config_contract(
        preconditions=["在任何蝉镜 API 调用前先运行本 skill"],
        required=[],
        optional=["ak", "sk"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing-config --status",
            "python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/open_login_page",
        ],
        outputs=["status JSON / access_token / 用户配置提示"],
    )


def status():
    return run_skill_script(SKILL_NAME, "chanjing-config", args=["--status"])


def set_credentials(ak: str, sk: str):
    return run_skill_script(SKILL_NAME, "chanjing-config", args=["--ak", ak, "--sk", sk])


def open_login_page():
    return run_skill_script(SKILL_NAME, "open_login_page")


def run_print_access_token_script():
    return run_skill_script(SKILL_NAME, "chanjing-get-token")

