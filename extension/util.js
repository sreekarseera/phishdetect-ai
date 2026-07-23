// Preferred CSV column order — chrome.storage returns object keys
// alphabetically, which puts "explanation" before "text" in exports.
const COLUMN_ORDER = ["text", "email", "label", "score", "explanation", "timestamp"];

// Turn an array of objects into a CSV file and trigger a download.
export function exportToCsv(rows, filename) {
  if (!rows.length) return;
  const keys = Object.keys(rows[0]);
  const headers = [
    ...COLUMN_ORDER.filter((k) => keys.includes(k)),
    ...keys.filter((k) => !COLUMN_ORDER.includes(k)),
  ];
  const csvLines = [
    headers.join(","),
    ...rows.map((row) =>
      headers.map((h) => `"${String(row[h]).replace(/"/g, '""')}"`).join(",")
    ),
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
  return matches ? [...new Set(matches.map((e) => e.toLowerCase()))] : [];
}
