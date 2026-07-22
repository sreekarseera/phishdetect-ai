# Your track: Backend + Popup integration (the critical path)

You own the pieces everything else plugs into. Don't wait on your teammates to start — stub their pieces first, swap in the real thing when they hand off.

## Files you own
- `backend/app.py`
- `backend/requirements.txt`
- `extension/popup.js`
- `extension/banner.js` (stretch — do this last)

## Order of operations

**1. `backend/requirements.txt`** — rewrite to: `fastapi`, `uvicorn`, `scikit-learn`, `pandas`, `joblib` (drop `transformers`/`torch`).

**2. `backend/app.py`** — while Teammate A is still training, you can write this against a fake model so you're not blocked:
```python
import joblib
model = joblib.load("model/model.joblib")  # swap in once Teammate A hands it off
```
Rewrite the file to: load the joblib model, expose only `POST /classify/` (drop the `/blocklist/*` routes and the in-memory `blocklist` set — that state now lives client-side, see `CLAUDE.md`). Keep the response shape `{"label": "LABEL_0"|"LABEL_1", "score": float, "explanation": str}` — `popup.js` depends on it. Keep the existing CORS middleware.

Test with `curl` before touching the extension at all:
```bash
curl -X POST localhost:8000/classify/ -H 'Content-Type: application/json' -d '{"text":"You won a free prize, click now!"}'
```

**3. `extension/popup.js`** — while Teammate B is still writing `storage.js`/`util.js`, stub them locally so you're not blocked, e.g. temporary local functions with the same names/signatures (see `CLAUDE.md` for the exact contracts), then swap your stub import for the real file once Teammate B hands off:
- On `#analyze` click: read `#input`, POST to `http://localhost:8000/classify/`, render into `#result`, call `addHistoryEntry(...)`.
- If `#email` is filled and the result is a scam, call `addBlocked(...)`.
- On popup load, render `#history` and `#blocklist` from `getHistory()`/`getBlocklist()`.
- Wire `#exportHistory`/`#exportBlocklist` to `exportToCsv(...)`.
- **Handle the backend-down case** — if `fetch` fails/throws, show a visible error in `#result` instead of failing silently. This will happen at least once during setup or the live demo.

**4. `extension/banner.js`** (only after 1-3 work end-to-end) — content script: on page load, call `extractEmails(document.body.innerText)`, check each against `getBlocklist()`, and if any match, inject a small warning banner `<div>` at the top of the page.

## Test it end-to-end
1. `cd backend && source venv/bin/activate && uvicorn app:app --reload`
2. `chrome://extensions` → enable Developer Mode → "Load unpacked" → select `extension/`
3. Open the popup, paste a scam-sounding message, click Analyze → check the result, then check it shows up under History.
4. Add an email in the blocklist, export both CSVs, confirm the files download correctly.
5. Visit any page containing that blocked email in its text, confirm the banner appears.
6. Stop `uvicorn`, click Analyze again, confirm you get a visible error instead of a silent failure or hang.

## If a teammate is late handing off
Don't sit idle — work on `banner.js`, more manual testing, or `docs`/README updates while you wait. Your stubs mean you're never fully blocked.
