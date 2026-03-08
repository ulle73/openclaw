"""Generate GravityClaw's initialization prompt by filling in your identity + provider names."""
from pathlib import Path
import os

BASE = Path(__file__).resolve().parents[1]
TEMPLATE = BASE / "resources" / "init_prompt_template.md"
OUTPUT = BASE / "resources" / "GravityClaw-init-prompt.md"

values = {
    "project_name": os.environ.get("PROJECT_NAME", "GravityClaw"),
    "owner_name": os.environ.get("OWNER_NAME", "GravityClaw Operator"),
    "primary_channel": os.environ.get("PRIMARY_CHANNEL", "telegram"),
    "voice_provider": os.environ.get("VOICE_PROVIDER", "11 Labs"),
    "voice_model": os.environ.get("VOICE_MODEL", "alloy"),
    "stt_provider": os.environ.get("STT_PROVIDER", "Gro"),
    "stt_model": os.environ.get("STT_MODEL", "whisper-1"),
    "llm_provider": os.environ.get("LLM_PROVIDER", "OpenRouter"),
}

if not TEMPLATE.exists():
    raise FileNotFoundError(f"Template not found: {TEMPLATE}")

template_text = TEMPLATE.read_text(encoding="utf-8")
output_text = template_text.format(**values)
OUTPUT.write_text(output_text, encoding="utf-8")
print(f"Wrote {OUTPUT.relative_to(BASE)}. Rerun after you change environment variables.")
