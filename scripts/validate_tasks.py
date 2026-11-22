"""Validate the Astrolabe data. Standard library only.

  python scripts/validate_tasks.py

Checks every task folder, the exact-text questions and the run records. Exits 1 on any problem.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []
seen_ids: set[str] = set()
DRAFT = "draft, not lawyer reviewed"


def err(msg: str) -> None:
    errors.append(msg)


def check_task(tj: Path) -> None:
    rel = tj.parent.relative_to(ROOT)
    try:
        t = json.loads(tj.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return err(f"{rel}: task.json is not valid JSON ({e})")
    for k in ("title", "work_type", "instructions", "deliverables", "criteria", "metadata"):
        if k not in t:
            err(f"{rel}: missing '{k}'")
    if t.get("work_type") != "analyze":
        err(f"{rel}: work_type must be 'analyze'")
    if t.get("deliverables") != {"advice-note.md": "advice-note.md"}:
        err(f"{rel}: deliverables must be {{\"advice-note.md\": \"advice-note.md\"}}")
    tags = t.get("tags", [])
    country = tj.parent.parent.name.split("-")[0]
    if len(tags) != 3 or tags[0].lower() != {"egypt": "egypt", "saudi": "saudi"}.get(country, "?"):
        err(f"{rel}: tags must be [country, area, source label] and the country must match the folder")
    md0 = t.get("metadata", {})
    aid = md0.get("astrolabe_id", "")
    if not re.fullmatch(r"AST-\d{3}", aid) or aid in seen_ids:
        err(f"{rel}: metadata.astrolabe_id must be a unique AST-NNN, found '{aid}'")
    seen_ids.add(aid)
    if not md0.get("source_ids"):
        err(f"{rel}: metadata.source_ids must list the sources the task was built from")
    if md0.get("status") not in ("approved", DRAFT):
        err(f"{rel}: metadata.status must be 'approved' or '{DRAFT}'")
    docs = tj.parent / "documents"
    if not (docs / "client-facts.txt").is_file():
        err(f"{rel}: documents/client-facts.txt is missing")
    ids = set()
    for c in t.get("criteria", []):
        cid = c.get("id", "?")
        if cid in ids:
            err(f"{rel}: duplicate criterion id {cid}")
        ids.add(cid)
        for k in ("id", "title", "match_criteria", "deliverables", "sources"):
            if k not in c:
                err(f"{rel} {cid}: missing '{k}'")
        m = c.get("match_criteria", "")
        if "PASS if" not in m or "FAIL if" not in m:
            err(f"{rel} {cid}: match_criteria must contain 'PASS if' and 'FAIL if'")
        if "client-facts.txt" not in c.get("sources", []):
            err(f"{rel} {cid}: sources must include client-facts.txt")
        for s in c.get("sources", []):
            if not (docs / s).is_file():
                err(f"{rel} {cid}: source '{s}' not found in documents/")
    if not 3 <= len(t.get("criteria", [])) <= 8:
        err(f"{rel}: expected 3 to 8 criteria, found {len(t.get('criteria', []))}")
    if md0.get("status") == DRAFT and "review" in md0:
        err(f"{rel}: has a review record but status is still a draft")
    md = t.get("metadata", {})
    if md.get("status") == "approved" and "review" not in md:
        err(f"{rel}: status is 'approved' but there is no metadata.review record")
    if "review" in md:
        for k in ("reviewer", "date", "outcome"):
            if k not in md["review"]:
                err(f"{rel}: metadata.review is missing '{k}'")


def check_questions() -> None:
    q = ROOT / "data/exact-text/questions.jsonl"
    ids = set()
    for n, line in enumerate(q.read_text(encoding="utf-8").splitlines(), 1):
        try:
            r = json.loads(line)
        except Exception:  # noqa: BLE001
            err(f"{q.name}:{n}: invalid JSON")
            continue
        for k in ("id", "jurisdiction", "type", "question", "reference"):
            if not r.get(k):
                err(f"{q.name}:{n}: missing '{k}'")
        if r.get("id") in ids:
            err(f"{q.name}:{n}: duplicate id {r.get('id')}")
        ids.add(r.get("id"))
    for f in (ROOT / "data/exact-text").glob("results.*.json"):
        res = {r["id"] for r in json.loads(f.read_text(encoding="utf-8"))}
        if res != ids:
            err(f"{f.name}: question ids differ from questions.jsonl ({len(res ^ ids)} differ)")


def check_runs(slugs: set[str]) -> None:
    for f in sorted((ROOT / "results/tasks").glob("*.json")):
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            err(f"{f.name}: invalid JSON")
        if f.name.split(".")[0] not in slugs:
            err(f"{f.name}: no task folder with this name")


def main() -> int:
    tasks = sorted((ROOT / "tasks").glob("*/*/task.json"))
    for tj in tasks:
        check_task(tj)
    check_questions()
    check_runs({t.parent.name for t in tasks})
    print(f"{len(tasks)} tasks checked, {len(errors)} problem(s)")
    for e in errors:
        print(" -", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
