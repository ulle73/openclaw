from __future__ import annotations

import argparse
import asyncio
import base64
import json
import os
import time
from typing import Any
from pathlib import Path

from openai import AuthenticationError, OpenAI
from playwright.async_api import Page, async_playwright


def ensure_utf8_output() -> None:
    for stream in (os.sys.stdout, os.sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def openclaw_root() -> Path:
    return Path.home() / ".openclaw"


def load_openclaw_oauth_access_token() -> str | None:
    candidate_files = [
        openclaw_root() / "agents" / "boss" / "agent" / "auth-profiles.json",
        openclaw_root() / "agents" / "main" / "agent" / "auth-profiles.json",
    ]

    now_ms = int(time.time() * 1000)
    for path in candidate_files:
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        last_good = ((payload.get("lastGood") or {}).get("openai-codex") or "").strip()
        profiles = payload.get("profiles") or {}
        profile = profiles.get(last_good) if last_good else None
        if not profile:
            for value in profiles.values():
                if value.get("type") == "oauth" and value.get("provider") == "openai-codex":
                    profile = value
                    break
        if not profile:
            continue

        access = (profile.get("access") or "").strip()
        expires = int(profile.get("expires") or 0)
        if access and (expires == 0 or expires > now_ms):
            return access
    return None


def build_openai_client() -> tuple[OpenAI, str]:
    env_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if env_key:
        return OpenAI(api_key=env_key), "api_key"

    oauth_access = load_openclaw_oauth_access_token()
    if oauth_access:
        return OpenAI(api_key=oauth_access), "openclaw_oauth"

    raise RuntimeError(
        "Ingen giltig OpenAI-credential hittades. Varken OPENAI_API_KEY eller en giltig OpenClaw OAuth access-token finns tillgänglig."
    )


def extract_final_text(response: Any) -> str:
    lines: list[str] = []
    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", None) != "message":
            continue
        content = getattr(item, "content", None) or []
        for part in content:
            text = getattr(part, "text", None)
            if isinstance(text, str) and text.strip():
                lines.append(text.strip())
    return "\n\n".join(lines).strip()


def first_computer_call(response: Any) -> Any | None:
    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", None) == "computer_call":
            return item
    return None


async def handle_computer_actions(page: Page, actions: list[Any]) -> None:
    for action in actions:
        action_type = getattr(action, "type", None)
        if action_type == "click":
            await page.mouse.click(
                getattr(action, "x", 0),
                getattr(action, "y", 0),
                button=getattr(action, "button", "left"),
            )
        elif action_type == "double_click":
            await page.mouse.dblclick(
                getattr(action, "x", 0),
                getattr(action, "y", 0),
                button=getattr(action, "button", "left"),
            )
        elif action_type == "scroll":
            await page.mouse.move(getattr(action, "x", 0), getattr(action, "y", 0))
            await page.mouse.wheel(
                getattr(action, "scrollX", 0),
                getattr(action, "scrollY", 0),
            )
        elif action_type == "keypress":
            for key in getattr(action, "keys", []) or []:
                await page.keyboard.press(" " if key == "SPACE" else key)
        elif action_type == "type":
            await page.keyboard.type(getattr(action, "text", ""))
        elif action_type == "move":
            await page.mouse.move(getattr(action, "x", 0), getattr(action, "y", 0))
        elif action_type == "drag":
            path = getattr(action, "path", None) or []
            if not path:
                continue
            first = path[0]
            await page.mouse.move(first["x"], first["y"])
            await page.mouse.down()
            for point in path[1:]:
                await page.mouse.move(point["x"], point["y"])
            await page.mouse.up()
        elif action_type == "wait":
            await page.wait_for_timeout(getattr(action, "ms", 1000))
        elif action_type == "screenshot":
            continue
        else:
            raise RuntimeError(f"Unsupported computer action: {action_type}")


async def capture_screenshot_base64(page: Page) -> str:
    png_bytes = await page.screenshot(type="png")
    return base64.b64encode(png_bytes).decode("utf-8")


async def run_loop(prompt: str, model: str, max_steps: int) -> str:
    client, auth_mode = build_openai_client()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
            chromium_sandbox=True,
            env={},
            args=["--disable-extensions", "--disable-file-system"],
        )
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()

        try:
            response = client.responses.create(
                model=model,
                tools=[{"type": "computer"}],
                input=prompt,
            )
        except AuthenticationError as exc:
            detail = str(exc)
            if auth_mode == "openclaw_oauth" and "api.responses.write" in detail:
                raise RuntimeError(
                    "OpenClaw Codex OAuth-token hittades, men den saknar Responses API-scope för direkt OpenAI SDK computer-use. "
                    "OpenClaw OAuth räcker alltså inte ensam för den officiella direct-API-harnessen. "
                    "Använd en credential med Responses-scope eller routea detta genom OpenClaws egen providerkedja."
                ) from exc
            raise

        for _ in range(max_steps):
            computer_call = first_computer_call(response)
            if computer_call is None:
                break

            await handle_computer_actions(page, list(getattr(computer_call, "actions", []) or []))
            screenshot_base64 = await capture_screenshot_base64(page)

            response = client.responses.create(
                model=model,
                tools=[{"type": "computer"}],
                previous_response_id=response.id,
                input=[
                    {
                        "type": "computer_call_output",
                        "call_id": computer_call.call_id,
                        "output": {
                            "type": "computer_screenshot",
                            "image_url": f"data:image/png;base64,{screenshot_base64}",
                            "detail": "original",
                        },
                    }
                ],
            )

        await context.close()
        await browser.close()

    final_text = extract_final_text(response)
    return final_text or "Computer-use-loopen avslutades utan ett vanligt textsvar."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run OpenAI computer use with a local Playwright browser harness.")
    parser.add_argument("--prompt", required=True, help="User task for the model")
    parser.add_argument("--model", default="gpt-5.4", help="Responses model to use")
    parser.add_argument("--max-steps", type=int, default=20, help="Maximum screenshot/action turns")
    return parser


def main() -> int:
    ensure_utf8_output()
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = asyncio.run(run_loop(args.prompt, args.model, args.max_steps))
    except Exception as exc:
        print(f"OpenAI computer use misslyckades.\n\n{exc}")
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
