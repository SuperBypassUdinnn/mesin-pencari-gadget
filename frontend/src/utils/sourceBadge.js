const SOURCE_BADGE_CLASSES = {
  Gadgetren: "badge badge-gadgetren",
  "Jagat Review": "badge badge-jagat",
  Droidlime: "badge badge-droidlime",
  Yangcanggih: "badge badge-yangcanggih",
  Hybrid: "badge badge-hybrid",
};

const FALLBACK_BADGE_CLASS =
  "badge border-slate-200 bg-slate-100 text-slate-700";

export function getSourceBadgeClass(source) {
  return SOURCE_BADGE_CLASSES[source] || FALLBACK_BADGE_CLASS;
}
