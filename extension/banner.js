// Content script — runs on every page. Not loaded as an ES module (Chrome
// doesn't load declarative content scripts as modules), so this stays
// self-contained instead of importing storage.js/util.js.
(function () {
  let dismissed = false;

  function extractEmails(text) {
    const matches = text.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g);
    return matches ? [...new Set(matches.map((e) => e.toLowerCase()))] : [];
  }

  function showBanner(matchedEmails) {
    if (dismissed || document.getElementById("phishdetect-banner")) return;

    const banner = document.createElement("div");
    banner.id = "phishdetect-banner";
    banner.textContent = `⚠️ PhishDetect AI: this page mentions a blocked email address (${matchedEmails.join(", ")})`;
    banner.style.cssText = [
      "position:fixed", "top:0", "left:0", "right:0", "z-index:2147483647",
      "background:#6c3fa0", "color:#fff", "font-family:system-ui,sans-serif",
      "font-size:14px", "padding:10px 16px", "text-align:center",
      "box-shadow:0 2px 6px rgba(0,0,0,0.2)",
    ].join(";");

    const dismiss = document.createElement("button");
    dismiss.textContent = "✕";
    dismiss.style.cssText =
      "margin-left:12px;background:none;border:none;color:#fff;cursor:pointer;font-size:14px;";
    dismiss.addEventListener("click", () => {
      dismissed = true;
      banner.remove();
    });

    banner.appendChild(dismiss);
    document.body.prepend(banner);
  }

  function scanPage() {
    if (dismissed) return;
    chrome.storage.local.get("blocklist", ({ blocklist = [] }) => {
      if (!blocklist.length) return;
      const pageEmails = extractEmails(document.body.innerText);
      const matched = pageEmails.filter((email) => blocklist.includes(email));
      if (matched.length) showBanner(matched);
    });
  }

  scanPage();

  // Pages like Google Docs/Gmail render content after the initial load, or
  // update it live as the user types — a one-time scan misses that entirely,
  // which defeats the point of a "you're about to use a blocked address"
  // warning. Re-scan (debounced) whenever the page's content changes.
  let debounceTimer = null;
  const observer = new MutationObserver(() => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(scanPage, 800);
  });
  observer.observe(document.body, { childList: true, subtree: true, characterData: true });

  // Also re-scan immediately if the blocklist itself changes (e.g. the user
  // just blocked an email via the popup) while this tab is already open.
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area === "local" && changes.blocklist) scanPage();
  });
})();
