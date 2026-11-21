import { describe, it, expect, vi, afterEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import Navbar from "./components/Navbar.jsx";
import SearchBar from "./components/SearchBar.jsx";
import ResultCard from "./components/ResultCard.jsx";
import SplitView from "./components/SplitView.jsx";
import SpecsModal from "./components/SpecsModal.jsx";
import MetricsTable from "./components/MetricsTable.jsx";

afterEach(() => cleanup());

const SAMPLE_ITEM = {
  id: "doc-1",
  title: "ASUS Zenbook 14 OLED Review",
  source: "Jagat Review",
  url: "https://example.com/review",
  category: "Laptop",
  date: "2026-01-01",
  score: 0.98,
  latency_ms: 1.3,
  snippet: "Laptop tipis dengan layar OLED dan performa tinggi.",
  specs: {
    chipset: "Intel Core Ultra 7",
    ram: "16 GB",
  },
};

describe("Responsive layout contracts", () => {
  it("SearchBar stacks quick suggestions and lets long pills wrap", () => {
    const { container } = render(
      <SearchBar value="" onChange={() => {}} onSearch={() => {}} loading={false} />
    );

    const suggestion = screen.getByText(
      "HP baterai tahan lama seharian tanpa sering cas"
    );
    expect(suggestion.className).toContain("w-full");
    expect(suggestion.className).toContain("sm:w-auto");
    expect(suggestion.className).toContain("text-left");
    expect(suggestion.className).toContain("leading-snug");
    expect(container.querySelector(".min-w-0")).not.toBeNull();
  });

  it("ResultCard wraps the metadata row and footer actions", () => {
    const { container } = render(
      <ResultCard item={SAMPLE_ITEM} onResultClick={() => {}} />
    );

    const article = container.querySelector("article");
    expect(article.className).toContain("p-4");
    expect(article.className).toContain("sm:p-5");
    expect(container.querySelectorAll(".flex-wrap").length).toBeGreaterThan(0);
    expect(container.querySelector(".sm\\:flex-row")).not.toBeNull();
  });

  it("SplitView collapses to one column until the large breakpoint", () => {
    const { container } = render(
      <SplitView
        bm25Results={[SAMPLE_ITEM]}
        sbertResults={[SAMPLE_ITEM]}
        bm25Latency={1.3}
        sbertLatency={18}
        onResultClick={() => {}}
      />
    );

    const columns = container.querySelector("section > div");
    expect(columns.className).toContain("flex-col");
    expect(columns.className).toContain("lg:flex-row");
    expect(screen.getByText("Okapi BM25")).toBeDefined();
    expect(screen.getByText("Sentence-BERT")).toBeDefined();
    expect(screen.getAllByText("1 hasil").length).toBe(2);
  });

  it("SpecsModal is scrollable and keeps the specs table horizontally safe", () => {
    render(
      <SpecsModal
        document={{
          ...SAMPLE_ITEM,
          content: "Ulasan lengkap perangkat dengan banyak detail teknis.",
        }}
        onClose={() => {}}
      />
    );

    const dialog = screen.getByRole("dialog");
    expect(dialog.className).toContain("p-3");
    expect(dialog.className).toContain("sm:p-4");
    expect(dialog.querySelector('[class*="max-h-"]')).not.toBeNull();
    expect(dialog.querySelector(".overflow-y-auto")).not.toBeNull();
    expect(dialog.querySelector(".overflow-x-auto")).not.toBeNull();
    expect(dialog.querySelector("table").className).toContain("min-w-[320px]");
  });

  it("MetricsTable exposes horizontal scroll on narrow screens", () => {
    const { container } = render(
      <MetricsTable
        data={{
          bm25: { map: 0.4647, mean_p5: 0.7467 },
          sbert: { map: 0.2993, mean_p5: 0.5467 },
        }}
      />
    );

    expect(container.querySelector(".overflow-x-auto")).not.toBeNull();
    expect(container.querySelector("table").className).toContain("min-w-[480px]");
  });
});

describe("Responsive interactions", () => {
  it("Navbar toggles the mobile menu and routes the selected view", () => {
    const onChangeView = vi.fn();
    render(<Navbar view="pencarian" onChangeView={onChangeView} />);

    const toggle = screen.getByRole("button", { name: "Buka menu" });
    expect(toggle.getAttribute("aria-expanded")).toBe("false");

    fireEvent.click(toggle);
    expect(toggle.getAttribute("aria-expanded")).toBe("true");

    const evaluasiButtons = screen.getAllByRole("button", { name: "Evaluasi" });
    fireEvent.click(evaluasiButtons[evaluasiButtons.length - 1]);

    expect(onChangeView).toHaveBeenCalledWith("evaluasi");
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
  });

  it("SearchBar fills the input and triggers search from a suggestion pill", () => {
    const onChange = vi.fn();
    const onSearch = vi.fn();
    render(
      <SearchBar value="" onChange={onChange} onSearch={onSearch} loading={false} />
    );

    fireEvent.click(screen.getByText("ASUS Zenbook Intel OLED"));

    expect(onChange).toHaveBeenCalledWith("ASUS Zenbook Intel OLED");
    expect(onSearch).toHaveBeenCalledWith("ASUS Zenbook Intel OLED");
  });

  it("ResultCard opens document details from the title and the specs button", () => {
    const onResultClick = vi.fn();
    render(<ResultCard item={SAMPLE_ITEM} onResultClick={onResultClick} />);

    fireEvent.click(screen.getByText(SAMPLE_ITEM.title));
    fireEvent.click(screen.getByText("Lihat Spesifikasi"));

    expect(onResultClick).toHaveBeenCalledTimes(2);
    expect(onResultClick).toHaveBeenCalledWith("doc-1");
  });

  it("SpecsModal closes through the button, the Escape key, and the backdrop", () => {
    const onClose = vi.fn();
    render(<SpecsModal document={SAMPLE_ITEM} onClose={onClose} />);

    fireEvent.click(screen.getByText("Tutup"));
    expect(onClose).toHaveBeenCalledTimes(1);

    fireEvent.keyDown(window, { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(2);

    const backdrop = document.querySelector('[aria-hidden="true"]');
    fireEvent.click(backdrop);
    expect(onClose).toHaveBeenCalledTimes(3);
  });
});
