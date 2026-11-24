#!/usr/bin/env python3
"""Score answers to the Astrolabe exact-text questions. Code only, no model judge.

An answer is **correct** when both hold:
  * recall: it contains at least `--min-recall` (default 60%) of the reference words,
    ignoring words the question already gives away;
  * numbers: it contains at least `--min-number` (default 80%) of the numbers in the
    reference (skipped when the reference has no number).

An answer that says "I don't know" (and has under 50% word recall) is **declined**.
Everything else is **wrong_or_partial**. A question with no answer is **missing**.

Usage:
    python3 code/score.py ANSWERS --questions data/exact-text/questions.jsonl

ANSWERS is either a JSONL file with one {"id": ..., "answer": ...} per line, or a
folder with one `<id>.txt` file per question.
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

DEFAULT_MIN_RECALL = 0.6
DEFAULT_MIN_NUMBER = 0.8
DECLINE_RECALL = 0.5  # an answer with at least this recall is never counted as a decline
DECLINE_PHRASES = ("لا اعلم", "لا أعلم", "لا استطيع", "غير متاكد", "don't know", "do not know")

_DIACRITICS = re.compile(r"[ً-ْـ]")  # harakat and tatweel
_ALEF = re.compile("[أإآ]")
_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def norm(text):
    """Normalise Arabic text: strip diacritics, unify alef/yeh/teh marbuta, Western digits, no punctuation."""
    text = _DIACRITICS.sub("", text or "")
    text = _ALEF.sub("ا", text).replace("ى", "ي").replace("ة", "ه")
    text = text.translate(_DIGITS)
    return re.sub(r"[^\w\s]", " ", text)


def toks(text):
    """Words of three or more characters, after normalisation."""
    return [t for t in norm(text).split() if len(t) >= 3]


def nums(text):
    """The set of numbers in the text, after normalisation."""
    return set(re.findall(r"\d+", norm(text)))


def score_answer(question, reference, answer, min_recall=DEFAULT_MIN_RECALL, min_number=DEFAULT_MIN_NUMBER):
    """Score one answer. Returns (label, word_recall, number_recall); number_recall is None if the reference has no number."""
    answer = answer or ""
    gold = set(toks(reference)) - set(toks(question)) or set(toks(reference))
    recall = len(gold & set(toks(answer))) / max(1, len(gold))
    ref_nums = nums(reference)
    number_recall = len(ref_nums & nums(answer)) / len(ref_nums) if ref_nums else None
    declined = any(norm(p) in norm(answer) for p in DECLINE_PHRASES) and recall < DECLINE_RECALL
    if declined:
        label = "declined"
    elif recall >= min_recall and (number_recall is None or number_recall >= min_number):
        label = "correct"
    else:
        label = "wrong_or_partial"
    return label, recall, number_recall


def load_questions(path):
    with open(path, encoding="utf-8") as f:
        return {q["id"]: q for q in map(json.loads, (line for line in f if line.strip()))}


def load_answers(path):
    """Answers from a JSONL file ({"id", "answer"}) or a folder of <id>.txt files."""
    path = Path(path)
    if path.is_dir():
        return {p.stem: p.read_text(encoding="utf-8") for p in sorted(path.glob("*.txt"))}
    with open(path, encoding="utf-8") as f:
        return {r["id"]: r.get("answer") or "" for r in map(json.loads, (line for line in f if line.strip()))}


def score_all(questions, answers, **thresholds):
    """Score every question. Returns a list of dicts, one per question, in question order."""
    rows = []
    for qid, q in questions.items():
        row = {"id": qid, "jurisdiction": q["jurisdiction"], "type": q["type"]}
        if qid not in answers:
            rows.append({**row, "label": "missing", "recall": None, "number_recall": None})
            continue
        label, recall, number_recall = score_answer(q["question"], q["reference"], answers[qid], **thresholds)
        rows.append({**row, "label": label, "recall": recall, "number_recall": number_recall})
    return rows


def summarise(rows):
    """Counts per label, overall and per (jurisdiction, type)."""
    overall = collections.Counter(r["label"] for r in rows)
    by_group = collections.defaultdict(collections.Counter)
    for r in rows:
        by_group[(r["jurisdiction"], r["type"])][r["label"]] += 1
    return overall, by_group


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("answers", help="JSONL file of {id, answer} lines, or a folder of <id>.txt files")
    ap.add_argument("--questions", default="data/exact-text/questions.jsonl", help="questions file (default: %(default)s)")
    ap.add_argument("--min-recall", type=float, default=DEFAULT_MIN_RECALL, help="share of reference words needed (default: %(default)s)")
    ap.add_argument("--min-number", type=float, default=DEFAULT_MIN_NUMBER, help="share of reference numbers needed (default: %(default)s)")
    ap.add_argument("--details", action="store_true", help="print one line per question")
    ap.add_argument("--json", metavar="OUT", help="also write the per-question results to this JSON file")
    args = ap.parse_args(argv)

    questions = load_questions(args.questions)
    answers = load_answers(args.answers)
    extra = sorted(set(answers) - set(questions))
    if extra:
        print(f"warning: {len(extra)} answer id(s) not in the questions file, ignored: {', '.join(extra[:5])}", file=sys.stderr)
    rows = score_all(questions, answers, min_recall=args.min_recall, min_number=args.min_number)

    if args.details:
        for r in rows:
            rec = "-" if r["recall"] is None else f"{r['recall']:.2f}"
            num = "-" if r["number_recall"] is None else f"{r['number_recall']:.2f}"
            print(f"{r['id']:8} recall={rec} num={num} {r['label']}")
        print()
    overall, by_group = summarise(rows)
    for (jur, typ), c in sorted(by_group.items()):
        print(f"{jur:6} {typ:8} {c['correct']:3}/{sum(c.values()):3} correct  (declined {c['declined']}, wrong or partial {c['wrong_or_partial']}, missing {c['missing']})")
    total = len(rows)
    print(f"{'ALL':15} {overall['correct']:3}/{total:3} correct = {100 * overall['correct'] / max(1, total):.1f}%  "
          f"(declined {overall['declined']}, wrong or partial {overall['wrong_or_partial']}, missing {overall['missing']})")
    if args.json:
        Path(args.json).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
