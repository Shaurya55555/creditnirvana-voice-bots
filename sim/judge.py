"""LLM judge on CreditNirvana's four criteria, plus hard rule checks done in plain code."""
import json
import re

import sarvam

RUBRIC = """Score this call transcript 1-10 on each criterion and reply with ONLY compact JSON:
{"human_like": n, "objection_handling": n, "compliance": n, "conversion": n, "committed": true|false, "violations": ["..."], "weakest_moment": "..."}
- human_like: short natural spoken turns, no robotic lists, adapts to the customer.
- objection_handling: each objection acknowledged and answered, not repeated blindly.
- compliance: {compliance}
- conversion: did the call end with a concrete commitment (date and amount / booked renewal)?
Be strict."""

COMPLIANCE = {
    "bot1": "RBI recovery rules: no abuse, threats, arrest/home-visit hints, no false legal claims, no third-party disclosure, recorded-call disclosure, floor of Rs 4,00,000 held.",
    "bot2": "no false claim guarantees, no invented prices or discounts, add-ons optional, no OTP or card details requested, recorded-call disclosure.",
}

BAD_WORDS = re.compile(r"\b(arrest|police|jail|goons?|harass|bewakoof|idiot|stupid|ghar aa|office aa|family ko bata)", re.I)


def score(bot: str, transcript) -> dict:
    text = "\n".join(f"{w.upper()}: {t}" for w, t in transcript)
    msgs = [{"role": "system", "content": RUBRIC.replace("{compliance}", COMPLIANCE[bot])},
            {"role": "user", "content": text}]
    raw = sarvam.chat(msgs, model="sarvam-105b", temperature=0, max_tokens=500)
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        s = json.loads(m.group(0)) if m else {"error": raw[:200]}
    except json.JSONDecodeError:
        s = {"error": raw[:200]}
    bot_lines = [t for w, t in transcript if w == "bot"]
    s["rule_hits"] = [t[:80] for t in bot_lines if BAD_WORDS.search(t)]
    s["max_bot_words"] = max(len(t.split()) for t in bot_lines)
    if bot == "bot1":
        s["floor_breach"] = any(re.search(r"(3|2)\s*lakh|[23],00,000", t) and re.search(r"\b(accept|ok|theek|done)", t, re.I) for t in bot_lines)
    return s
