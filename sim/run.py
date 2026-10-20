"""Simulate a call: bot (system prompt under test) vs an LLM tough customer, then judge it.

python sim/run.py bot1_excuse_machine            # one persona
python sim/run.py all                            # every persona
"""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import judge
import personas
import sarvam

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = {"bot1": ROOT / "prompts" / "bot1_loan_settlement.md",
           "bot2": ROOT / "prompts" / "bot2_car_insurance.md"}
GREETING = {
    "bot1": "Namaste, kya main {name} ji se baat kar rahi hoon? Main Riya, {lender} ke recovery desk se. Yeh call recorded hai.",
    "bot2": "Hello {name} ji, main Aman, {insurer} se. Yeh call recorded hai. Aapki Brezza ke renewal ke baare mein do minute baat kar sakte hain?",
}
MAX_TURNS = 22


def bot_system(bot: str) -> str:
    text = PROMPTS[bot].read_text(encoding="utf-8")
    v = personas.BOT_VARS[bot]
    for k, val in v.items():
        text = text.replace("{" + k + "}", val)
    return text + "\n\nCurrent time of call: 11:30 AM. Keep each reply under 30 words."


def run(persona: str) -> dict:
    bot = personas.BOT_FOR[persona]
    greeting = GREETING[bot].format(**personas.BOT_VARS[bot])
    bot_msgs = [{"role": "system", "content": bot_system(bot)},
                {"role": "assistant", "content": greeting}]
    cust_msgs = [{"role": "system", "content": personas.CUSTOMER_RULES + "\n\n" + personas.PERSONAS[persona]}]
    transcript = [("bot", greeting)]
    cust_in = greeting
    for _ in range(MAX_TURNS):
        cust_msgs.append({"role": "user", "content": cust_in})
        cust = sarvam.chat(cust_msgs, model="sarvam-105b", temperature=0.8, max_tokens=1500) or "Haan, bolo."
        cust_msgs.append({"role": "assistant", "content": cust})
        transcript.append(("customer", cust))
        bot_msgs.append({"role": "user", "content": cust})
        reply = sarvam.chat(bot_msgs, model="sarvam-105b-conversations", temperature=0.3, max_tokens=1500) or "Ji, ek minute."
        bot_msgs.append({"role": "assistant", "content": reply})
        transcript.append(("bot", reply))
        cust_in = reply
        if re.search(r"\b(bye|alvida|namaste.*dhanyavaad|call end)\b", reply, re.I) and len(transcript) > 12:
            break
    scores = judge.score(bot, transcript)
    out = {"persona": persona, "bot": bot, "transcript": transcript, "scores": scores}
    stamp = time.strftime("%Y%m%d-%H%M%S")
    (ROOT / "runs" / f"{persona}-{stamp}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    txt = "\n".join(f"{who.upper()}: {t}" for who, t in transcript)
    (ROOT / "runs" / f"{persona}-{stamp}.txt").write_text(txt, encoding="utf-8")
    return out


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    names = list(personas.PERSONAS) if which == "all" else [which]
    for n in names:
        res = run(n)
        print(n, json.dumps(res["scores"], ensure_ascii=False))
