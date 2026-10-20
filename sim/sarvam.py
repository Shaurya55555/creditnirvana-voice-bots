"""Thin Sarvam client: chat completions and text-to-speech. Key is read from .env, never printed."""
import base64
import os
import re
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://api.sarvam.ai"


def _key() -> str:
    key = os.environ.get("SARVAM_API_KEY", "")
    if not key:
        env = ROOT / ".env"
        if env.exists():
            for line in env.read_text(encoding="utf-8").splitlines():
                if line.startswith("SARVAM_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        raise SystemExit("SARVAM_API_KEY missing: add it to .env")
    return key


def _post(path: str, body: dict, retries: int = 4) -> dict:
    for attempt in range(retries):
        try:
            r = requests.post(
                BASE + path,
                headers={"api-subscription-key": _key(), "Content-Type": "application/json"},
                json=body,
                timeout=90,
            )
        except requests.exceptions.RequestException:
            time.sleep(2 * (attempt + 1))
            continue
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 * (attempt + 1))
            continue
        if not r.ok:
            raise RuntimeError(f"{path} {r.status_code}: {r.text[:300]}")
        return r.json()
    raise RuntimeError(f"{path} failed after {retries} tries")


def chat(messages: list[dict], model: str = "sarvam-105b", temperature: float = 0.4,
         max_tokens: int = 400) -> str:
    text = ""
    for budget in (max_tokens, max_tokens * 2, max_tokens * 4):  # reasoning can eat the budget and leave content empty
        out = _post("/v1/chat/completions", {
            "model": model, "messages": messages,
            "temperature": temperature, "max_tokens": budget,
        })
        text = out["choices"][0]["message"]["content"] or ""
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
        if text:
            break
    return text


def tts(text: str, speaker: str, lang: str = "hi-IN", model: str = "bulbul:v3",
        pace: float = 1.0, rate: int = 24000) -> bytes:
    out = _post("/text-to-speech", {
        "text": text[:2400], "target_language_code": lang, "speaker": speaker,
        "model": model, "pace": pace, "speech_sample_rate": rate,
    })
    return base64.b64decode(out["audios"][0])
