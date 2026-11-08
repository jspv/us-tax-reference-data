# Federal settlement (tax years 2025 and 2026), 2026-11-08

Two independent readers (A and B, `docs/federal-brief.md`) filled `schema/federal.schema.json` from the archived
sources. Field by field: 2025, 488 lines agree and 46 differ; 2026, 481 agree and 45 differ. No printed figure
differed. The differences were in how derivations and indexing are written, and in what was left out:

- **Ordinary bracket edges: no derivation (both readers).** 26 U.S.C. 1(j)(3)(B)(iii): "subsection (f)(8) shall not
  apply", so each status's table is indexed from its own 2018 base table. Settled as both readers had it, with a
  note in `brackets.notes`: the first five single and separate edges still equal half the joint edges every year
  (base tables exactly half; rounding x down to 25 equals half of 2x rounded down to 50), so a consumer that derives
  them gets the same figures.
- **IRMAA derivations:** A recorded every derived limit (joint 2x, joint top 1.5x, lived-together separate = individual
  top minus the first limit, both as `over` and `up_to`); B had fewer. A taken.
- **SALT:** A derives the separate cap, threshold and floor as half; B lacked the floor. A taken. Rate "0.30" (A).
- **Premium rounding** (42 CFR 408.27, to 10 cents) and `indexed_from: 2026` for the age 60-63 catch-up: A only. A taken.
- **RMD start age:** A gives 1951-1959 -> 73 and 1960 on -> 75 and leaves out earlier births (the old 70 1/2 boundary
  falls mid-1949; anyone born before 1951 began by 2023). B's "through 1950 -> 72" is wrong for births before July 1,
  1949. A taken.
- **Added in settlement (2026):** married-filing-separately NIIT and additional Medicare thresholds (125,000) and SALT
  cap and threshold (20,200, 252,500), each as a half-of-joint (or half-of-single) derivation. The statute sets them
  as half and no 2026 source prints them, so `tools/validate.py` now skips the "printed" check for derived figures
  and proves them by re-doing the rule.
- **Left out (neither source prints them):** HSA limits; employer payroll rates (26 U.S.C. 3111 not archived). The
  earnings-test indexing (`wage_index`) is marked not confirmed: 42 U.S.C. 403(f)(8) is not archived.
- **Qualifying surviving spouse:** the senior deduction threshold (75,000), additional Medicare threshold (200,000)
  and Social Security base amounts (25,000/34,000) differ from joint because the statute gives the joint amount to
  a joint return only.

Reader notes: `work/extract/federal/A/NOTES.md`, `work/extract/federal/B/NOTES.md`.
