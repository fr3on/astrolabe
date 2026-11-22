#!/usr/bin/env python3
"""Deterministic scoring of a run file: gold-token recall, number recall, decline detection. No LLM judge."""
import json, re, sys, collections
def norm(s):
    s = re.sub(r"[ً-ْـ]", "", s or "")
    s = re.sub("[أإآ]", "ا", s).replace("ى", "ي").replace("ة", "ه")
    s = s.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    return re.sub(r"[^\w\s]", " ", s)
def toks(s): return [t for t in norm(s).split() if len(t) >= 3]
def nums(s): return set(re.findall(r"\d+", norm(s)))
DECLINE = ("لا اعلم", "لا أعلم", "لا استطيع", "غير متاكد", "don't know", "do not know")
if __name__ == '__main__':
    _d = json.load(open(sys.argv[2]))
    gold = {g["id"]: g["gold"] for g in _d["G"]}
    quest = {q["id"]: q["q"] for q in _d["Q"]}
    rows = [json.loads(l) for l in open(sys.argv[1])]
    agg = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        ans = r["answer"] or ""; g = gold[r["id"]]
        gt = set(toks(g)) - set(toks(quest[r["id"]])) or set(toks(g));  # ignore words the question already gave away
        rec = len(gt & set(toks(ans))) / max(1, len(gt))
        gn = nums(g); nrec = (len(gn & nums(ans)) / len(gn)) if gn else None
        declined = any(norm(x) in norm(ans) for x in DECLINE) and rec < 0.5
        label = "declined" if declined else "correct" if rec >= 0.6 and (nrec is None or nrec >= 0.8) else "wrong_or_partial"
        agg[(r["model"], r["arm"], r["id"][:2])][label] += 1
        print(r["id"], r["arm"], f"recall={rec:.2f}", "num=" + ("-" if nrec is None else f"{nrec:.2f}"), label)
    print()
    for k, v in sorted(agg.items()): print(k, dict(v))
