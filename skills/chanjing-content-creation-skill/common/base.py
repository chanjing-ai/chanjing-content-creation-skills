from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

from exceptions import SkillExecutionError, SkillHTTPError, SkillTimeoutError


# --- HTTP（原 http_client.py，合并入 L1 base） ---


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"
    data = None
    request_headers = dict(headers or {})
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        raise SkillHTTPError(str(exc)) from exc


# --- 轮询（原 polling.py） ---


def poll_until(
    fetch: Callable[[], Any],
    *,
    is_done: Callable[[Any], bool],
    is_failed: Callable[[Any], bool] | None = None,
    interval_seconds: float = 3.0,
    timeout_seconds: float = 300.0,
) -> Any:
    deadline = time.time() + timeout_seconds
    while True:
        value = fetch()
        if is_done(value):
            return value
        if is_failed and is_failed(value):
            return value
        if time.time() >= deadline:
            raise SkillTimeoutError(f"polling timed out after {timeout_seconds}s")
        time.sleep(interval_seconds)


# --- 鉴权配置（原 auth.py，依赖 request_json） ---

CONFIG_DIR = Path(os.environ.get("CHANJING_CONFIG_DIR", Path.home() / ".chanjing"))
CONFIG_FILE = CONFIG_DIR / "credentials.json"
API_BASE = os.environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")
BUFFER_SECONDS = 300
LOGIN_URL = "https://www.chanjing.cc/openapi/login"

NO_CREDENTIALS_MSG = """已在浏览器打开蝉镜登录/注册页。
获取秘钥后请执行：
  python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing-config --ak <你的app_id> --sk <你的secret_key>
设置完毕后请重新执行您之前的操作。"""


def _run_open_login_page() -> None:
    try:
        skills_dir = Path(__file__).resolve().parent.parent
        script = skills_dir / "products" / "chanjing-credentials-guard" / "scripts" / "open_login_page"
        if script.exists():
            subprocess.run([sys.executable, str(script)], check=False, timeout=5)
        else:
            import webbrowser

            webbrowser.open(LOGIN_URL)
    except Exception:
        try:
            import webbrowser

            webbrowser.open(LOGIN_URL)
        except Exception:
            pass


def load_chanjing_credentials() -> dict[str, Any]:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as file_obj:
            return json.load(file_obj)
    return {}


def save_chanjing_credentials(data: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as file_obj:
        json.dump(data, file_obj, indent=2, ensure_ascii=False)
    try:
        os.chmod(CONFIG_FILE, 0o600)
    except OSError:
        pass


def refresh_chanjing_access_token(app_id: str, secret_key: str) -> tuple[str | None, str | None]:
    body = request_json(
        "POST",
        f"{API_BASE}/open/v1/access_token",
        body={"app_id": app_id, "secret_key": secret_key},
    )
    if body.get("code") != 0:
        return None, body.get("msg", "获取 Token 失败")
    payload = body.get("data") or {}
    token = payload.get("access_token")
    if not token:
        return None, "API 返回无 access_token"
    data = load_chanjing_credentials()
    data["access_token"] = token
    data["expire_in"] = payload.get("expire_in")
    save_chanjing_credentials(data)
    return token, None


def resolve_chanjing_access_token() -> tuple[str | None, str | None]:
    data = load_chanjing_credentials()
    app_id = (data.get("app_id") or "").strip()
    secret_key = (data.get("secret_key") or "").strip()
    if not app_id or not secret_key:
        _run_open_login_page()
        return None, NO_CREDENTIALS_MSG

    now = int(time.time())
    token = data.get("access_token")
    expire_in = data.get("expire_in")
    try:
        expire_in = int(expire_in) if expire_in is not None else 0
    except (ValueError, TypeError):
        expire_in = 0
    if token and expire_in > now + BUFFER_SECONDS:
        return token, None
    return refresh_chanjing_access_token(app_id, secret_key)


def print_chanjing_access_token_cli() -> None:
    token, err = resolve_chanjing_access_token()
    if err:
        raise SystemExit(err)
    print(token)


# --- 脚本与能力目录（原 base 能力函数） ---


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def skills_root() -> Path:
    return repo_root() / "skills"


def skill_dir(skill_name: str) -> Path:
    return skills_root() / "chanjing-content-creation-skill" / "products" / skill_name


def script_path(skill_name: str, script_name: str) -> Path:
    """L2：`products/<skill>/scripts/`；仅存在于 L3 的技能（如一键成片）在 `orchestration/<skill>/scripts/`。"""
    under_products = skill_dir(skill_name) / "scripts" / script_name
    if under_products.exists():
        return under_products
    under_orch = (
        skills_root()
        / "chanjing-content-creation-skill"
        / "orchestration"
        / skill_name
        / "scripts"
        / script_name
    )
    if under_orch.exists():
        return under_orch
    return under_products


def run_skill_script(
    skill_name: str,
    script_name: str,
    *,
    args: list[str] | None = None,
    parse_json: bool = False,
    cwd: Path | None = None,
) -> dict[str, Any]:
    cmd = [sys.executable, str(script_path(skill_name, script_name)), *(args or [])]
    proc = subprocess.run(
        cmd,
        cwd=str(cwd or repo_root()),
        text=True,
        capture_output=True,
        check=False,
    )
    result: dict[str, Any] = {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "command": cmd,
    }
    if parse_json and proc.stdout.strip():
        try:
            result["json"] = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise SkillExecutionError(
                f"{skill_name}/{script_name} did not return valid JSON"
            ) from exc
    return result


def capability_catalog(
    skill_name: str,
    *,
    manual: str,
    operations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "skill": skill_name,
        "manual": manual,
        "operations": operations,
    }


def config_contract(
    *,
    preconditions: list[str],
    required: list[str],
    optional: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "preconditions": preconditions,
        "required": required,
        "optional": optional or [],
    }


def usage_contract(*, examples: list[str], outputs: list[str]) -> dict[str, Any]:
    return {
        "examples": examples,
        "outputs": outputs,
    }


if __name__ == "__main__":
    print_chanjing_access_token_cli()
