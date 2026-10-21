"""Build submission PDFs from the markdown sources using python-markdown + headless Chrome.

python submission/build_pdfs.py
"""
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "submission"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
NOTE = OUT / "design_note.md"

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: Calibri, Arial, sans-serif; font-size: 10.5pt; line-height: 1.38; color: #111; }
h1 { font-size: 17pt; margin: 0 0 4pt; border-bottom: 2px solid #222; padding-bottom: 3pt; }
h2 { font-size: 12.5pt; margin: 12pt 0 3pt; color: #1a3a6b; }
ul { margin: 2pt 0 4pt 16pt; padding: 0; } li { margin: 1.5pt 0; }
p { margin: 3pt 0; } code { background: #f1f1f1; padding: 0 2px; }
.cover { margin-bottom: 8pt; font-size: 10pt; color: #333; }
.pb { page-break-before: always; }
"""

LIST_START = re.compile(r"([^\n])\n(?=\s*(?:[-*] |\d+\. ))")


def md(text: str) -> str:
    """python-markdown needs a blank line before a list; the sources do not have one."""
    text = LIST_START.sub(r"\1\n\n", text)
    return markdown.markdown(text, extensions=["tables", "sane_lists"])


def page(body: str) -> str:
    return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


def to_pdf(html_text: str, name: str) -> Path:
    h = OUT / f"{name}.html"
    h.write_text(html_text, encoding="utf-8")
    pdf = OUT / f"{name}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", h.as_uri()], check=True, capture_output=True)
    h.unlink()
    return pdf


def main() -> None:
    cover = ("<div class='cover'><b>Shaurya Bajpai</b> | bajpaishaurya2911@gmail.com | +91-7985200306 | "
             "Assignment: two Sarvam voice bots for CreditNirvana (Voice Labs)</div>")
    b1 = (ROOT / "prompts" / "bot1_loan_settlement.md").read_text(encoding="utf-8")
    b2 = (ROOT / "prompts" / "bot2_car_insurance.md").read_text(encoding="utf-8")
    print(to_pdf(page(cover + md(b1) + "<div class='pb'></div>" + md(b2)), "Shaurya_Bajpai_System_Prompts"))
    compact = "<style>@page{margin:12mm 14mm} body{font-size:9.4pt;line-height:1.28} h2{margin:8pt 0 2pt}</style>"
    print(to_pdf(page(compact + md(NOTE.read_text(encoding="utf-8"))), "Shaurya_Bajpai_Design_Note"))


if __name__ == "__main__":
    sys.exit(main())
