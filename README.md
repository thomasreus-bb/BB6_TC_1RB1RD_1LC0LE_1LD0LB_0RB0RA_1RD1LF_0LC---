# A translated cycler with period 4.1·10²⁴ in BB(6): `1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---`

| | |
|---|---|
| machine | `1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---` (BB(6) holdout, Holdout Guide #38, "Rules known, no proof", simulated 2.9·10²⁸) |
| result | from step 26,735,911,821,080,026,413,068,533,212 on, the machine is a **translated cycler** with a left record |
| period | **4,126,262,385,607,271,490,126,714 steps** (≈ 4.1·10²⁴) |
| shift | the tape grows by **2,428,193,875,694 cells** to the left per period |
| cells read in a period | at most **3,336 cells** right of the left edge at the start of the period |
| consequence | the machine never halts |
| status | found with an accelerated simulator; **not yet independently confirmed** (see [What is not proved](#what-is-not-proved)) |

Found by Thomas Reus with Claude (Anthropic), 8 Nov 2026, while studying the BB(6) holdouts in [bb6-vampire-family](https://github.com/thomasreus-bb/bb6-vampire-family-1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---) (candidate no. 48 there).

## Size compared with Skelet #1

[Skelet #1](https://wiki.bbchallenge.org/wiki/Skelet_1), the best-known large translated cycler among the 5-state machines, starts its cycle after about 5.42·10⁵¹ steps and has a period of 8,468,569,863 steps. The cycler here starts much earlier (2.67·10²⁸ steps) but its **period is about 5·10¹⁴ times longer** (4.1·10²⁴ steps), and in one period the head moves more than 2.4·10¹² cells.

## How the machine works

Transition table:

| | 0 | 1 |
|---|---|---|
| A | 1RB | 1RD |
| B | 1LC | 0LE |
| C | 1LD | 0LB |
| D | 0RB | 0RA |
| E | 1RD | 1LF |
| F | 0LC | HALT |

HALT needs state F on a 1. F is only entered from E reading a 1 (via C reading 1 → B reading 1 → E reading 1, moving left), so a HALT needs a block `1111` met from the right by a leftward sweep in state C.

### Phases

The run is a "Bell": a block grows to the left while a counter on its right is used up, then the counter is rebuilt from the grown block. At the left record in state C that starts a phase, the tape is

    (01)^3 (1001)^B T   or   0100 (1001)^B T

where `T` is a short near tail (at most a few dozen cells). Right of that lies a stack of long gaps of zeros, separated by the marker `1 (100)^3 0110011001`. The gaps are created during phases and used up slowly by later phases.

### Exact one-phase laws

For the main phase types the next counter B′ is given exactly by residues of B. `step48.c` runs one phase on a built tape. `types48.py` checked every B in [150, 850) or [200, 650) (no gap behind):

| type | law |
|---|---|
| `0100`, T empty | B′ = (5B+d)/3, d = 9, 4, 14, 12, 49, 14, 24, 16, 23 for B mod 9 = 0…8 |
| `0100`, T = `011011` | B′ = (5B+d)/3, d = 27, 1, 77, 42, 49, 29, 3, 19, −1 for B mod 9 = 0…8 |
| `(01)^3`, T empty, B ≡ 2 (mod 5) | B′ = (7B+71)/5; a new gap of about (B−147)/5 cells is created |
| `(01)^3`, T empty, B ≡ 3 (mod 5) | B′ = B+13 |
| `(01)^3`, T empty, B ≡ 4 (mod 5) | B′ = (5B+d)/3, d = 54, 58, 77, 51, 76, 98, 81, 118, 71 for B mod 9 = 0…8 |
| `(01)^3`, T empty, B ≡ 0, 1 (mod 5) | longer phases, no single law |
| `(01)^3`, T = `0111001110011001` (after every +13 phase) | B ≡ 1: (7B+23)/5; B ≡ 4: B+26; B ≡ 0: (5B+d)/3; **B ≡ 3: HALT** |

These are the 5/3, 7/5 and +13 branches mentioned in the Holdout Guide, now with all constants.

Built tapes do halt, for example:
- tail `0111001110011001` with B ≡ 3 (mod 5);
- `(01)^3`, empty tail, B ≡ 40 (mod 70) when the first gap is at least about 1.07·B.

The laws avoid these cases. After a +13 phase B ≡ 1 (mod 5), never 3, and `0100` phases lead to `(01)^3`-empty phases with B ≢ 0 (mod 5).

### The restart

`data/phases_bs40.txt` lists all phase starts of the real run. In 80 phases up to step 2.6736·10²⁸ there is no HALT.

At step 26,735,911,820,734,401,541,954,296,395 the first `(01)^3`-empty phase with B ≡ 0 (mod 5) since the start appears (B = 47,451,826,833,435, first gap 6,778,832,404,745 cells). It does not halt. Instead a small computation starts again at the left end with **B = 807**. It runs through 73 phases up to B = 586,507,771,955, again a `(01)^3`-empty phase with B ≡ 0 (mod 5) and a short gap (75,678,422,150 cells), which starts it again at B = 807.

Each of these runs is identical phase by phase (type, B, near tail, gaps, step counts) and leaves a copy of its structure on the tape.

## The translated cycler

Let t₀ < t₁ < t₂ be the restart records, i.e. the left records in state C that start the phase with B = 807:

| restart | step | cells from the head to the right end |
|---|---|---|
| 0 | 26,735,911,821,080,026,413,068,533,212 | 197,113,627,881,536 |
| 1 | 26,740,038,083,465,633,684,558,659,926 | 199,541,821,757,230 |
| 2 | 26,744,164,345,851,240,956,048,786,640 | 201,970,015,632,924 |

`phase48m.py` stores the exact tape at each restart and the smallest number of cells right of the head during each period (`data/tc_restarts.pkl`, readable form in `data/restart_configs.txt`). `tccheck.py` then checks the Lin recurrence condition for a translated cycler with a left record (`data/tc_check.txt`):

- Both records are left records in state C.
- Between t₀ and t₁ the head never goes more than W = 3,336 cells to the right of the left edge it had at t₀ (3,310 cells between t₁ and t₂).
- The first W + 100 cells from the left edge are identical at t₀ and t₁, and at t₁ and t₂. The comparison is cell by cell, and long runs of equal blocks are compared block-wise.

So from t₀ on the machine does the same thing in every period, shifted 2,428,193,875,694 cells to the left. It never reads the rest of the tape again and never halts. Between t₀ and t₁ the cells right of the first 3,336 still held the original structure, and between t₁ and t₂ a copy; the period is the same in both cases.

## The accelerated simulator

`msim48.py` stores the tape as runs of 40-cell blocks and uses two kinds of acceleration:
- a whole run of equal blocks is crossed in one step when the head passes through it unchanged (chain step);
- loops whose tape shape recurs with linearly changing run lengths are skipped. It needs 3 equal changes in a row, a period of up to 4 macro steps, and exact sums of the step counts. A safety margin keeps every shrinking run long enough.

A restart cycle is skipped the same way, but this is not used for the result: the three restarts above were all simulated, not skipped. At the left end of the tape the leftmost block is simulated cell by cell, so that every left record can be inspected.

Checks against direct simulation (`chk48.py`, `at48.c`): at 260 random event times up to 5·10¹⁰ steps the tape, state and step count agree exactly. The phase starts agree with an independent direct run (`ph48.c`) up to 5·10¹⁰ steps, and with a run using 120-cell blocks up to 5.9·10¹³ steps.

## What is not proved

- The loop skipping in `msim48.py` is a heuristic: a skipped loop is assumed to repeat exactly, and that assumption is not checked when it is applied. It is checked against direct simulation only up to 5·10¹⁰ steps, but the result depends on about 2.67·10²⁸ simulated steps.
- The excursion bound W is sampled whenever the head turns from right to left in a macro step, with one block (40 cells) of safety. Inside skipped loops the deepest point is taken from the iterations simulated after the skip. A margin of 100 cells is added in the comparison.

Two ways to make it a proof:
1. **Independent simulation.** Reach the configuration of restart 0 with another simulator (exact step count and tape as in `data/restart_configs.txt`), then simulate one period and check the Lin condition.
2. **Certificate.** Verify one period from the stored restart 0 configuration in a proof assistant, plus the fact that this configuration is reached.

## Files

| file | content |
|---|---|
| `sim/msim48.py` | accelerated simulator (block runs, chain steps, loop skipping, cell-by-cell left edge) |
| `sim/phase48m.py` | real run, lists every phase start; with `TCDUMP=file` it stores the restart tapes and excursions |
| `sim/tccheck.py` | exact Lin recurrence check from the stored restart tapes |
| `sim/chk48.py`, `sim/at48.c` | comparison of the accelerated simulator with direct simulation |
| `sim/ph48.c` | direct simulation that prints the phase starts (up to about 10¹² steps) |
| `sim/step48.c`, `sim/pmap48.py` | one phase of a built tape; parse and build phase-start tapes |
| `sim/types48.py`, `sim/laws48.py` | one-phase laws per phase type, and the table of laws |
| `sim/hit48.py` | halting rate of built restart phases with a short gap |
| `sim/canon48.py`, `sim/cmpanch.py` | earlier comparison of restart tapes in canonical form |
| `data/phases_bs40.txt` | all phase starts of the real run up to the fourth restart (`PH step prefix B tail gap`) |
| `data/tc_restarts.pkl`, `data/restart_configs.txt` | exact tapes at the three restarts |
| `data/tc_restarts.txt`, `data/tc_check.txt` | output of the restart run and of `tccheck.py` |

## Reproduce

    bash reproduce.sh check    # re-check the stored restart tapes (seconds)
    bash reproduce.sh direct   # accelerated vs. direct simulation up to 5·10¹⁰ steps (a few minutes)
    bash reproduce.sh full     # simulate up to the third restart and check the cycle (30–60 minutes)

Needs Python 3 and gcc.
