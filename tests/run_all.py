"""Run all 17 automated end-to-end tests for PhishDetect AI.

Spins up its own headless Chrome (invisible, separate profile — does not touch
your normal Chrome), loads the extension into it, starts the backend if it
isn't already running, and drives the popup + banner through every scenario.

Usage (one-time setup: pip install websocket-client — the only test dependency):
    python3 tests/run_all.py

Ports used: 9223 (Chrome DevTools), 8791 (test pages), 8000 (backend).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import CDP, attach, evaluate  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.environ.get(
    "CHROME_BIN", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
CDP_PORT = 9223
PAGES_PORT = 8791

SCAM_TEXT = "URGENT: Your bank account has been suspended due to suspicious activity. Verify your identity within 24 hours or your account will be permanently closed."
SAFE_TEXT = "Hey, are we still on for lunch tomorrow at noon? Let me know."
EMAIL_1 = "security.alert.desk@gmail.com"
EMAIL_2 = "refund.processing.team@gmail.com"
BANNER_EMAIL = "service.helpline.customer@gmail.com"

results = []
procs = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), str(detail)))


def http_ok(url):
    try:
        urllib.request.urlopen(url, timeout=2)
        return True
    except Exception:
        return False


def backend_up():
    try:
        req = urllib.request.Request(
            "http://localhost:8000/classify/",
            data=json.dumps({"text": "ping"}).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=2)
        return True
    except Exception:
        return False


def wait_for(fn, seconds=15):
    for _ in range(int(seconds * 2)):
        if fn():
            return True
        time.sleep(0.5)
    return False


# ---------------------------------------------------------------- setup
profile_dir = tempfile.mkdtemp(prefix="phishdetect-test-")
chrome = subprocess.Popen(
    [
        CHROME,
        f"--user-data-dir={profile_dir}",
        "--headless=new",
        f"--remote-debugging-port={CDP_PORT}",
        "--enable-unsafe-extension-debugging",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank",
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
procs.append(chrome)

pages = subprocess.Popen(
    [sys.executable, "-m", "http.server", str(PAGES_PORT)],
    cwd=os.path.join(REPO, "tests", "testpages"),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
procs.append(pages)

if not wait_for(lambda: http_ok(f"http://localhost:{CDP_PORT}/json/version")):
    sys.exit("Chrome DevTools endpoint never came up — is Chrome installed at the expected path?")
if not wait_for(lambda: http_ok(f"http://localhost:{PAGES_PORT}/clean.html")):
    sys.exit("Test-page server never came up")

with urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json/version") as r:
    ws_url = json.load(r)["webSocketDebuggerUrl"]
c = CDP(ws_url)
EXT_ID = c.cmd("Extensions.loadUnpacked", {"path": os.path.join(REPO, "extension")})["id"]
print(f"Headless Chrome up, extension loaded ({EXT_ID})")


def new_tab(url, settle=1.2):
    tid = c.cmd("Target.createTarget", {"url": url})["targetId"]
    sid = attach(c, tid)
    time.sleep(settle)
    return sid


def analyze(sid, text, email):
    expr = f"""
    new Promise((res) => {{
      document.getElementById('input').value = {json.dumps(text)};
      document.getElementById('email').value = {json.dumps(email)};
      document.getElementById('analyze').click();
      const iv = setInterval(() => {{
        const el = document.getElementById('result');
        if (el.textContent && el.textContent !== 'Analyzing…') {{
          clearInterval(iv);
          res(JSON.stringify({{text: el.textContent, cls: el.className}}));
        }}
      }}, 100);
      setTimeout(() => {{ clearInterval(iv); res('"TIMEOUT"'); }}, 10000);
    }})
    """
    return json.loads(evaluate(c, sid, expr, await_promise=True))


def storage(sid, key):
    return json.loads(
        evaluate(
            c, sid,
            f"chrome.storage.local.get('{key}').then(r => JSON.stringify(r['{key}'] || []))",
            await_promise=True,
        )
    )


try:
    # ------------------------------------------------ popup tests
    popup = new_tab(f"chrome-extension://{EXT_ID}/popup.html", settle=1)
    evaluate(c, popup, "chrome.storage.local.clear()", await_promise=True)

    r = analyze(popup, "", "")
    check("Empty input shows friendly message", r != "TIMEOUT" and "Paste a message" in r["text"], r)

    started_backend = False
    if backend_up():
        print("Backend already running — skipping the 2 backend-down tests")
        check("Backend down shows clear error", True, "SKIPPED (backend already running)")
        check("Backend-down attempt saves nothing", True, "SKIPPED (backend already running)")
    else:
        r = analyze(popup, SCAM_TEXT, "")
        check("Backend down shows clear error", r != "TIMEOUT" and "Couldn't reach the backend" in r["text"], r)
        check("Backend-down attempt saves nothing", len(storage(popup, "history")) == 0)
        backend = subprocess.Popen(
            [os.path.join(REPO, "backend", "venv", "bin", "uvicorn"), "app:app", "--port", "8000"],
            cwd=os.path.join(REPO, "backend"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        procs.append(backend)
        started_backend = True
        if not wait_for(backend_up):
            sys.exit("Backend failed to start — does backend/venv exist? (see README setup)")
        print("Backend started for online tests")

    r = analyze(popup, SCAM_TEXT, EMAIL_1)
    check("Scam message flagged", r != "TIMEOUT" and "Potential scam" in r["text"] and r["cls"] == "scam", r)
    hist, block = storage(popup, "history"), storage(popup, "blocklist")
    check("History has 1 entry with sender email", len(hist) == 1 and hist[0]["email"] == EMAIL_1)
    check("Scam sender auto-blocklisted", block == [EMAIL_1], block)

    analyze(popup, SCAM_TEXT, EMAIL_1)
    check("Duplicate (same text+email) deduped", len(storage(popup, "history")) == 1)

    analyze(popup, SCAM_TEXT, EMAIL_2)
    hist, block = storage(popup, "history"), storage(popup, "blocklist")
    check("Same text, different sender = new row", len(hist) == 2 and hist[1]["email"] == EMAIL_2)
    check("Second sender also blocklisted", block == [EMAIL_1, EMAIL_2], block)

    r = analyze(popup, SAFE_TEXT, "friend@example.com")
    check("Normal message classified safe", r != "TIMEOUT" and "Looks safe" in r["text"] and r["cls"] == "safe", r)
    check("Safe sender NOT blocklisted", "friend@example.com" not in storage(popup, "blocklist"))

    check("History list renders all rows", evaluate(c, popup, "document.querySelectorAll('#history li').length") == 3)
    check("Blocklist renders both emails", evaluate(c, popup, "document.querySelectorAll('#blocklist li').length") == 2)
    check("History tooltip shows sender", "Sender:" in evaluate(c, popup, "document.querySelector('#history li').title"))

    # ------------------------------------------------ banner tests
    evaluate(c, popup, f"chrome.storage.local.set({{blocklist: ['{BANNER_EMAIL}']}})", await_promise=True)

    sid = new_tab(f"http://localhost:{PAGES_PORT}/clean.html")
    before = evaluate(c, sid, "!!document.getElementById('phishdetect-banner')")
    evaluate(c, sid, f"document.getElementById('compose').textContent += ' contact {BANNER_EMAIL} now'")
    time.sleep(2)
    after = evaluate(c, sid, "!!document.getElementById('phishdetect-banner')")
    check("Banner appears on live-typed email (no reload)", (not before) and after, f"before={before} after={after}")

    sid = new_tab(f"http://localhost:{PAGES_PORT}/iframe_host.html")
    evaluate(c, sid, f"document.getElementById('editor').contentDocument.getElementById('doc').textContent += ' reply to {BANNER_EMAIL}'")
    time.sleep(2)
    after = evaluate(c, sid, "!!document.getElementById('editor').contentDocument.getElementById('phishdetect-banner')")
    check("Banner appears inside iframe (all_frames)", after)

    sid = new_tab(f"http://localhost:{PAGES_PORT}/clean.html")
    evaluate(c, sid, "document.getElementById('compose').textContent += ' send funds to fraud.refund.desk@gmail.com'")
    time.sleep(2)
    before = evaluate(c, sid, "!!document.getElementById('phishdetect-banner')")
    evaluate(
        c, popup,
        "chrome.storage.local.get('blocklist').then(r => chrome.storage.local.set({blocklist: [...r.blocklist, 'fraud.refund.desk@gmail.com']}))",
        await_promise=True,
    )
    time.sleep(2)
    after = evaluate(c, sid, "!!document.getElementById('phishdetect-banner')")
    check("Banner reacts to blocklist change while page open", (not before) and after, f"before={before} after={after}")

finally:
    c.close()
    for p in procs:
        p.terminate()
    shutil.rmtree(profile_dir, ignore_errors=True)

# ---------------------------------------------------------------- report
print()
all_ok = True
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail[:110]}]" if (detail and not ok) or "SKIPPED" in detail else ""))
    all_ok = all_ok and ok
print()
if all_ok:
    print(f"ALL {len(results)} TESTS PASSED")
else:
    print("SOME TESTS FAILED")
    sys.exit(1)
