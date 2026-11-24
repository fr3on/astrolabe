# Scoring notes

How the exact-text rule behaves, and how much the headline numbers depend on it. The rule itself is in [`code/score.py`](../code/score.py): an answer is right when it contains at least 60% of the reference words (ignoring words the question already gives away) and every number in the reference.

## Does the 60% cutoff matter?

The same answers scored at other cutoffs, with the number rule unchanged. "From memory" is 0 of 209 for every model at every cutoff (Gemini 4 Argon gets 1 if the number rule is dropped), so only the with-the-text results change.

| Model | 50% | **60% (used)** | 70% | 80% | 60%, words only |
|---|---|---|---|---|---|
| Claude Sonnet 4.6 | 84% | **82%** | 73% | 57% | 88% |
| Gemini 4 Neon | 96% | **96%** | 96% | 91% | 99.5% |
| Gemini 4 Argon | 92% | **91%** | 90% | 86% | 97% |
| Gemini 4 Hydrogen | 97% | **97%** | 97% | 94% | 100% |

The order of the models does not change at 50%, 60% or 70%, and the cutoff moves the headline by at most 2 points between 50% and 60%. At 80% the gap widens: Claude Sonnet 4.6 falls to 57% while the Gemini models stay between 86% and 94%, so a strict cutoff favours the models that quote the text more closely. The number rule matters more: it is what separates the models, because most misses have nearly all the words but lack a number.

**One number-rule effect, checked.** All 7 of Gemini 4 Hydrogen's misses, and 6 of Claude Sonnet 4.6's, are one case: the reference starts "مادة ١" and the answer writes "المادة الأولى", so the number 1 is not found. Counting "المادة الأولى" as 1 in the answer (the reference side unchanged) would move Hydrogen from 202 to 209 (97% to 100%) and Claude Sonnet 4.6 from 171 to 177 (82% to 85%), and would not change Gemini 4 Neon (201) or Gemini 4 Argon (191). The published numbers keep the original rule, so they stay comparable with Claude Sonnet 5.5 and Opus 5.5.

Claude Sonnet 5.5 and Opus 5.5 are not in this table because their raw exact-text answers were not saved as files, only the pass or fail per question. Any change to the scoring rule can therefore be applied to the other four models but not to those two, and their batched setup (up to 24 questions per reply) may also differ from the others.


## Judge check

Both task judges are Claude models. To check for a judge effect, Gemini 4 Neon graded the 208 criteria of Claude Opus 5.5's advice notes with the same judge prompt. It agreed with the two Claude judges (both must pass) on 206 of 208 criteria (99%): 202 passes on each side, with one criterion Neon failed and Claude passed, and one the other way. This is one model's notes and one Gemini judge.
