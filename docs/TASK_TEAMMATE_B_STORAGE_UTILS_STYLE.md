# Your task: Storage helpers, utility functions, and styling

## Goal
Write three small, self-contained files for the Chrome extension. None of these depend on the backend or on anyone else's work — you can start immediately and test entirely on your own.

## Files you own (only edit these)
- `extension/storage.js` (currently empty)
- `extension/util.js` (currently empty)
- `extension/style.css` (currently empty)

**Do not touch** any other file (especially `popup.html` / `manifest.json` — they're already correct). If you think another file needs to change, message Sreekar first.

## Why this matters
Sreekar's `popup.js` is going to call the exact function names below. If you rename something or change what it returns, his code breaks. Stick to these signatures exactly.

## Step 1 — `extension/storage.js`
A thin wrapper around Chrome's `chrome.storage.local` API, so the rest of the extension never has to touch `chrome.storage` directly. Export these five functions (use `export` since `popup.js` is loaded as `type="module"`):

```js
// Get the array of past analysis results. Returns [] if nothing saved yet.
export async function getHistory() {
  const { history = [] } = await chrome.storage.local.get("history");
  return history;
}

// Add one entry to history. entry = {text, label, score, explanation, timestamp}
export async function addHistoryEntry(entry) {
  const history = await getHistory();
  history.push(entry);
  await chrome.storage.local.set({ history });
}

// Get the array of blocked email addresses. Returns [] if none.
export async function getBlocklist() {
  const { blocklist = [] } = await chrome.storage.local.get("blocklist");
  return blocklist;
}

// Add an email to the blocklist (lowercase it, avoid duplicates).
export async function addBlocked(email) {
  const blocklist = await getBlocklist();
  const normalized = email.toLowerCase();
  if (!blocklist.includes(normalized)) {
    blocklist.push(normalized);
    await chrome.storage.local.set({ blocklist });
  }
}

// Remove an email from the blocklist.
export async function removeBlocked(email) {
  const blocklist = await getBlocklist();
  const updated = blocklist.filter(e => e !== email.toLowerCase());
  await chrome.storage.local.set({ blocklist: updated });
}
```
(This is a complete, working implementation — you can use it close to as-is.)

## Step 2 — `extension/util.js`
Two helper functions:

```js
// Turn an array of objects into a CSV file and trigger a download.
export function exportToCsv(rows, filename) {
  if (!rows.length) return;
  const headers = Object.keys(rows[0]);
  const csvLines = [
    headers.join(","),
    ...rows.map(row => headers.map(h => `"${String(row[h]).replace(/"/g, '""')}"`).join(","))
  ];
  const blob = new Blob([csvLines.join("\n")], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

// Pull email addresses out of a block of text.
export function extractEmails(text) {
  const matches = text.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g);
  return matches ? [...new Set(matches.map(e => e.toLowerCase()))] : [];
}
```
(Also complete — usable close to as-is.)

## Step 3 — `extension/style.css`
Style `extension/popup.html` (open it in a browser or via `chrome://extensions` once loaded, to see the current unstyled version). Look at the element IDs already in `popup.html`: `#input`, `#email`, `#analyze`, `#result`, `#history`, `#blocklist`, plus the export buttons. Go for the palette mentioned in `extension/README.md`: **off-white background, purple and gold accents**. Keep it simple — a clean popup (~350-400px wide is typical for Chrome extension popups), readable text, a clearly clickable "Analyze" button, and some visual distinction for scam vs. safe results in `#result` (e.g. red/gold tint for scam, green/purple tint for safe). Don't overthink it — a clean, legible popup beats an elaborate one you don't finish.

## Step 4 — Test it yourself, without needing the backend or Sreekar's code
You can test `storage.js` and `util.js` directly in Chrome's DevTools console once the extension is loaded unpacked (`chrome://extensions` → enable Developer Mode → "Load unpacked" → select the `extension/` folder → open the popup → right-click → Inspect):
```js
import('./storage.js').then(async m => {
  await m.addBlocked('test@example.com');
  console.log(await m.getBlocklist()); // should show ['test@example.com']
});
```
For `style.css`, just open `popup.html` and visually check it looks right after loading the unpacked extension and clicking the toolbar icon.

## Done checklist
- [ ] `storage.js` exports all 5 functions with these exact names, tested in the console
- [ ] `util.js` exports both functions, tested in the console
- [ ] `style.css` makes the popup look clean and on-brand (off-white/purple/gold)
- [ ] Told Sreekar it's ready, so he can plug it into `popup.js` / `banner.js`

## If you get stuck
Ping Sreekar. Don't spend more than ~20 minutes stuck on one thing — flag it instead.
