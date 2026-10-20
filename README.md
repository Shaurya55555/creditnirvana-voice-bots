# CreditNirvana voice bot assignment

Two Sarvam voice agents: Bot 1 personal loan settlement (Riya), Bot 2 car insurance renewal (Aman).

- `prompts/`: the system prompts (source of truth, pasted into Sarvam)
- `sim/`: test harness. LLM tough customers call the prompts, an LLM judge scores them on CreditNirvana's four criteria (human-like, objection handling, compliance, conversion), plus code checks for banned words and the Rs 4,00,000 floor
- `PLATFORM_SETUP.md`: exact clicks and settings on indus.sarvam.ai, number rental, recordings
- `runs/`: transcripts, scores, audio
- `submission/`: PDFs and the reply email

## Run
```
pip install requests
copy .env.example .env      # put SARVAM_API_KEY in it
python sim/run.py all
python sim/render_audio.py runs/<file>.json
```
