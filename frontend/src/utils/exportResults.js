export function buildSearchExport({
  query,
  bm25Results,
  sbertResults,
  bm25Latency,
  sbertLatency,
}) {
  return {
    query: query || "",
    exported_at: new Date().toISOString(),
    bm25: {
      latency_ms: bm25Latency ?? 0,
      results: bm25Results || [],
    },
    sbert: {
      latency_ms: sbertLatency ?? 0,
      results: sbertResults || [],
    },
  };
}

export function buildExportFilename(date = new Date()) {
  const stamp = date.toISOString().replace(/[:.]/g, "-");
  return `hasil-pencarian-${stamp}.json`;
}

export function downloadJson(filename, data) {
  if (
    typeof document === "undefined" ||
    typeof URL === "undefined" ||
    typeof URL.createObjectURL !== "function"
  ) {
    return false;
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.rel = "noopener";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  return true;
}
