import {
  getHistory,
  addHistoryEntry,
  getBlocklist,
  addBlocked,
  removeBlocked,
} from "./storage.js";
import { exportToCsv } from "./util.js";

const BACKEND_URL = "http://localhost:8000/classify/";

const inputEl = document.getElementById("input");
const emailEl = document.getElementById("email");
const analyzeBtn = document.getElementById("analyze");
const resultEl = document.getElementById("result");
const historyEl = document.getElementById("history");
const blocklistEl = document.getElementById("blocklist");
const exportHistoryBtn = document.getElementById("exportHistory");
const exportBlocklistBtn = document.getElementById("exportBlocklist");

function showResult(text, kind) {
  resultEl.textContent = text;
  resultEl.className = kind; // "scam" | "safe" | "error"
}

async function renderHistory() {
  const history = await getHistory();
  historyEl.innerHTML = "";
  history
    .slice()
    .reverse()
    .forEach((entry) => {
      const li = document.createElement("li");
      const preview = entry.text.length > 50 ? entry.text.slice(0, 50) + "…" : entry.text;
      const label = entry.label === "LABEL_1" ? "🚩 Scam" : "✅ Safe";
      li.textContent = `${label} (${Math.round(entry.score * 100)}%) — ${preview}`;
      historyEl.appendChild(li);
    });
}

async function renderBlocklist() {
  const blocklist = await getBlocklist();
  blocklistEl.innerHTML = "";
  blocklist.forEach((email) => {
    const li = document.createElement("li");
    const span = document.createElement("span");
    span.textContent = email;
    const removeBtn = document.createElement("button");
    removeBtn.textContent = "✕";
    removeBtn.className = "remove-btn";
    removeBtn.addEventListener("click", async () => {
      await removeBlocked(email);
      await renderBlocklist();
    });
    li.appendChild(span);
    li.appendChild(removeBtn);
    blocklistEl.appendChild(li);
  });
}

analyzeBtn.addEventListener("click", async () => {
  const text = inputEl.value.trim();
  if (!text) {
    showResult("Paste a message first.", "error");
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing…";
  showResult("Analyzing…", "");

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    const data = await response.json();
    const isScam = data.label === "LABEL_1";

    showResult(
      `${isScam ? "🚩 Potential scam" : "✅ Looks safe"} (${Math.round(data.score * 100)}% confidence) — ${data.explanation}`,
      isScam ? "scam" : "safe"
    );

    await addHistoryEntry({
      text,
      label: data.label,
      score: data.score,
      explanation: data.explanation,
      timestamp: new Date().toISOString(),
    });

    const email = emailEl.value.trim();
    if (isScam && email) {
      await addBlocked(email);
      await renderBlocklist();
    }

    await renderHistory();
  } catch (err) {
    showResult(
      "⚠️ Couldn't reach the backend. Make sure it's running (uvicorn app:app --reload) on localhost:8000.",
      "error"
    );
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze";
  }
});

exportHistoryBtn.addEventListener("click", async () => {
  const history = await getHistory();
  exportToCsv(history, "history.csv");
});

exportBlocklistBtn.addEventListener("click", async () => {
  const blocklist = await getBlocklist();
  exportToCsv(
    blocklist.map((email) => ({ email })),
    "blocklist.csv"
  );
});

renderHistory();
renderBlocklist();
