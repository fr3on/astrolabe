Each file is one run: `<task>.<model-setting>.json`. `sonnet46` is Claude Sonnet 4.6 with the files, `sonnet46nodata` is the same model without data, `sonnet55` is Claude Sonnet 5.5 and `opus55` is Claude Opus 5.5, both with the files (four tasks per reply, no tools). These records are answer only: the transcript is empty and there are no token counts.
Fields: `metrics` (turns, tokens, seconds), `answer` (the advice note), `judges` (per-criterion verdicts from both judges),
`dual` (stored scores; use the share of criteria **both** judges passed as the headline), and the full transcript.
