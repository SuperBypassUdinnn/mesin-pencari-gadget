import { describe, it, expect, vi, afterEach } from "vitest";
import { buildSearchExport, downloadJson } from "./exportResults.js";

const originalCreateObjectURL = URL.createObjectURL;
const originalRevokeObjectURL = URL.revokeObjectURL;

function restoreUrlMethod(name, original) {
  if (original) {
    Object.defineProperty(URL, name, {
      configurable: true,
      writable: true,
      value: original,
    });
  } else {
    delete URL[name];
  }
}

afterEach(() => {
  restoreUrlMethod("createObjectURL", originalCreateObjectURL);
  restoreUrlMethod("revokeObjectURL", originalRevokeObjectURL);
  vi.restoreAllMocks();
});

describe("search result export", () => {
  it("builds a payload with both engines and the original query", () => {
    const payload = buildSearchExport({
      query: "ASUS Zenbook Intel OLED",
      bm25Results: [{ id: "bm25-1", score: 9.6 }],
      sbertResults: [{ id: "sbert-1", score: 0.87 }],
      bm25Latency: 1.2,
      sbertLatency: 18,
    });

    expect(payload.query).toBe("ASUS Zenbook Intel OLED");
    expect(payload.bm25.latency_ms).toBe(1.2);
    expect(payload.bm25.results).toHaveLength(1);
    expect(payload.sbert.latency_ms).toBe(18);
    expect(payload.sbert.results).toHaveLength(1);
    expect(typeof payload.exported_at).toBe("string");
  });

  it("downloads JSON through a temporary object URL", () => {
    const createObjectURL = vi.fn(() => "blob:mock");
    const revokeObjectURL = vi.fn();
    Object.defineProperty(URL, "createObjectURL", {
      configurable: true,
      writable: true,
      value: createObjectURL,
    });
    Object.defineProperty(URL, "revokeObjectURL", {
      configurable: true,
      writable: true,
      value: revokeObjectURL,
    });
    const click = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => {});

    const downloaded = downloadJson("hasil.json", { query: "q" });

    expect(downloaded).toBe(true);
    expect(createObjectURL).toHaveBeenCalledTimes(1);
    expect(click).toHaveBeenCalledTimes(1);
    expect(revokeObjectURL).toHaveBeenCalledWith("blob:mock");
    expect(document.querySelector('a[download="hasil.json"]')).toBeNull();
  });

  it("returns false when the browser cannot create object URLs", () => {
    Object.defineProperty(URL, "createObjectURL", {
      configurable: true,
      writable: true,
      value: undefined,
    });

    expect(downloadJson("hasil.json", { query: "q" })).toBe(false);
  });
});
