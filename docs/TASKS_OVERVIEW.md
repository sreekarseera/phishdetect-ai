# Task split — Phase 2 (hardening + polish)

Full context/architecture: see `../CLAUDE.md` (rules, locked contracts).

## Status
Phase 1 (get a working demo end-to-end) is **done**. Sreekar built the full stack solo while teammates were unavailable:
- Backend: scikit-learn model (211-row dataset, 100% val accuracy, verified against novel out-of-template examples), FastAPI serving it
- Extension: `storage.js`, `util.js`, `popup.js`, `banner.js`, `style.css` all implemented
- Manually tested end-to-end in Chrome; found and fixed 3 real bugs (mangled emoji from missing charset, duplicate history rows on repeat clicks, missing sender-email tracking in history)

Repo: https://github.com/sreekarseera/phishdetect-ai — everything above is pushed to `main`.

## What's left
This is no longer "build from scratch" work — it's hardening and polish before the actual demo. Two parallel tracks:

| Track | Owner | Focus | Doc |
|---|---|---|---|
| A — Model hardening | Teammate 1 | Stress-test the model against real (non-templated) examples, expand `dataset.csv` to cover gaps, retrain | `TASK_TEAMMATE_A_DATA_MODEL.md` |
| B — QA + polish | Teammate 2 | Full manual QA pass (including the still-unconfirmed banner feature), `style.css` polish, README update | `TASK_TEAMMATE_B_STORAGE_UTILS_STYLE.md` |

Sreekar: available to unblock either track, fix anything flagged as broken (see the note in each doc — teammates should report issues rather than editing `popup.js`/`storage.js`/`app.py` themselves), and decide if/when to fold in any stretch goals (e.g. full-page scam-text scanning in `banner.js`, beyond just blocked-email matching).

## Ground rules for handoff
- `git pull` before starting, `git push` when you have something working — small, frequent commits.
- If you find a bug outside your own files, report it to Sreekar rather than fixing it yourself — see `CLAUDE.md` for why (stay-in-your-lane rule exists to avoid merge conflicts and contract drift).
- If something in `CLAUDE.md`'s locked contracts seems wrong, ask before changing it.
