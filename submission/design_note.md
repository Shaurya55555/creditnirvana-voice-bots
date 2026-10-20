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
Add-on prices were not provided, so the bot does not quote exact prices. Lender and insurer names and the payment-link and logging tools are placeholders wired in on Sarvam.

## Testing and what it changed
I generated an automated test suite on Sarvam for each agent (AI-written tough-customer scenarios with expected behaviours) and used the failures to rewrite the prompts.
- Riya, first run: 10 of 25 passed. Core money paths held (full payment, the Rs 4,00,000 floor, job-loss and "already paid" excuses, wrong number, self-harm distress). Failures: multi-step negotiation, a 9 PM call, calming a "police" threat, leaking loan details to a family member, not stopping collection on hospitalisation or bereavement, long replies, and reading digits aloud.
- Fix: a "hard stops" block that overrides everything (identity before any loan detail, distress ends the pitch, calling hours, explicit "no arrest" reassurance, floor, amounts spoken in words, two short sentences) plus a one-step-per-reply negotiation rule.
- Aman, first run: 11 of 21 passed. Most failures were the prompt naming payment and logging tools that were not connected, and Engine Protect not pitched for city drivers.
- Fix: removed the tool references (the bot now promises the link by SMS and WhatsApp only), and made Zero Depreciation plus Engine Protect the default pitch for city, traffic and rain.
- Voicemail is switched off on the loan bot so a debt message can never be left with a third party.
Re-run scores after these fixes were not completed before the free credit ran out, so I am not claiming them.
