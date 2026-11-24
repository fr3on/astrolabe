# Scorer for the exact-text questions

`score.py` scores answers to the 209 exact-text questions in [`data/exact-text/questions.jsonl`](../data/exact-text/questions.jsonl). It uses code only, with no model judge, and needs only the Python 3 standard library.

## The rule

An answer is **correct** when both hold:

1. **Words:** it contains at least **60%** of the words in the reference, ignoring words the question already gives away.
2. **Numbers:** it contains at least **80%** of the numbers in the reference. This is skipped when the reference has no number.

Before comparing, text is normalised: diacritics and tatweel are removed, alef forms (أ إ آ) become ا, ى becomes ي, ة becomes ه, Arabic-Indic digits become Western digits, and punctuation is dropped. Only words of three or more characters count.

Other labels:

- **declined:** the answer says "I don't know" (or similar) and has under 50% word recall.
- **wrong_or_partial:** everything else.
- **missing:** the question has no answer.

Both thresholds can be changed with `--min-recall` and `--min-number`. The defaults are the rule used for every published result.

## Usage

From the repository root:

```bash
python3 code/score.py ANSWERS
```

`ANSWERS` is one of:

- a JSONL file with one `{"id": "T1-1", "answer": "..."}` per line, or
- a folder with one `<id>.txt` file per question (for example `T1-1.txt`).

Options:

| Option | What it does |
|---|---|
| `--questions PATH` | Questions file (default `data/exact-text/questions.jsonl`) |
| `--min-recall X` | Share of reference words needed (default `0.6`) |
| `--min-number X` | Share of reference numbers needed (default `0.8`) |
| `--details` | Print one line per question with its recall and label |
| `--json OUT` | Also write the per-question results to a JSON file |

Example output:

```text
Egypt  article   33/ 33 correct  (declined 0, wrong or partial 0, missing 0)
Egypt  decree    39/ 47 correct  (declined 0, wrong or partial 8, missing 0)
Egypt  fatwa     49/ 54 correct  (declined 0, wrong or partial 5, missing 0)
Saudi  article   70/ 75 correct  (declined 0, wrong or partial 5, missing 0)
ALL             191/209 correct = 91.4%  (declined 0, wrong or partial 18, missing 0)
```

## As a library

```python
from score import score_answer

label, word_recall, number_recall = score_answer(question, reference, answer)
```

## Tests

```bash
python3 -m unittest discover -s code
```

How the results change with other thresholds, and with the "مادة ١" versus "المادة الأولى" case, is in [`docs/SCORING.md`](../docs/SCORING.md).
