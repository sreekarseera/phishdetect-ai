# PhishDetect AI Chrome Extension 🚫📩

The Chrome (Manifest V3) side of PhishDetect AI. Talks to the local FastAPI
backend for classification; keeps all history/blocklist state in
`chrome.storage.local` (nothing is stored server-side).

## Features

- 🧠 ML-powered scam detection (scikit-learn TF-IDF + Logistic Regression, served by the backend)
- 🧾 History log of analyzed messages, deduped by (message, sender) pair, sender shown on hover
- 🚫 Blocklist of scam sender emails — auto-added when a scam has a sender, removable from the popup
- 📢 Live warning banner on any webpage mentioning a blocked email — reacts to typing and blocklist changes without a page reload (works in iframes too)
- 💾 Export history and blocklist to CSV
- 🎨 Clean minimalist UI (off-white, purple, gold palette)

## Files

| File | Purpose |
|---|---|
| `manifest.json` | MV3 config; injects `banner.js` into all frames of all pages |
| `popup.html` / `popup.js` | Analyze UI, history, blocklist, CSV export |
| `banner.js` | Content script — scans pages for blocked emails, shows the warning banner |
| `storage.js` | `chrome.storage.local` wrapper: `getHistory`, `addHistoryEntry`, `getBlocklist`, `addBlocked`, `removeBlocked` |
| `util.js` | `exportToCsv(rows, filename)`, `extractEmails(text)` |
| `style.css` | Popup styling |

## Setup

1. Start the backend first (from the repo root — full steps in the root `README.md`):
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app:app --reload
   ```
2. Open `chrome://extensions`, enable **Developer mode**, click **Load unpacked**, and select this `extension/` folder.
3. Click the extension icon, paste a message, Analyze.

The backend URL is hardcoded to `http://localhost:8000` by design (local demo
only — see `CLAUDE.md` in the repo root).

## Known limitations

See the root `README.md` — short version: canvas-rendered apps (Google Docs
etc.) don't expose live-typed text to any extension, and content scripts can't
run on `chrome://` pages or `data:` URLs.
