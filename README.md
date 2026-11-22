# Astrolabe

<p align="center">
  <img src="docs/assets/hero.svg" alt="Astrolabe: a benchmark of Arabic law" width="100%">
</p>

<p align="center">
  <img alt="Code: Apache-2.0" src="https://img.shields.io/badge/code-Apache--2.0-2E7D32?style=flat-square">
  <img alt="Data: CC BY 4.0" src="https://img.shields.io/badge/data-CC%20BY%204.0-2E7D32?style=flat-square">
  <a href="https://github.com/fr3on/astrolabe/actions/workflows/validate.yml"><img alt="Validate data" src="https://github.com/fr3on/astrolabe/actions/workflows/validate.yml/badge.svg?branch=main"></a>
  <a href="CONTRIBUTING.md"><img alt="Contributions welcome" src="https://img.shields.io/badge/contributions-welcome-0E7C7B?style=flat-square"></a>
</p>

<p align="center">
  <img alt="Jurisdictions: Saudi Arabia and Egypt" src="https://img.shields.io/badge/jurisdictions-Saudi%20Arabia%20%C2%B7%20Egypt-0E7C7B?style=flat-square">
  <img alt="44 tasks" src="https://img.shields.io/badge/tasks-44-4F46E5?style=flat-square">
  <img alt="209 exact-text questions" src="https://img.shields.io/badge/questions-209-4F46E5?style=flat-square">
  <img alt="Lawyer reviewed: 16 of 44 tasks" src="https://img.shields.io/badge/lawyer%20reviewed-16%2F44-B45309?style=flat-square">
  <img alt="Format: Harvey LAB" src="https://img.shields.io/badge/format-Harvey%20LAB-111827?style=flat-square">
</p>

A benchmark of Arabic law. The first release covers Saudi Arabia and Egypt.

Do language models know the law, or do they only sound like they do? Astrolabe tests two things:

1. **Exact-text questions (209).** The model is asked for the exact wording of an article, decree or fatwa. Scored by code, with no model in the loop.
2. **Client-matter tasks (44, 208 criteria).** A model writes a short advice note for a client. Each task has pass/fail criteria in the [Harvey LAB](https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark) format, graded by two model judges. A criterion counts only when both judges pass it.

Each is run two ways: **no data** (from memory) and **files only** (the source text is given).

## Results

With the source text, all three models pass about 97% of the task criteria. Without it, no model got more than 1 of the 209 exact-text questions right.

| Model | Setting | Exact text right | Criteria passed | Tasks fully passed |
|---|---|---|---|---|
| Claude Sonnet 4.6 | No data | 0% (0 of 209) | 38% (78 of 208) | 2 of 44 |
| Claude Sonnet 4.6 | With the text | 82% (171 of 209) | **97%** (202 of 208) | **41 of 44** |
| Claude Sonnet 5.5 | No data | 0% (0 of 209) | 35% (72 of 208) | 1 of 44 |
| Claude Sonnet 5.5 | With the text | **90%** (189 of 209) | **97%** (201 of 208) | 38 of 44 |
| Claude Opus 5.5 | No data | 0.5% (1 of 209) | not run | not run |
| Claude Opus 5.5 | With the text | 88% (184 of 209) | **97%** (202 of 208) | 38 of 44 |

- **No data:** the model answers from memory. **With the text:** the source texts are in the prompt.
- **Criteria passed:** a criterion counts only when both judges pass it. Each model was run once. Bold marks the best score among the "With the text" rows (ties are all bold).
- **Sonnet 5.5 and Opus 5.5:** these answered four tasks per reply, with no tools, so they have no trajectory and the comparison with Sonnet 4.6 is not exact. Their exact-text questions were answered in batches of up to 24, with and without the text; the task notes were run with the text only.
- The models read the law well and do not remember it. 16 of the 44 tasks were reviewed by a lawyer; the rest are drafts.

## Scoring

- **Exact text:** right when the answer contains at least 60% of the reference words and every number in it.
- **Tasks:** the two judges are Claude Sonnet 4.6 and Claude Opus 4.6. The judge prompt is the unchanged Harvey LAB rubric template.

## Status and limits

Three models, one run each, two legal systems. Run scripts for the exact-text questions and the Dike search check are not in this release yet.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Lawyer review, new tasks and new runs are the most useful.

## Licences

- Code: Apache-2.0 (`LICENSE`).
- Questions, tasks, criteria and run records: CC BY 4.0 (`LICENSE-DATA.md`).
- Source texts (laws, decrees, fatwas) keep the terms of their original publishers and of Dike. See `NOTICE.md`.
