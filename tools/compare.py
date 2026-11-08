"""Compare two independent layer-1 readings of the same state, field by field.

    uv run python -m tools.compare A.json B.json

Structured fields (amounts, rates, ages, dates, true/false, choices from a list) must match exactly.
Free text, citations and the ids each reader invents are listed but do not count. List items are
matched by what they mean, not by position or wording:
  reliefs        by form, covered income, whose age, and the age and birth-date bounds
  deductions     by what and per;  surtaxes by rate;  capital gains by what they apply to
  income tests   by position (one per item);  indexing entries by their answer
Exit 1 when any structured field differs: each is then settled against the booklet by a third read
and the settlement is logged.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

FREE_TEXT = {"notes", "label", "condition", "as_printed", "cap_rule", "not_covered", "other_conditions",
             "note", "section", "publication", "accessed", "url", "id", "best_of_group", "cannot_combine_with",
             "index", "figure"}


def item_label(item: dict, index: int):
    if "covers" in item and "who" in item:  # a relief branch
        who = item["who"]
        form = item.get("form", "?")
        if form == "subtraction" and not item.get("cap") and not item.get("income_test") and not item.get("sub_limits"):
            form = "exempt_in_full"  # an uncapped, untested subtraction removes all of the income
        bounds = [who.get(k) for k in ("min_age", "max_age", "born_on_or_after", "born_on_or_before")]
        return ("relief(" + form + ";" + ",".join(sorted(item["covers"])) + ";"
                + who.get("basis", "?") + ";" + "/".join("-" if b is None else str(b) for b in bounds) + ")")
    if "what" in item and "per" in item:
        return f"deduction({item['what']}/{item['per']})"
    if "applies_to" in item and "treatment" in item:
        return f"gains({item['applies_to']})"
    if "figure" in item and "indexed" in item:
        return f"indexing({item['indexed']})"
    if "rate" in item and "over" in item:
        return f"surtax({item['rate']})"
    if "income" in item and "amount" in item:
        return f"sub_limit({item['income']})"
    return index


def normalise(value):
    """Write a relief the same way however a reader chose to: an uncapped, untested subtraction is exempt in full."""
    if isinstance(value, dict):
        out = {k: normalise(v) for k, v in value.items()}
        if out.get("form") == "subtraction" and "covers" in out and not out.get("cap") and not out.get("income_test") and not out.get("sub_limits"):
            out["form"] = "exempt_in_full"
        return out
    if isinstance(value, list):
        return [normalise(v) for v in value]
    return value


def flatten(value, path=""):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from flatten(item, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            yield path, sorted(value, key=str)  # a list of plain values compares as a set
            return
        seen: dict[str, int] = {}
        for index, item in enumerate(value):
            label = item_label(item, index) if isinstance(item, dict) else index
            if isinstance(label, str):
                seen[label] = seen.get(label, 0) + 1
                if seen[label] > 1:
                    label = f"{label}#{seen[label]}"
            yield from flatten(item, f"{path}[{label}]")
    else:
        yield path, value


def is_free_text(path: str) -> bool:
    return path.split(".")[-1].split("[")[0] in FREE_TEXT


def compare(a: dict, b: dict) -> tuple[list[str], list[str]]:
    left, right = dict(flatten(normalise(a))), dict(flatten(normalise(b)))
    structured, text = [], []
    for path in sorted(set(left) | set(right)):
        x, y = left.get(path), right.get(path)  # a field left out, null and an empty list mean the same
        if x == y or (x in (None, []) and y in (None, [])):
            continue
        x = "<missing>" if path not in left else x
        y = "<missing>" if path not in right else y
        (text if is_free_text(path) else structured).append(f"{path}: A={x!r}  B={y!r}")
    return structured, text


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    structured, text = compare(json.loads(Path(argv[0]).read_text()), json.loads(Path(argv[1]).read_text()))
    print(f"{len(structured)} structured differences, {len(text)} wording differences")
    for line in structured:
        print("  DIFF", line)
    for line in text:
        print("  text", line[:200])
    return 1 if structured else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
