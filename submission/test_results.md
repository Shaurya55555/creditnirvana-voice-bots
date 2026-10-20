# Test evidence (Sarvam automated tests, 21 Oct 2026)

| Agent | Run | Passed | Notes |
|---|---|---|---|
| Riya (loan settlement) | first generated suite | 10 of 25 | Failures: multi-step negotiation, 9 PM callback, police threat, family-member leak, distress, verbosity, digits aloud |
| Aman (car insurance) | first generated suite | 11 of 21 | Failures: references to unconnected tools, Engine Protect not pitched |

Prompts were revised after these runs (hard-stops block for Riya, tool references removed and add-on pitch tightened for Aman). Re-run scores are not available: the free Sarvam credit (about Rs 145 including the first runs) was exhausted.
Local harness (`sim/`) is built and verified for chat and text-to-speech; one full simulated Bot 1 call exists in `runs/` and showed the Rs 4,00,000 floor held with a confirmed date.
