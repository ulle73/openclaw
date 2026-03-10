from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

try:
    import output_bus
except ModuleNotFoundError:
    from scripts import output_bus


WORKSPACE = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = WORKSPACE / "scripts" / "install_program.ps1"
BROWSER_HOST = WORKSPACE / "scripts" / "browser_host.js"

INSTALL_PATTERNS = [
    re.compile(r"(?:ladda\s+ner\s+(?:och\s+)?)?installera\s+(.+?)(?:\s+för\s+mig)?[.!?]*$", re.IGNORECASE),
    re.compile(r"(?:download\s+and\s+)?install\s+(.+?)(?:\s+for\s+me)?[.!?]*$", re.IGNORECASE),
]

PAPER_VERIFY_COMMAND = (
    "$candidates=@("
    "\"$env:LOCALAPPDATA\\Programs\\Paper\\Paper.exe\","
    "\"$env:LOCALAPPDATA\\Programs\\paper\\Paper.exe\","
    "\"$env:ProgramFiles\\Paper\\Paper.exe\","
    "\"${env:ProgramFiles(x86)}\\Paper\\Paper.exe\""
    ");"
    "foreach($p in $candidates){ if($p -and (Test-Path $p)){ Write-Output $p; exit 0 } };"
    "exit 1"
)


@dataclass(frozen=True)
class AppSpec:
    key: str
    display_name: str
    aliases: tuple[str, ...]
    winget_id: str | None = None
    download_url: str | None = None
    silent_profile: str = "auto"
    verify_command: str | None = None


KNOWN_APPS = (
    AppSpec(
        key="paper-desktop",
        display_name="Paper Desktop",
        aliases=(
            "paper desktop",
            "paper app",
            "paper.design",
            "paper design",
            "paper",
        ),
        download_url="https://download.paper.design/",
        silent_profile="nsis",
        verify_command=PAPER_VERIFY_COMMAND,
    ),
)


def ensure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def normalize(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    lowered = folded.lower()
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def extract_install_target(raw_message: str) -> str | None:
    lines = [line.strip() for line in (raw_message or "").splitlines() if line.strip()]
    for candidate in reversed(lines):
        for pattern in INSTALL_PATTERNS:
            match = pattern.search(candidate)
            if match:
                return clean_target(match.group(1))

    whole = (raw_message or "").strip()
    for pattern in INSTALL_PATTERNS:
        match = pattern.search(whole)
        if match:
            return clean_target(match.group(1))
    return None


def clean_target(value: str) -> str:
    cleaned = (value or "").strip().strip("\"'`")
    cleaned = re.sub(r"\s+(?:snalla|snälla|please)$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+(?:tack)$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+[.!?]+$", "", cleaned)
    return cleaned.strip()


def find_known_app(query: str) -> AppSpec | None:
    query_norm = normalize(query)
    if not query_norm:
        return None

    best_match: tuple[int, AppSpec] | None = None
    for spec in KNOWN_APPS:
        score = 0
        for alias in spec.aliases:
            alias_norm = normalize(alias)
            if query_norm == alias_norm:
                score = max(score, 100)
            elif query_norm in alias_norm or alias_norm in query_norm:
                score = max(score, 80)
            elif all(token in alias_norm for token in query_norm.split()):
                score = max(score, 60)
        if score and (best_match is None or score > best_match[0]):
            best_match = (score, spec)
    return best_match[1] if best_match else None


def parse_winget_search(output: str) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for line in output.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.startswith("-") or stripped.startswith("Name"):
            continue
        parts = re.split(r"\s{2,}", stripped)
        if len(parts) < 3:
            continue
        results.append(
            {
                "name": parts[0].strip(),
                "id": parts[1].strip(),
                "version": parts[2].strip(),
                "match": parts[3].strip() if len(parts) > 3 else "",
            }
        )
    return results


def find_winget_app(query: str) -> AppSpec | None:
    command = ["winget", "search", "--source", "winget", query]
    process = subprocess.run(command, capture_output=True, text=True, cwd=WORKSPACE)
    if process.returncode != 0:
        return None

    query_norm = normalize(query)
    candidates = parse_winget_search(process.stdout)
    scored: list[tuple[int, dict[str, str]]] = []
    for candidate in candidates:
        name_norm = normalize(candidate["name"])
        id_norm = normalize(candidate["id"])
        score = 0
        if query_norm == name_norm or query_norm == id_norm:
            score = 100
        elif name_norm.startswith(query_norm) or id_norm.startswith(query_norm):
            score = 90
        elif query_norm in name_norm or query_norm in id_norm:
            score = 70
        elif all(token in name_norm for token in query_norm.split()):
            score = 60
        if score:
            scored.append((score, candidate))

    if not scored:
        return None

    scored.sort(key=lambda item: item[0], reverse=True)
    top_score, top_candidate = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else -1
    if top_score < 90 and second_score >= top_score:
        return None

    return AppSpec(
        key=f"winget:{top_candidate['id']}",
        display_name=top_candidate["name"],
        aliases=(query,),
        winget_id=top_candidate["id"],
    )


def resolve_app(query: str) -> AppSpec | None:
    known = find_known_app(query)
    if known:
        return known
    return find_winget_app(query)


def discover_paper_download_url() -> str:
    command = [
        "node",
        str(BROWSER_HOST),
        "links",
        "https://paper.design/downloads",
        "--limit",
        "60",
        "--json",
    ]
    process = subprocess.run(command, capture_output=True, text=True, cwd=WORKSPACE)
    if process.returncode != 0:
        return "https://download.paper.design/"

    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        return "https://download.paper.design/"

    for link in payload.get("links", []):
        href = str(link.get("href") or "").strip()
        if href.startswith("https://download.paper.design/windows/"):
            return href
    for link in payload.get("links", []):
        href = str(link.get("href") or "").strip()
        if href.startswith("https://download.paper.design/"):
            return href
    return "https://download.paper.design/"


def resolve_download_url(app: AppSpec) -> str | None:
    if app.key == "paper-desktop":
        return discover_paper_download_url()
    return app.download_url


def run_install_script(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    command = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(INSTALL_SCRIPT),
        *arguments,
    ]
    return subprocess.run(command, capture_output=True, text=True, cwd=WORKSPACE)


def verification_args(app: AppSpec) -> list[str]:
    arguments: list[str] = ["-Action", "verify"]
    if app.winget_id:
        arguments.extend(["-WingetId", app.winget_id])
    if app.verify_command:
        arguments.extend(["-VerifyCommand", app.verify_command])
    return arguments


def install_args(app: AppSpec) -> list[str]:
    if app.winget_id:
        arguments = ["-Action", "install-winget", "-WingetId", app.winget_id]
    else:
        url = resolve_download_url(app)
        if not url:
            raise RuntimeError(f"No install source available for {app.display_name}")
        arguments = ["-Action", "install-url", "-DownloadUrl", url]
        if app.silent_profile:
            arguments.extend(["-SilentProfile", app.silent_profile])

    if app.verify_command:
        arguments.extend(["-VerifyCommand", app.verify_command])
    return arguments


def already_installed_message(app: AppSpec, detail: str) -> str:
    return f"✅ {app.display_name} finns redan installerat.\n\nVerifiering: {detail.strip()}"


def installed_message(app: AppSpec, detail: str) -> str:
    return f"✅ {app.display_name} installerades och verifierades.\n\n{detail.strip()}"


def unresolved_message(target: str) -> str:
    return (
        "❌ Jag kunde inte avgöra exakt vilket program du menade tillräckligt säkert för auto-install.\n\n"
        f"Tolkad målapp: {target}"
    )


def platform_guard() -> None:
    if platform.system().lower() != "windows":
        raise RuntimeError("Den här auto-installvägen är bara uppsatt för Windows just nu.")


def maybe_send_ops_alert(source: str, detail: str) -> None:
    try:
        output_bus.fanout_text("ops-alerts", output_bus.build_ops_alert(source, detail), silent=True)
    except Exception:
        pass


def handle_request(raw_message: str, dry_run: bool = False) -> tuple[int, str]:
    platform_guard()
    target = extract_install_target(raw_message)
    if not target:
        return 2, "❌ Jag kunde inte extrahera ett installationsmål från meddelandet."

    app = resolve_app(target)
    if not app:
        return 3, unresolved_message(target)

    verify_before = run_install_script(verification_args(app))
    if verify_before.returncode == 0:
        return 0, already_installed_message(app, verify_before.stdout or verify_before.stderr)

    if dry_run:
        method = f"winget:{app.winget_id}" if app.winget_id else f"url:{resolve_download_url(app)}"
        return 0, f"DRY RUN: skulle installera {app.display_name} via {method}"

    install_process = run_install_script(install_args(app))
    detail = (install_process.stdout or install_process.stderr or "").strip()
    if install_process.returncode != 0:
        maybe_send_ops_alert(
            "Program installation",
            f"Mål: {app.display_name}\n\nFel: {detail or 'okänt fel'}",
        )
        return install_process.returncode, f"❌ Installationen av {app.display_name} misslyckades.\n\n{detail or 'Okänt fel.'}"

    return 0, installed_message(app, detail)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Handle explicit install requests deterministically.")
    parser.add_argument("--raw-message", required=True, help="Original user message")
    parser.add_argument("--dry-run", action="store_true", help="Resolve without installing")
    parser.add_argument("--json", action="store_true", help="Emit JSON payload")
    return parser


def main() -> int:
    ensure_utf8_output()
    parser = build_parser()
    args = parser.parse_args()

    code, message = handle_request(args.raw_message, dry_run=args.dry_run)
    if args.json:
        print(json.dumps({"ok": code == 0, "code": code, "message": message}, ensure_ascii=False))
    else:
        print(message)
    return 0 if code == 0 else code


if __name__ == "__main__":
    raise SystemExit(main())
