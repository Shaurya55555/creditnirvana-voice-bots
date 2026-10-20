# Sarvam Voice Agents: exact setup for both bots

Platform: https://indus.sarvam.ai (log in, open Voice Agents). Build > Agents > Create from Scratch.
Docs used: voice-agents quickstart, conversation settings, variables, telephony (rent-from-sarvam).

## Common settings (both bots)
- Instructions tab: paste the matching file from `prompts/`. In the pasted text replace `{name}`, `{lender}`, `{insurer}` with `@` variables (type `@` in the canvas and pick the chip).
- Settings > Language personalisation: starting language Hindi, "Switch language during call" ON, allowed: Hindi, English.
- Settings > Listening: Let callers interrupt ON. Eagerness: Normal. Nudge quiet callers: 1 nudge at 6s ("Hello, aap line pe hain?"), hang up after 2 unanswered nudges. Max call length: 8 minutes.
- Model temperature: 0.3. TTS: Bulbul v4 if listed (v3 reaches end of life on Voice Agents on 10 Nov 2026), pick one female voice for Riya (Bot 1) and one male voice for Aman (Bot 2).
- Test with "test agent" before deploying. Deployments use a committed version, so commit before assigning a number.

## Bot 1: Riya (loan settlement)
- Variables: `customer_name` (default "Rahul Mehta"), `lender_name` (default "Capital Trust Finance").
- Greeting: `Namaste, kya main @customer_name ji se baat kar rahi hoon? Main Riya, @lender_name ke recovery desk se. Yeh call recorded hai.`
- Turn the recorded-call disclosure into a non-interruptible greeting if the toggle exists.

## Bot 2: Aman (car insurance renewal)
- Variables: `customer_name` (default "Vikram Singh"), `insurer_name` (default "SecureDrive General Insurance").
- Greeting: `Hello @customer_name ji, main Aman, @insurer_name se. Yeh call recorded hai. Aapki Brezza ke renewal ke baare mein do minute baat kar sakte hain?`

## Phone numbers for the reply email (Deploy > Phone Numbers)
1. Add Connection > Rent from Sarvam > Individual > complete KYC (mandatory, takes time: start today).
2. Buy 2 numbers (paid from the Sarvam wallet; rental is 30 days with no grace period on renewal).
3. Deploy > Inbound Calls: assign number A to Bot 1, number B to Bot 2.
4. Call both from your own phone once. Put those two numbers in the reply email. Inbound defaults the variables, so the bot works for any caller.
5. For outbound (they may prefer the bot to call them): Deploy > Outbound Campaigns, CSV with columns customer_name plus the lender/insurer names.

## Recordings (2 to 5 minutes each)
- Real phone call: call your inbound number as a tough customer, then Monitor > Agent Analytics > Call Logs shows call, transcript, recording.
- Simulated: `python sim/run.py bot1_excuse_machine` then `python sim/render_audio.py runs/<file>.json`. Label these "simulated customer" when sending. A real phone recording is stronger evidence; use the simulated one only as backup.

## Pre-submission checklist
- [ ] Both agents committed and tested in "test agent"
- [ ] Two numbers live and verified by calling them
- [ ] One 2 to 5 minute recording per bot (tough customer)
- [ ] prompts PDF, design note, scorecard in `submission/`
- [ ] Reply sent on the original thread before 27 Oct 2026 11:59 PM IST
