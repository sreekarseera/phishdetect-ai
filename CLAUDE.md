# Rules for anyone (or any AI) working on this repo

This is a 24-48 hour hackathon project. The single goal is a **working demo**, not clean code. Every rule below exists to protect speed. If a rule and "best practice" conflict, follow the rule.

## Locked architecture decisions — do not silently change these

1. **Model = scikit-learn only.** TF-IDF + Logistic Regression, via `backend/train_model.py`. Do **not** reintroduce `transformers`/`torch`/RoBERTa — it was deliberately dropped because it's too slow to set up and iterate on under a hackathon deadline. If you think the model needs to change, say so before doing it, don't just do it.
2. **Backend is stateless.** `app.py` only exposes `POST /classify/`. No database, no in-memory blocklist on the server. All history and blocklist data lives in the Chrome extension's `chrome.storage.local`, via `extension/storage.js`. Don't add server-side persistence.
3. **Fixed API contract** — every consumer depends on this shape, so it must not change without updating every consumer at once:
   - Request: `POST http://localhost:8000/classify/` with JSON body `{"text": "..."}`
   - Response: `{"label": "LABEL_0" | "LABEL_1", "score": <float 0-1>, "explanation": "<string>"}` (`LABEL_1` = scam)
4. **Fixed `storage.js` contract** (used by `popup.js` and `banner.js`):
   - `getHistory()`, `addHistoryEntry(entry)`, `getBlocklist()`, `addBlocked(email)`, `removeBlocked(email)` — all async, all backed by `chrome.storage.local`.
5. **Fixed `util.js` contract**: `exportToCsv(rows, filename)`, `extractEmails(text)`.

## Speed rules

- **No new test infrastructure, no CI setup.** The one exception that exists: `tests/run_all.py` (17 end-to-end checks, ~30s, see `tests/README.md`) — run it before every push. Don't expand it into a "real" test suite or add frameworks; anything it doesn't cover is manual click-through only.
- **No new dependencies** (pip or otherwise) without flagging it to Sreekar first — every new install is a chance to burn 30+ minutes on an environment bug.
- **Stay in your assigned files.** Three people are working in parallel (see `docs/TASKS_OVERVIEW.md`). Touching someone else's file without telling them causes merge conflicts and rework.
- **Commit small, commit often** (every working increment), so teammates can pull working code instead of a half-finished file.
- **If stuck on one bug for more than ~20 minutes, simplify the feature instead of continuing to debug it.** A smaller working feature beats a bigger broken one at demo time.
- **Prefer the obvious/boring solution over a clever one.** Copy-paste-obvious code is fine here.
- **Hardcode `http://localhost:8000`** as the backend URL. No env config, no deployment — this is a local demo.
- **Don't add error handling for cases that can't happen in a local demo.** Do handle the "backend isn't running" case in `popup.js` — that one WILL happen during setup/demo.

## For AI assistants specifically

Read this file before touching any code in this repo. If asked to "improve" or "clean up" something, don't reintroduce anything banned above (transformers/torch, server-side storage, new dependencies) unless explicitly asked. Prefer finishing the feature in the current task doc over refactoring adjacent code.
