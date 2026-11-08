import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "./App.jsx";

describe("App Component", () => {
  it("renders Navbar and SearchPage by default", () => {
    render(<App />);
    expect(screen.getByText("Pencarian Gadget")).toBeDefined();
    expect(screen.getByText("Pencarian")).toBeDefined();
    expect(screen.getByText("Evaluasi")).toBeDefined();
  });
});
