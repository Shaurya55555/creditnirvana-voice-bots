# Design Note: CreditNirvana Voice Bot Assignment

Shaurya Bajpai | bajpaishaurya2911@gmail.com | +91-7985200306

## Approach
Both bots are voice-first prompts: short turns (about 25 words), spoken-form numbers, Hinglish that mirrors the customer's language, and explicit interruption handling. Each prompt has the same skeleton: role, one measurable goal with a fallback ladder, a locked set of case facts, tone, call flow, objection library, negotiation limits, compliance, and end-of-call outcome tags. Locking the facts and the floor inside the prompt stops the model inventing figures mid-call.

## Bot 1: Loan Settlement
- Conversion: a three-step ask ladder: full Rs 6,50,000, then Rs 4,00,000 lump sum within 7 days, then a split or token payment to lock the offer. The amount never goes below Rs 4,00,000; only timing and structure flex. The call never ends without a date.
- Excuses: every excuse gets a short acknowledgement, a call-out that it does not change the dues, and a return to "give me a date and an amount". The bot names the repeat pattern directly, which delivers the firm tone requested.
- Pressure without threats: consequences (credit-bureau impact, the lender's right to legal recovery, accruing interest) are stated once as facts, then the bot returns to the offer. Urgency comes from the real 7-day window and the Rs 2,50,000 saving.
- Compliance: 8 AM to 7 PM window, recorded-call disclosure, borrower verification before any detail, no third-party disclosure, no abuse, no invented legal action, grievance route on dispute, and a distress exit.

## Bot 2: Car Insurance Renewal
- Conversion: consultative opening, IDV change explained before the customer raises it, discount anchored at Rs 5,000 saved (about Rs 40 a day), then 2 to 3 add-ons matched to discovery answers. Fallbacks: fewer add-ons, base renewal, payment link with a committed time.
- IDV as a pitch: the Rs 1,00,000 drop is explained as depreciation, then used to sell Return to Invoice and Zero Depreciation.
- Price comparison: the bot invites a like-for-like check (same IDV, same add-ons, garage network, claim handling) and never disparages competitors or invents their price.
- Policy questions: comprehensive vs third party, NCB and cashless are answered directly; anything uncertain is sent in writing on WhatsApp instead of guessed.
- Compliance: no false claim guarantees, no invented discounts or prices, add-ons stated as optional, payment only through an official link, never OTP or card details on the call.

## Assumptions
Add-on prices were not provided, so the bot uses clearly indicative figures (Zero Depreciation about Rs 2,500, Engine Protect about Rs 1,200, Roadside Assistance about Rs 600) and says the exact amount is on the WhatsApp quote. Lender and insurer names are placeholders. No tools are connected, so each bot promises the payment link by SMS and WhatsApp rather than sending it.

## Testing and what it changed
I generated an automated suite on Sarvam for each agent (AI-written tough-customer scenarios with behaviour checks), ran it, and rewrote the prompts from the failures.
- Riya: 10 of 25 on the first draft, then 18 of 21 and 17 of 21. Fixes: a hard-stops block (identity before any loan detail, distress ends the pitch, calling hours, "no arrest" reassurance, the floor, spoken numbers, two short sentences), one negotiation step per reply, a discount request as the cue to present Rs 4,00,000, no vague callbacks, exact repetition of the customer's date. One test expects collection to continue after "my mother is in the ICU"; I kept the pitch ending there because that is the compliant behaviour.
- Aman: 11 of 21 on the first draft, then 12 of 18 and 14 of 18. Fixes: phantom tool references removed, Zero Depreciation plus Engine Protect for city driving, a hard brevity stop, indicative add-on prices so a running total can be stated, no "I will check with the team", an explicit do-not-call acknowledgement, Return to Invoice as the answer to the IDV drop.
- Voicemail is off on the loan bot so a debt message is never left with a third party.
Suites are AI-generated and scores vary a point or two per run. The last prompt revision was committed but could not be re-run, so its score is not claimed.
