# Shourya's task: Demo readiness

## Goal
The extension works, but nobody has tested it as "a stranger setting it up for the first time" or thought through what actually gets said/shown live in front of judges. That's your job — make sure the *demo* doesn't fail even if the code is fine.

> **Update:** the root `README.md` is already written and pushed — **skip Step 2**. Your job is now Steps 1, 3, and 4. If your cold-start test (Step 1) finds the README instructions wrong or confusing, fix the README wording directly — that's still yours.

## Files you own
- `README.md` (repo root — already written; you maintain/fix it based on your cold-start test)
- `docs/DEMO_SCRIPT.md` (new file, you're creating it)

You're not expected to write extension/backend code for this task. If you spot a bug, report it to Sreekar rather than fixing it yourself (see `CLAUDE.md`).

## Step 1 — Cold-start test
Pretend you've never seen this project before. On your own machine:
```bash
git clone https://github.com/sreekarseera/phishdetect-ai.git
cd phishdetect-ai/backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 train_model.py     # only needed if model/model.joblib isn't already in the repo
uvicorn app:app --reload
```
Then load `extension/` as an unpacked extension in Chrome (`chrome://extensions` → Developer Mode → Load unpacked) and try analyzing a message.

Write down **every single point where you got stuck or something wasn't obvious** — missing step, confusing error, unclear instruction. This is exactly what will happen if a judge or teammate tries to run it cold, so it needs to be smooth.

## Step 2 — Write the root `README.md`
There's currently no top-level README explaining what this project even is (only `extension/README.md`, which is extension-specific). Write one that covers, in order:
1. One-paragraph pitch: what PhishDetect AI does and why (scam/phishing message detector, Chrome extension + local ML backend)
2. Screenshot or short description of what the popup looks like/does
3. Setup instructions — using exactly what worked for you in Step 1, not a guess
4. Project structure (`backend/` vs `extension/`, one line each)

## Step 3 — Write `docs/DEMO_SCRIPT.md`
A short, literal script for the live demo — what to say and click, in order. Suggested flow:
1. One sentence on the problem ("phishing/scam messages are everywhere, this catches them before you click")
2. Paste a real-sounding scam message → click Analyze → point out the confidence score
3. Paste a normal message → click Analyze → show it doesn't false-positive
4. Add a sender email on a scam result → show it lands in Blocked Emails
5. Type the blocked email into a **Gmail compose window** (or any normal webpage) → the purple warning banner appears live as you type — this is the money moment, it's confirmed working. **Don't use Google Docs for this** (canvas rendering means live detection can't work there; Docs only shows the banner after a reload — usable as a bonus, not the main beat)
6. Export History as CSV → briefly show the data is real/exportable
7. One closing line on what's genuinely custom here (a real trained model, not a hardcoded keyword list) vs. what's a known limitation (small-ish training set, local-only — no deployed backend)

Keep every line short — this gets read out loud under time pressure, not read silently.

## Step 4 — Prepare backup scam/legit example messages
Collect ~6-8 test messages (mix of obvious and subtle scams, plus normal messages) in `docs/DEMO_SCRIPT.md` or a small `docs/demo-examples.txt`, so whoever's demoing isn't typing from memory or improvising live. Test each one against the real model first and note the actual result next to it, so there are no surprises during the live run.

## Done checklist
- [ ] Did a full cold-start clone-and-run, wrote down every rough edge
- [ ] `README.md` written and accurate to what you actually had to do
- [ ] `docs/DEMO_SCRIPT.md` written, short enough to read aloud in ~90 seconds
- [ ] 6-8 pre-tested example messages ready to paste during the demo
- [ ] Reported any bugs/rough edges found in Step 1 to Sreekar

## If you get stuck
Ping Sreekar. Don't spend more than ~20 minutes stuck on one thing — flag it instead.
