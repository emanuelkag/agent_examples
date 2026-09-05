# Time-loop convention: estimate before, measure after

Every issue that we start working on gets a **frozen estimate** at start and a
**measured actual** at close, both as timestamped issue comments. The pairs are
the calibration dataset for agent time/resource estimation (estimate → measure →
calibrate → feed back).

## The three estimate lines (posted when work starts, never edited)

```
est_active_min: 60        # machine work W, expected (range 30-120)
est_tokens: 200000        # output tokens across all sessions/agents
est_calendar: unknown     # wall-clock to done_when; "unknown" is legitimate
```

Plus a JSON block (schema below). Post with:

```
python scripts/issue_time_loop.py estimate --repo owner/repo --issue N \
    --active-min 60 --active-range 30-120 --tokens 200000 --confidence 0.35
```

## The three actual lines (posted at close)

```
act_active_min: 74        # from transcript extraction or commit spans
act_tokens: 231000        # measured, from session usage fields
act_calendar_min: 310     # first work marker -> done_when verified
```

```
python scripts/issue_time_loop.py close --repo owner/repo --issue N \
    --active-min 74 --tokens 231000 --calendar-min 310 --evidence "commit spans abc123..def456"
```

## Rules (each one exists because a measurement failed without it)

1. **Declare the unit.** Work W (token-proportional machine effort), machine
   duration D (critical path), and calendar time are different quantities,
   measured factor 10+ apart. An estimate without a declared unit is not
   scoreable.
2. **Freeze estimates.** Never edit an estimate comment; corrections are a new
   comment. The comment `createdAt` is the tamper-proof timestamp.
3. **Estimate in tokens first**, convert to minutes with measured rates (see
   `docs/machine_time_reference.md`). Tokens are the native effort unit; the
   session-level conversion holds at Spearman 0.96.
4. **Source taxonomy** (from `orchestrator/app/routing/contracts.py::Estimate`):
   `planning_heuristic` until calibration data exists; `calibrated` only after
   ≥20 measured pairs in the same class. `unknown` is a legitimate value —
   never guess to fill a field.
5. **Censoring.** Open issues with an estimate and no actual are *censored*
   observations. They count neither as hit nor miss; `report` lists them
   separately. Ignoring them biases the dataset toward short tasks.
6. **Provenance separation.** Machine-generated actuals (transcript extraction)
   and human-confirmed actuals are tracked in separate fields — a system that
   counts its own outputs as confirmation calibrates itself endogenously.
7. **Actual = done_when verified**, not the close click. If the issue has no
   third-party-checkable done_when, say so in the evidence field.
8. **No retroactive estimates.** Work that already started before an estimate
   exists gets actuals only; the pair is marked `estimate: missing`.
9. **Mandatory covariates** in the actual: model(s) used, notable throttling or
   contention, parallel branches. Without them the dataset measures
   infrastructure noise, not estimation skill.

## Evaluation

`python scripts/issue_time_loop.py report --repo owner/repo` pairs estimates
with actuals and prints per-quantity `log(actual/estimate)` bias and spread,
plus the censored count. A constant-median baseline is reported alongside —
an estimator that does not beat it has no signal (permutation-null rule).

Reference values and the measurement behind this convention:
`docs/machine_time_reference.md`.
