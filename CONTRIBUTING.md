# Contributing

Thanks for helping improve Astrolabe. The most useful contributions are better tasks, sharper criteria, lawyer review and new runs.

## Ways to contribute

1. **Lawyer review.** Check a task's criteria against its sources and add a review record (see below).
2. **Add or improve a task.** A client matter with source texts, a short deliverable and pass/fail criteria.
3. **Sharpen criteria.** Make a criterion more concrete, one fact per criterion.
4. **Add exact-text questions.** Articles, decrees or fatwas, with the exact reference text.
5. **Add a run.** A new model or setting, with the full run record.

## Ground rules

- **Source texts come from Dike or another public official source you can name.** Say where each text came from in your PR. No texts from Najiz.
- **Client facts are invented.** No real people, companies, cases or confidential material.
- **Keep tasks self-contained.** Everything the model needs is in the task folder.
- **No secrets.** Never commit keys, tokens, database addresses or `.env` files.
- **Small pull requests.** One task, one review or one run per PR.
- Run `python scripts/validate_tasks.py` before opening a PR. CI runs the same check.

## Task format

```text
tasks/<country>-<area>/<task-slug>/
├── task.json
└── documents/
    ├── client-facts.txt
    └── source-1.txt, source-2.txt, ...
```

The folder is `egypt-<area>` or `saudi-<area>`, and the slug is lowercase words joined by hyphens.
`task.json` follows the [Harvey LAB](https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark) format. This is a real one, shortened:

```json
{
  "title": "Formal and Substantive Conditions for Inter-Authority Dispute Jurisdiction",
  "work_type": "analyze",
  "tags": ["Egypt", "civil procedure and litigation", "فتوى رقم 373 - بتاريخ 2020/12/12"],
  "instructions": "أنت محامٍ يقدّم المشورة لعميلك. اطّلع على المستندات المرفقة ... واكتب باللغة العربية.",
  "deliverables": { "advice-note.md": "advice-note.md" },
  "criteria": [
    {
      "id": "C-001",
      "title": "Jurisdiction over inter-authority disputes",
      "match_criteria": "PASS if the note states that ... FAIL if the note does not state that ...",
      "deliverables": ["advice-note.md"],
      "sources": ["client-facts.txt", "source-1.txt"]
    }
  ],
  "metadata": {
    "astrolabe_id": "AST-114",
    "status": "draft, not lawyer reviewed",
    "source_ids": ["eg-fatwa-15743#1", "eg-fatwa-15743#2"]
  }
}
```

- `work_type` is `analyze` and `deliverables` is always `advice-note.md`.
- `tags` has three entries: the country (`Egypt` or `Saudi`), the practice area, and a label for the source (for example the fatwa number and date, or the law's name).
- `instructions` are in Arabic. Copy the wording from an existing task.
- `metadata.astrolabe_id` is a unique `AST-` plus three digits. `source_ids` lists the sources the task was built from.
- `metadata.status` is `draft, not lawyer reviewed` until a lawyer reviews it, then `approved`.
- Each task has 3 to 8 criteria (existing tasks have 3 to 6). Criteria ids run `C-001`, `C-002`, ...
- `client-facts.txt` holds the invented client facts and the questions to answer. It is listed in every criterion's `sources`.

## Writing good criteria

- Each criterion is `PASS if ... FAIL if ...`, and both parts are required.
- One checkable fact per criterion. Do not bundle two rules into one.
- A reader should understand what a pass needs from `match_criteria` alone.
- Every criterion lists the files it relies on under `sources`, and always includes `client-facts.txt`.
- A criterion must be supported by the source texts in the folder. Do not require knowledge that is not in them.
- Names and numbers must match the sources exactly.

A task is fully passed only when every criterion passes under both judges, so a vague or wrong criterion fails the whole task.

## Lawyer review

A reviewer checks every criterion against its sources and the law, fixes wording, and adds a record to `task.json`. `status` changes from `draft, not lawyer reviewed` to `approved`:

```json
"metadata": {
  "status": "approved",
  "review": {
    "reviewer": "Name",
    "date": "2026-11-23",
    "outcome": "approved",
    "changes": ["what was changed"],
    "notes": "what was verified"
  }
}
```

If a reviewer prefers not to be named, say so in the PR and we will record the review without a name.
Tasks without a review record are drafts.

## Exact-text questions

Add a line to `data/exact-text/questions.jsonl` with `id`, `jurisdiction`, `type`, `question`, `reference` and `canonical_id`.
The reference is the exact text. Scoring is by code: right when the answer has at least 60% of the reference words and at least 80% of its numbers.

## Adding a run

Put one JSON per run in `results/tasks/`, named `<task-slug>.<setting>.json`, with the transcript, metrics and both judges' verdicts.
State the model, the setting (no data or files only) and the date in the PR. Report the share of criteria that **both** judges passed.

## Licences

By contributing you agree that code is under Apache-2.0 and data (questions, tasks, criteria, run records) is under CC BY 4.0.
Source texts keep their publishers' terms. See `NOTICE.md`.
