"""Turn a simulated transcript JSON into a two-voice call recording (mp3) with Sarvam Bulbul TTS + ffmpeg.

python sim/render_audio.py runs/<file>.json
These are simulated-customer recordings. Label them as such when submitting.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sarvam

VOICES = {"bot1": ("priya", "rahul"), "bot2": ("aditya", "rohan")}  # (agent voice, customer voice); adjust to your v3 voice list


def main(path: str) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    agent_v, cust_v = VOICES[data["bot"]]
    tmp = Path(tempfile.mkdtemp())
    gap = tmp / "gap.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.45", str(gap)],
                   check=True, capture_output=True)
    parts = []
    for i, (who, text) in enumerate(data["transcript"]):
        wav = tmp / f"{i:03d}.wav"
        wav.write_bytes(sarvam.tts(text, agent_v if who == "bot" else cust_v,
                                   pace=1.05 if who == "bot" else 0.95))
        parts += [wav, gap]
    lst = tmp / "list.txt"
    lst.write_text("\n".join(f"file '{p.as_posix()}'" for p in parts), encoding="utf-8")
    out = Path(path).with_suffix(".mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "24000", str(out)],
                   check=True, capture_output=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                         capture_output=True, text=True).stdout.strip()
    print(out, f"{float(dur):.0f}s")


if __name__ == "__main__":
    main(sys.argv[1])
