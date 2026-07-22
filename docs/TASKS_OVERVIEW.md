# Task split — 3 people, parallel tracks

Full context/architecture: see `../CLAUDE.md` (rules, locked contracts) and the original plan at `~/.claude/plans/hazy-growing-moon.md` on Sreekar's machine.

## Why split this way
The two teammate tracks (Data/Model, and Storage/Utils/Style) don't depend on each other and don't depend on the final backend or popup — they only need to follow the **fixed contracts** in `CLAUDE.md`. That means all three tracks can start at the same time. Sreekar's track (backend + popup) is the integration point and the hardest part, so he owns it.

## Tracks

| Track | Owner | Files owned | Depends on |
|---|---|---|---|
| A — Data & Model | Teammate 1 | `backend/dataset.csv`, `backend/train_model.py`, `backend/model/model.joblib` (generated) | Nothing — start immediately |
| B — Storage & UI utils | Teammate 2 | `extension/storage.js`, `extension/util.js`, `extension/style.css` | Nothing — start immediately (just follow the contracts in `CLAUDE.md`) |
| C — Backend & Popup | Sreekar | `backend/app.py`, `backend/requirements.txt`, `extension/popup.js`, `extension/banner.js` | `app.py` needs Track A's `model.joblib` to fully test (can stub it and swap in later); `popup.js`/`banner.js` need Track B's functions to fully test (can stub them and swap in later) |

Full task briefs: `TASK_TEAMMATE_A_DATA_MODEL.md`, `TASK_TEAMMATE_B_STORAGE_UTILS_STYLE.md`, `TASK_SREEKAR_BACKEND_POPUP.md`.

## Timeline (wall-clock, working in parallel)

- **Hour 0-2:** All three start simultaneously. A builds dataset + trains a first model. B writes storage.js/util.js/style.css against the fixed contracts. Sreekar starts app.py against a placeholder model, and popup.js against stub versions of storage.js/util.js functions (so he isn't blocked waiting).
- **Hour 2-3:** A hands off `model.joblib` to Sreekar. B hands off real `storage.js`/`util.js` to Sreekar. Sreekar swaps stubs for the real files.
- **Hour 3-5:** Sreekar finishes popup.js integration and banner.js. A and B are now free — pull them onto testing, more dataset rows, or extra styling.
- **Hour 5-6:** Everyone tests the full extension end-to-end together (see "Test it end-to-end" in each task doc).

This gets a demoable product in **~5-6 hours of parallel work**, well inside the 24-48 hour window, even accounting for teammates needing more time on their pieces.

## Ground rules for handoff
- When your track's files are ready, tell Sreekar directly (don't just push and assume he'll notice) and say exactly what changed.
- If you finish early, don't start touching someone else's files — ping Sreekar for the next task instead.
- If something in `CLAUDE.md`'s contracts doesn't make sense or seems wrong, ask Sreekar before changing it — the other tracks are relying on it staying fixed.
