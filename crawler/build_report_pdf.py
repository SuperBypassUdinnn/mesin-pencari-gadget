import base64
import html
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List

from markdown_it import MarkdownIt

REPORT_FILES = [
    "docs/report/00_Halaman_Judul_dan_Pengesahan.md",
    "docs/report/01_Abstrak_dan_Abstract.md",
    "docs/report/BAB_I_Pendahuluan.md",
    "docs/report/BAB_II_Tinjauan_Kepustakaan.md",
    "docs/report/BAB_III_Metode_Penelitian.md",
    "docs/report/BAB_IV_Hasil_dan_Pembahasan.md",
    "docs/report/BAB_V_Kesimpulan_dan_Saran.md",
    "docs/report/Daftar_Pustaka.md",
    "docs/report/Lampiran_Kontribusi_Anggota.md",
]

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    # macOS application bundles
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

BROWSER_COMMANDS = ["msedge", "microsoft-edge", "microsoft-edge-stable", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]


def _find_browser() -> str:
    for command in BROWSER_COMMANDS:
        resolved = shutil.which(command)
        if resolved:
            return resolved
    for path in EDGE_CANDIDATES:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(
        "No headless Chromium/Edge binary found on system. "
        "Install Microsoft Edge or Google Chrome (or set PATH to include it)."
    )


def _extract_braced(text: str, start: int) -> tuple[str, int]:
    """Extract balanced {...} group starting at index `start`."""
    if start >= len(text) or text[start] != "{":
        return "", start
    depth = 0
    for idx in range(start, len(text)):
        if text[idx] == "{":
            depth += 1
        elif text[idx] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : idx], idx + 1
    return text[start + 1 :], len(text)


def _replace_fracs(expr: str) -> str:
    """Replace nested \\frac{num}{den} expressions cleanly without regex brace issues."""
    out: List[str] = []
    i = 0
    while i < len(expr):
        if expr.startswith(r"\frac{", i):
            num, pos = _extract_braced(expr, i + 5)
            if pos < len(expr) and expr[pos] == "{":
                den, pos2 = _extract_braced(expr, pos)
                num_clean = _replace_fracs(num)
                den_clean = _replace_fracs(den)
                out.append(f"({num_clean}) / ({den_clean})")
                i = pos2
                continue
        out.append(expr[i])
        i += 1
    return "".join(out)


def _latex_to_readable_html(expr: str) -> str:
    """Convert subset of LaTeX math used in report chapters to clean HTML."""
    s = expr.strip()
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = _replace_fracs(s)
    replacements = [
        (r"\\left\(", "("),
        (r"\\right\)", ")"),
        (r"\\sum_\{([^}]*)\}\^\{([^}]*)\}", r"&Sigma;<sub>\1</sub><sup>\2</sup>"),
        (r"\\sum_\{([^}]*)\}", r"&Sigma;<sub>\1</sub>"),
        (r"\\ln", "ln"),
        (r"\\cdot", " &middot; "),
        (r"\\cap", " &cap; "),
        (r"\\in", " &isin; "),
        (r"\\hat\{u\}", "u&#770;"),
        (r"\\hat\{v\}", "v&#770;"),
        (r"\\hat\{V\}", "V&#770;"),
        (r"\\\|([^|]+)\\\|_2", r"||\1||<sub>2</sub>"),
        (r"\\\|", "||"),
        (r"\\quad", " &nbsp;&nbsp; "),
        (r"\{,\}", ","),
        (r"_\{([^}]*)\}", r"<sub>\1</sub>"),
        (r"\^\{([^}]*)\}", r"<sup>\1</sup>"),
        (r"_([A-Za-z0-9]+)", r"<sub>\1</sub>"),
        (r"\^([A-Za-z0-9]+)", r"<sup>\1</sup>"),
    ]
    for pattern, repl in replacements:
        s = re.sub(pattern, repl, s)
    return s.replace("{", "").replace("}", "")


def _preprocess_math(md_text: str) -> str:
    def _block_sub(match: re.Match) -> str:
        rendered = _latex_to_readable_html(match.group(1))
        return f'\n<div class="equation">{rendered}</div>\n'

    def _inline_sub(match: re.Match) -> str:
        rendered = _latex_to_readable_html(match.group(1))
        return f'<span class="inline-math">{rendered}</span>'

    md_text = re.sub(r"\$\$(.+?)\$\$", _block_sub, md_text, flags=re.DOTALL)
    md_text = re.sub(r"(?<!\$)\$([^$\n]+?)\$(?!\$)", _inline_sub, md_text)
    return md_text


def _embed_local_images(html_body: str, base_dir: Path) -> str:
    img_pattern = re.compile(r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)/?>', re.IGNORECASE)

    def _replace(match: re.Match) -> str:
        before, src, after = match.group(1), match.group(2), match.group(3)
        if src.startswith(("http://", "https://", "data:")):
            return match.group(0)
        img_path = (base_dir / src).resolve()
        if not img_path.is_file():
            return match.group(0)
        encoded = base64.b64encode(img_path.read_bytes()).decode("ascii")
        alt_match = re.search(r'alt="([^"]*)"', before + after)
        caption = html.unescape(alt_match.group(1)) if alt_match else ""
        cap_html = f"<figcaption>{html.escape(caption)}</figcaption>" if caption else ""
        return (
            f'<figure class="report-figure">'
            f'<img {before}src="data:image/png;base64,{encoded}"{after}/>'
            f"{cap_html}</figure>"
        )

    return img_pattern.sub(_replace, html_body)


def _render_front_matter(md: MarkdownIt, raw_text: str, base_dir: Path) -> str:
    md_front = MarkdownIt("commonmark", {"html": True, "breaks": True}).enable("table")
    parts = [p.strip() for p in raw_text.split("\n---\n") if p.strip()]
    sections: List[str] = []
    for idx, part in enumerate(parts):
        # Strip top "# Halaman Judul dan Pengesahan" header from the first chunk
        cleaned = re.sub(r"^#\s+Halaman Judul dan Pengesahan\s*", "", part).strip()
        is_cover = "## Sampul" in cleaned or "## Halaman Judul" in cleaned
        cleaned = re.sub(r"^##\s+(Sampul|Halaman Judul)\s*", "", cleaned).strip()
        html_part = md_front.render(_preprocess_math(cleaned))
        html_part = _embed_local_images(html_part, base_dir)
        cls = "front-cover page-break" if is_cover else "front-section page-break"
        sections.append(f'<section class="{cls}">{html_part}</section>')
    return "\n".join(sections)


def _render_chapter(md: MarkdownIt, path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if path.name.startswith("00_"):
        return _render_front_matter(md, raw, path.parent)
    processed = _preprocess_math(raw)
    rendered = md.render(processed)
    rendered = _embed_local_images(rendered, path.parent)
    return f'<section class="chapter page-break">{rendered}</section>'


def build_pdf(output_pdf: str = "docs/report/Kelompok_4.pdf") -> str:
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    sections = [_render_chapter(md, Path(p)) for p in REPORT_FILES]

    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8" />
<title>Laporan Proyek Akhir Penelusuran Informasi - Kelompok 4</title>
<style>
  @page {{
    size: A4;
    margin: 3cm 3cm 3cm 4cm;
  }}
  body {{
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #111827;
    margin: 0;
    padding: 0;
  }}
  .page-break {{
    page-break-after: always;
    break-after: page;
  }}
  section:last-child {{
    page-break-after: auto;
    break-after: auto;
  }}
  .front-cover {{
    text-align: center;
    padding-top: 24pt;
  }}
  .front-cover p {{
    text-align: center;
    margin: 12pt 0;
  }}
  .front-cover ol {{
    display: inline-block;
    text-align: left;
    margin: 8pt auto;
  }}
  .front-section h2, .chapter h1 {{
    text-align: center;
    font-size: 14pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 0;
    margin-bottom: 16pt;
  }}
  h2 {{
    font-size: 12.5pt;
    font-weight: bold;
    margin-top: 16pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 12pt;
    font-weight: bold;
    margin-top: 12pt;
    margin-bottom: 4pt;
    page-break-after: avoid;
  }}
  .chapter p, .front-section p {{
    text-align: justify;
    margin: 0 0 10pt 0;
  }}
  ul, ol {{
    margin: 6pt 0 10pt 0;
    padding-left: 20pt;
  }}
  li {{
    text-align: justify;
    margin-bottom: 4pt;
  }}
  code {{
    font-family: "Consolas", "Courier New", monospace;
    font-size: 10pt;
    background-color: #f3f4f6;
    padding: 1pt 3pt;
    border-radius: 2pt;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0 14pt 0;
    font-size: 10pt;
    line-height: 1.35;
  }}
  th, td {{
    border: 1px solid #374151;
    padding: 5pt 6pt;
    vertical-align: top;
    text-align: left;
  }}
  th {{
    background-color: #e5e7eb;
    font-weight: bold;
    text-align: center;
  }}
  tr {{
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  .equation {{
    text-align: center;
    margin: 10pt 0;
    padding: 6pt 10pt;
    font-style: italic;
    background: #f9fafb;
    border-left: 3px solid #2563eb;
  }}
  .inline-math {{
    font-style: italic;
  }}
  figure.report-figure {{
    margin: 12pt 0 16pt 0;
    text-align: center;
    break-inside: avoid;
    page-break-inside: avoid;
  }}
  figure.report-figure img {{
    max-width: 100%;
    height: auto;
    border: 1px solid #d1d5db;
  }}
  figure.report-figure figcaption {{
    font-size: 10pt;
    font-style: italic;
    color: #374151;
    margin-top: 5pt;
    text-align: center;
  }}
</style>
</head>
<body>
{''.join(sections)}
</body>
</html>
"""

    browser = _find_browser()
    out_path = Path(output_pdf).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(full_html)
        tmp_html = tmp.name

    try:
        cmd = [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={out_path}",
            Path(tmp_html).as_uri(),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0 or not out_path.is_file():
            raise RuntimeError(f"PDF export failed (code={result.returncode}): {result.stderr}")
    finally:
        if os.path.exists(tmp_html):
            os.remove(tmp_html)

    size_kb = out_path.stat().st_size / 1024.0
    print(f"[ReportPDF] Exported {output_pdf} ({size_kb:.1f} KB) using {os.path.basename(browser)}")
    return str(out_path)


if __name__ == "__main__":
    build_pdf()
