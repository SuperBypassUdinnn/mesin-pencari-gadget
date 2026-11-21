import { describe, it, expect, vi, afterEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import App from "./App.jsx";

afterEach(() => cleanup());

vi.mock("./services/api.js", () => ({
  api: {
    searchGadgets: vi.fn().mockResolvedValue({
      bm25: { results: [], latency_ms: 0 },
      sbert: { results: [], latency_ms: 0 },
    }),
    getDocument: vi.fn().mockResolvedValue({}),
    getHealth: vi.fn().mockResolvedValue({ status: "ok" }),
    getEvaluation: vi.fn().mockResolvedValue({
      bm25: {
        map: 0.4647,
        mean_p5: 0.7467,
        avg_latency_ms: 1.28,
        per_query_results: [],
      },
      sbert: {
        map: 0.2993,
        mean_p5: 0.5467,
        avg_latency_ms: 18,
        per_query_results: [],
      },
      test_queries_count: 15,
    }),
  },
}));

describe("App Component", () => {
  it("renders Navbar and SearchPage by default", () => {
    render(<App />);
    expect(screen.getByText("Pencarian Gadget")).toBeDefined();
    expect(screen.getByText("Pencarian")).toBeDefined();
    expect(screen.getByText("Evaluasi")).toBeDefined();
  });

  it("switches to the evaluation dashboard when the Evaluasi tab is clicked", async () => {
    render(<App />);

    fireEvent.click(screen.getAllByRole("button", { name: "Evaluasi" })[0]);

    expect(await screen.findByText("Evaluasi IR")).toBeDefined();
    expect(screen.getByText("Perbandingan Metrik Evaluasi")).toBeDefined();
  });
});
