// Get the array of past analysis results. Returns [] if nothing saved yet.
export async function getHistory() {
  const { history = [] } = await chrome.storage.local.get("history");
  return history;
}

// Add one entry to history. entry = {text, label, score, explanation, timestamp}
// Skips the add if it's a re-analysis of the same text as the most recent
// entry, so repeated clicks on unchanged input don't spam duplicate rows.
export async function addHistoryEntry(entry) {
  const history = await getHistory();
  const last = history[history.length - 1];
  if (last && last.text === entry.text) return;
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
  const updated = blocklist.filter((e) => e !== email.toLowerCase());
  await chrome.storage.local.set({ blocklist: updated });
}
