# Per-model notes

Details behind the results tables in the [README](../README.md).

## Claude Sonnet 4.6
Run with the agent harness on AWS Bedrock; full run records (transcript, metrics, both judges) are in `results/tasks/`.

## Claude Sonnet 5.5 and Opus 5.5
They answered four tasks per reply with no tools, so there is no trajectory and the comparison with Sonnet 4.6 is not exact. Their exact-text questions were answered in batches of up to 24, with and without the text. Task runs exist in both settings; the run records are answer only.

## Gemini 4 Neon
One agent run, with the same 209 questions and the same scoring rule.
- **Exact text:** 0% from memory, 96% with the text. Seven of its eight misses fail only because the article number ("مادة ١ -") is missing from the answer; the Claude models miss almost the same questions.
- **Tasks:** graded with the same two judges as the Claude models. With the text: 202 of 208 criteria and 40 of 44 tasks. From memory (facts only, no source text): 146 of 208 criteria and 10 of 44 tasks.
- **From-memory score:** far above the Claude models' 35–51%, and Gemini 4 Argon lands in the same place. Both ran as agents with tools and were told to use no web or search. Tool use was not logged, but a check of the from-memory notes found no sign of searching: only 13 of Neon's 77 cited article numbers appear in the source text, and the notes rarely copy its wording.

## Gemini 4 Argon
Same exact-text run as Neon.
- **Exact text:** it answered "I don't know" to 203 of 209 questions from memory (0%); 91% with the text.
- **Tasks:** 203 of 208 criteria and 40 of 44 tasks with the text; 151 of 208 criteria and 14 of 44 tasks from memory.

## Gemini 4 Hydrogen
Same exact-text run as Neon.
- **Exact text:** it answered "I don't know" to all 209 questions from memory; 97% with the text. All 7 of its misses have 87–96% of the reference words and fail only on the number check.
- **Tasks:** from memory (facts only, no source text) it passed 121 of 208 criteria and 3 of 44 tasks. That is lower than Neon (70%) and Argon (73%) but still above the Claude average of 41%. The with-the-text notes are not run yet.
