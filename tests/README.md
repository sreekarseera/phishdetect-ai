# Automated tests

17 end-to-end checks covering the popup flow (classify, history dedup, blocklist
auto-add, backend-down error) and the live banner (typed email, iframe, blocklist
change). Runs in an invisible headless Chrome with its own throwaway profile —
it never touches your normal Chrome, your tabs, or your extension's stored data.

## One-time setup

```bash
cd backend && source venv/bin/activate    # the usual backend venv
pip install websocket-client              # the only test-only dependency
```

## Run

```bash
python3 tests/run_all.py        # from the repo root, with the venv active
```

Takes ~30 seconds. If your backend is already running on :8000 it uses it (and
skips the 2 backend-down tests); otherwise it starts and stops one itself.

**Run this before every push.** If a test fails that passed before your change,
your change broke it — fix it or message Sreekar before pushing.

Chrome is expected at the standard macOS path; override with the `CHROME_BIN`
env var if yours lives elsewhere.
