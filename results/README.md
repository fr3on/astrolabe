Each file is one run: `<task>.<model-setting>.json`. `sonnet46` is files only, `sonnet46nodata` is no data.
Fields: `metrics` (turns, tokens, seconds), `answer` (the advice note), `judges` (per-criterion verdicts from both judges),
`dual` (stored scores; use the share of criteria **both** judges passed as the headline), and the full transcript.
