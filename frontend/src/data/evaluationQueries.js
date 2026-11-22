// Mirrors data/ground_truth/test_queries.json plus the exact/semantic split
// documented in the report (q01-q08 exact, q09-q15 semantic).
export const EVALUATION_QUERIES = {
  q01: { text: "Xiaomi kamera Leica", type: "Eksak" },
  q02: { text: "ASUS Zenbook Intel OLED", type: "Eksak" },
  q03: { text: "smartwatch layar AMOLED baterai awet", type: "Eksak" },
  q04: { text: "laptop gaming NVIDIA RTX", type: "Eksak" },
  q05: { text: "smartphone chipset Snapdragon 8", type: "Eksak" },
  q06: { text: "layar AMOLED 120Hz fast charging", type: "Eksak" },
  q07: { text: "Samsung Galaxy Z Fold", type: "Eksak" },
  q08: { text: "smartphone MediaTek Dimensity 5G", type: "Eksak" },
  q09: {
    text: "smartphone fotografi malam hari minim cahaya",
    type: "Semantik",
  },
  q10: {
    text: "laptop tipis dan ringan untuk kerja mahasiswa",
    type: "Semantik",
  },
  q11: {
    text: "HP baterai tahan lama seharian tanpa sering cas",
    type: "Semantik",
  },
  q12: {
    text: "laptop layar akurat untuk editing video kreator",
    type: "Semantik",
  },
  q13: {
    text: "smartphone gaming kencang harga terjangkau",
    type: "Semantik",
  },
  q14: {
    text: "tablet layar luas untuk produktivitas dan hiburan",
    type: "Semantik",
  },
  q15: {
    text: "earbuds TWS peredam bising suara jernih",
    type: "Semantik",
  },
};

export function getEvaluationQueryMeta(queryId, row = {}) {
  const known = EVALUATION_QUERIES[queryId] || {};

  return {
    text: row.query || row.query_text || known.text || queryId || "-",
    type: row.query_type || known.type || "Tidak diketahui",
  };
}
