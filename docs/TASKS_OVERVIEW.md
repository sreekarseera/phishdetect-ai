# Task split — Phase 2 (hardening + polish), 4-person team

Full context/architecture: see `../CLAUDE.md` (rules, locked contracts).

## Status
Phase 1 (get a working demo end-to-end) is **done**. Sreekar built the full stack solo while teammates were unavailable:
- Backend: scikit-learn model (211-row dataset, 100% val accuracy, verified against novel out-of-template examples), FastAPI serving it
- Extension: `storage.js`, `util.js`, `popup.js`, `banner.js`, `style.css` all implemented, plus a fix for the popup visibly resizing on every Analyze click
- Manually tested end-to-end in Chrome; found and fixed several real bugs (mangled emoji from missing charset, duplicate history rows, missing sender-email tracking, popup resize jumpiness)

Repo: https://github.com/sreekarseera/phishdetect-ai — everything above is pushed to `main`.

## What's left
Hardening and polish before the demo, split into three parallel tracks:

| Track | Owner | Focus | Doc |
|---|---|---|---|
| A — Model hardening | Smaran | Stress-test the model against real (non-templated) examples, expand `dataset.csv` to cover gaps, retrain | `TASK_SMARAN_DATA_MODEL.md` |
| B — QA + polish | Dhruv | Full manual QA pass (including the still-unconfirmed banner feature), `style.css` polish, extension README update | `TASK_DHRUV_QA_POLISH.md` |
| C — Demo readiness | Shourya | Cold-start setup test, root `README.md`, a literal demo script, pre-tested example messages for the live run | `TASK_SHOURYA_DEMO_PREP.md` |

Sreekar: available to unblock any track, fix anything flagged as broken (see the note in each doc — teammates should report issues rather than editing `popup.js`/`storage.js`/`app.py`/`banner.js` themselves), and decide if/when to fold in any stretch goals (e.g. full-page scam-text scanning in `banner.js`, beyond just blocked-email matching).

## Why this split
- A and B don't touch the same files (backend vs. extension), so they're safe to run at the same time.
- C is almost entirely docs/process work — lowest risk of breaking anything, and genuinely useful (a cold-start test from someone who hasn't touched the code will catch setup problems the rest of us are now blind to).

## Ground rules for handoff
- `git pull` before starting, `git push` when you have something working — small, frequent commits.
- If you find a bug outside your own files, report it to Sreekar rather than fixing it yourself — see `CLAUDE.md` for why (stay-in-your-lane rule exists to avoid merge conflicts and contract drift).
- If something in `CLAUDE.md`'s locked contracts seems wrong, ask before changing it.
