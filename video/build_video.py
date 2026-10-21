"""Render the project walkthrough video: HTML slides -> PNG (headless Chrome) -> MP4 (ffmpeg).

python video/build_video.py              # silent, captions only (works with no API credit)
python video/build_video.py --narrate    # adds Sarvam TTS narration per scene (needs a funded key in .env)

Every number on the slides comes from the Sarvam test runs and the saved simulated call in runs/.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "video"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 1920, 1080

CSS = """
*{box-sizing:border-box} body{margin:0;width:1920px;height:1080px;background:#0e1424;color:#eef2fb;
font-family:Segoe UI,Calibri,Arial,sans-serif;padding:84px 110px;position:relative}
h1{font-size:76px;margin:0 0 22px;letter-spacing:-1px} h2{font-size:54px;margin:0 0 34px;color:#8fb4ff}
p,li{font-size:38px;line-height:1.38;color:#d7def0} ul{padding-left:42px;margin:0} li{margin:10px 0}
.tag{display:inline-block;background:#1c2a4d;color:#8fb4ff;border-radius:999px;padding:8px 24px;font-size:28px;margin-bottom:26px}
.cols{display:flex;gap:56px} .card{flex:1;background:#151d36;border:1px solid #26335c;border-radius:22px;padding:34px 40px}
.card h3{margin:0 0 14px;font-size:40px;color:#fff} .big{font-size:96px;font-weight:700;color:#7cf0b1;line-height:1}
.bad{color:#ff9b9b} .good{color:#7cf0b1} .small{font-size:28px;color:#9fb0d6}
.bubble{border-radius:20px;padding:14px 26px;margin:10px 0;font-size:31px;line-height:1.3;max-width:1350px}
.bot{background:#1d3a74;border-bottom-left-radius:4px} .cust{background:#2b2f3f;margin-left:420px;border-bottom-right-radius:4px}
.foot{position:absolute;left:110px;bottom:48px;font-size:26px;color:#6f80a8}
table{border-collapse:collapse;width:100%} td,th{font-size:32px;padding:14px 18px;border-bottom:1px solid #26335c;text-align:left}
th{color:#8fb4ff}
"""


def page(body: str) -> str:
    return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}<div class='foot'>Shaurya Bajpai | CreditNirvana voice bot assignment</div></body></html>"


def excerpt() -> str:
    """Verbatim sentences from the saved simulated call (runs/), trimmed to whole sentences."""
    lines = [
        ("bot", "Rahul ji, aapka paanch lakh ka personal loan aath mahine se pending hai. Total due chheh lakh pachas hazaar hai."),
        ("cust", "Haan madam, meri job gayi hai abhi. Do lakh mein settlement ho sakta hai kya close karne ke liye?"),
        ("bot", "Company chaar lakh mein one-time settlement offer kar rahi hai. Isse aapke dhai lakh bach jayenge."),
        ("cust", "Dekho, bina details dekhe nahi bata sakta. Aaj commit nahi kar sakta."),
        ("bot", "Mujhe ek date aur ek amount chahiye, abhi. Kya aap chaar lakh tees tarikh tak de sakte hain?"),
        ("cust", "Haan, theek hai, tees tarikh tak chaar lakh de doonga."),
    ]
    return "".join(
        f"<div class='bubble {c}'><b>{'Riya' if c == 'bot' else 'Customer'}:</b> {t}</div>" for c, t in lines)


SCENES = [
    ("Two voice bots built to convert",
     page("<div class='tag'>CreditNirvana Voice Labs assignment</div><h1>Two voice agents.<br>One goal: conversion.</h1>"
          "<p>Riya settles overdue personal loans. Aman renews Maruti Brezza insurance.<br>Built on Sarvam Voice Agents, tested, and fixed from real failures.</p>"),
     "I built two voice agents on Sarvam: Riya for loan settlement and Aman for car insurance renewal. Both are designed around one goal, conversion, and tested against tough customers.", 9),
    ("The brief",
     page("<h2>What was asked</h2><div class='cols'><div class='card'><h3>Bot 1: Loan settlement</h3><ul><li>Rs 5L loan, 8 months unpaid</li><li>Dues Rs 6.5L, settle at Rs 4L</li><li>Firm, assertive, RBI compliant</li></ul></div>"
          "<div class='card'><h3>Bot 2: Insurance renewal</h3><ul><li>Maruti Brezza renewal</li><li>IDV Rs 9L to Rs 8L</li><li>Premium Rs 20k, discount Rs 15k</li></ul></div></div>"
          "<p style='margin-top:40px'>Judged on: human-like talk, objection handling, compliance, conversion.</p>"),
     "The brief was two bots, judged on human-like conversation, objection handling, compliance and conversion.", 10),
    ("How the prompts are built",
     page("<h2>Same skeleton, voice first</h2><ul><li><b>Locked case facts</b> so the model never invents a number</li><li><b>One goal</b> with a fallback ladder, never an open ending</li>"
          "<li><b>Short turns</b>, about 25 words, amounts spoken in words</li><li><b>Hard stops</b> that override everything, for compliance</li><li><b>Objection library</b> with a scripted pattern per excuse</li></ul>"),
     "Both prompts share one skeleton. Facts are locked, the goal has a fallback ladder, turns are short, and hard stops override everything for compliance.", 11),
    ("Riya: firm without crossing the line",
     page("<h2>Riya negotiates on timing, never on the floor</h2><div class='cols'><div class='card'><h3>Ask ladder</h3><ul><li>Full Rs 6,50,000</li><li>Rs 4,00,000 lump sum in 7 days</li><li>Two parts or a token today</li></ul></div>"
          "<div class='card'><h3>Compliance</h3><ul><li>Calls 8 AM to 7 PM only</li><li>No loan detail before identity</li><li>No threats, no third parties</li><li>Distress ends the pitch</li></ul></div></div>"),
     "Riya anchors on the full amount, then the four lakh settlement, then a split or a token payment. She only negotiates on timing, never on the floor, and stays inside recovery guidelines.", 11),
    ("A real simulated call",
     page("<h2 style='margin-bottom:18px'>Excuse machine vs Riya (saved test call)</h2>" + excerpt() + "<p class='small'>Simulated customer, text transcript from this project. Settlement held at Rs 4,00,000 with a confirmed date.</p>"),
     "Here is a saved test conversation. The customer keeps changing excuses and pushes for a lower amount. Riya names the pattern, holds four lakh, and keeps asking for a date.", 14),
    ("Aman: explain the drop, then sell",
     page("<h2>Aman turns the IDV drop into the pitch</h2><div class='cols'><div class='card'><h3>Flow</h3><ul><li>Explain IDV 9L to 8L before it is asked</li><li>Anchor the Rs 5,000 saving</li><li>Add-ons matched to the driver</li></ul></div>"
          "<div class='card'><h3>Handles</h3><ul><li>Online portal comparisons</li><li>Zero dep, Engine Protect, RSA</li><li>NCB, deductible, cashless</li></ul></div></div>"),
     "Aman explains the IDV change before the customer raises it, anchors the five thousand rupee saving, and matches add-ons to how the person drives.", 11),
    ("Test, fail, fix",
     page("<h2>Tested on Sarvam, rewritten from the failures</h2><div class='cols'><div class='card'><h3>Riya</h3><div class='big'>10 <span class='small'>of 25</span> &rarr; 18 <span class='small'>of 21</span></div><p class='small'>first draft, then after the rewrite</p><ul><li class='bad'>Leaked details to family</li><li class='bad'>Accepted a vague callback</li><li class='bad'>Read digits aloud</li></ul><p class='good'>Fix: hard stops, one step per reply</p></div>"
          "<div class='card'><h3>Aman</h3><div class='big'>11 <span class='small'>of 21</span> &rarr; 14 <span class='small'>of 18</span></div><p class='small'>first draft, then after the rewrite</p><ul><li class='bad'>Promised tools that are not connected</li><li class='bad'>Replies over 25 words</li><li class='bad'>No running total with add-ons</li></ul><p class='good'>Fix: brevity stop, indicative add-on prices</p></div></div>"),
     "I generated test suites on Sarvam. Riya went from ten of twenty five to eighteen of twenty one, and Aman from eleven of twenty one to fourteen of eighteen. The failures drove the rewrites: hard stops for Riya, and brevity plus a running total for Aman.", 14),
    ("Compliance by design",
     page("<h2>Compliance is in the prompt, not an afterthought</h2><table><tr><th>Risk</th><th>Rule in the prompt</th></tr><tr><td>Debt shared with family</td><td>Identity before any loan detail</td></tr>"
          "<tr><td>Threat of arrest or police</td><td>Explicit calm denial, grievance route</td></tr><tr><td>Customer in distress</td><td>Concern, callback in days, end</td></tr>"
          "<tr><td>Voicemail with debt message</td><td>Voicemail switched off</td></tr><tr><td>Invented prices or approvals</td><td>Locked facts, no claim guarantees</td></tr></table>"),
     "Compliance is built in. No loan details before identity, a calm denial of any arrest, distress ends the pitch, and voicemail is switched off.", 11),
    ("What is next",
     page("<h2>Status and next steps</h2><ul><li>Both agents committed on Sarvam</li><li>Prompts, harness, evidence and this video in the project</li><li>Next: phone numbers for live testing and a recorded tough-customer call per bot</li></ul>"
          "<p style='margin-top:36px' class='small'>github.com/Shaurya55555 | shaurya-bajpai.vercel.app</p>"),
     "Both agents are committed. Next are phone numbers for live testing and a recorded tough customer call for each bot. Thank you.", 9),
]


def render(narrate: bool) -> Path:
    tmp = Path(tempfile.mkdtemp())
    clips = []
    for i, (_, html, narration, secs) in enumerate(SCENES):
        h = tmp / f"s{i}.html"
        h.write_text(html, encoding="utf-8")
        png = tmp / f"s{i}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--window-size={W},{H}",
                        f"--screenshot={png}", h.as_uri()], check=True, capture_output=True)
        audio = None
        if narrate:
            sys.path.insert(0, str(ROOT / "sim"))
            import sarvam
            audio = tmp / f"s{i}.wav"
            audio.write_bytes(sarvam.tts(narration, "anand", lang="en-IN", model="bulbul:v3"))
            secs = max(secs, float(subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)],
                capture_output=True, text=True).stdout.strip()) + 0.8)
        clip = tmp / f"c{i}.mp4"
        cmd = ["ffmpeg", "-y", "-loop", "1", "-t", str(secs), "-i", str(png)]
        if audio:
            cmd += ["-i", str(audio), "-af", "apad", "-shortest"]
        cmd += ["-vf", "format=yuv420p,fade=t=in:st=0:d=0.4", "-r", "30", "-c:v", "libx264", str(clip)]
        if audio:
            cmd[-1:-1] = ["-c:a", "aac"]
        subprocess.run(cmd, check=True, capture_output=True)
        clips.append(clip)
    lst = tmp / "list.txt"
    lst.write_text("\n".join(f"file '{c.as_posix()}'" for c in clips), encoding="utf-8")
    out = OUT / ("walkthrough_narrated.mp4" if narrate else "walkthrough_captions.mp4")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)],
                   check=True, capture_output=True)
    return out


if __name__ == "__main__":
    print(render("--narrate" in sys.argv))
