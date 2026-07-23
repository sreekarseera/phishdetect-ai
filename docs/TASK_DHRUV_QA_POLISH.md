# Dhruv's task: QA pass + extension polish

> **Note:** the original version of this task (build storage.js/util.js/style.css) is already done — Sreekar built it solo while you were unavailable, then fixed a couple of bugs found during manual testing (mangled emoji from a missing charset, and duplicate history rows). This doc now covers the next phase: thorough QA and polish before the demo.

## Goal
The core extension works end-to-end (classify → history → blocklist → export → banner), but it's only been tested by one person for a short time. Your job is to actually try to break it, and make it look better while you're at it.

## Files you own (only edit these)
- `extension/style.css`
- `extension/README.md`
- Anything you find broken in `extension/popup.js`, `extension/storage.js`, `extension/util.js`, `extension/banner.js` — but **message Sreekar before changing these**, don't just push fixes silently, since he's the one who has to keep the pieces consistent.

**Do not touch** `backend/` at all — that's Smaran's and Sreekar's territory.

## Setup
1. Get the latest code: `git pull`
2. Start the backend (in one terminal): `cd backend && source venv/bin/activate && uvicorn app:app --reload`
3. Load the extension: `chrome://extensions` → enable Developer Mode → **Load unpacked** → select the `extension/` folder

## Step 1 — QA pass (do this first, before styling)
Go through this checklist and note anything that looks wrong, confusing, or broken:
- [ ] Analyze a clearly scammy message → shows "🚩 Potential scam" with a confidence %
- [ ] Analyze a clearly normal message → shows "✅ Looks safe"
- [ ] Analyze the exact same message + sender email twice in a row → only **one** row appears in History (not two)
- [ ] Analyze the exact same message with a **different** sender email → a **new** row appears in History
- [ ] Hover over a History row → a tooltip shows the sender email (or "No sender email provided" if left blank)
- [ ] Add a sender email on a scam message → it appears under "Blocked Emails"
- [ ] Click the ✕ next to a blocked email → it's removed from the list
- [ ] Click **Export History** → a CSV downloads, opens cleanly in Numbers/Excel with columns for text/email/label/score/explanation/timestamp
- [ ] Click **Export Blocklist** → a CSV downloads with the blocked emails
- [ ] Stop the backend (Ctrl+C in its terminal), click Analyze → shows a clear error message instead of hanging or failing silently
- [ ] **Banner test** (already confirmed working via automated headless tests — this is just a human sanity check): add an email to the blocklist, then type that email into any **normal** webpage (e.g. a Gmail compose window) → a purple warning banner should appear within ~1 second, live, no reload. **Do not use Google Docs for this** — Docs renders text to canvas, so live typing there is invisible to all extensions (known limitation, documented in the root README, not a bug to report).
- [ ] Try an empty message (click Analyze with nothing typed) → should show a friendly message, not an error or a backend call
- [ ] Analyze several messages in a row → the popup's overall size should stay stable (it used to visibly jump/grow on every click — fixed, but worth re-confirming)

For anything that fails, write down: what you did, what you expected, what actually happened. Send that list to Sreekar rather than trying to fix backend/JS logic yourself.

## Step 2 — Polish `style.css`
Once you've done the QA pass, look at the popup with fresh eyes:
- Does the off-white/purple/gold palette feel consistent and clean, or does anything look off?
- Is the "Analyze" button's disabled/loading state ("Analyzing…") visually obvious?
- Do the History and Blocklist sections look good with 10+ entries in them (scroll behavior, spacing)?
- Anything you'd improve — spacing, font sizes, colors, hover states on buttons — go ahead and tweak `style.css` directly, it's low-risk since it only affects appearance.

## Step 3 — Update `extension/README.md`
It currently still describes the old RoBERTa-based backend. Update the "Setup" section to match what's actually true now (scikit-learn, `pip install -r requirements.txt`, `python3 train_model.py` before first run, etc. — check `backend/requirements.txt` and `backend/train_model.py` for the actual current steps).

## Done checklist
- [ ] Full QA checklist above run through, results (pass/fail list) sent to Sreekar
- [ ] Banner tested and confirmed working (or reported as broken)
- [ ] `style.css` polish pass done
- [ ] `extension/README.md` updated to match the current architecture

## If you get stuck
Ping Sreekar. Don't spend more than ~20 minutes stuck on one thing — flag it instead.
