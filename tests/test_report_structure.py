"""Structure validation for the USK FMIPA academic report and presentation.

Validates that all 10 final report and presentation documents exist, are
substantial in content (more than 200 characters each), and contain the
required academic headings for each chapter following the USK FMIPA thesis
report guidelines (Lampiran 7, 8, 9, 11a, 11b, 12, 13).
"""

import os

import pytest

REPORT_DIR = "docs/report"
PRESENTATION_DIR = "docs/presentation"

# Mapping of each required document file to the academic headings that must
# appear (case-insensitive) within its content.
REQUIRED_DOCUMENTS = {
    os.path.join(REPORT_DIR, "00_Halaman_Judul_dan_Pengesahan.md"): [
        "Sampul",
        "Halaman Judul",
        "Lembar Pengesahan",
        "Pernyataan Bebas Plagiasi",
        "Kata Pengantar",
        "Daftar Isi",
    ],
    os.path.join(REPORT_DIR, "01_Abstrak_dan_Abstract.md"): [
        "Abstrak",
        "Abstract",
        "Kata Kunci",
        "Keywords",
    ],
    os.path.join(REPORT_DIR, "BAB_I_Pendahuluan.md"): [
        "BAB I",
        "Pendahuluan",
        "Latar Belakang",
        "Rumusan Masalah",
        "Maksud dan Tujuan",
        "Manfaat Penelitian",
    ],
    os.path.join(REPORT_DIR, "BAB_II_Tinjauan_Kepustakaan.md"): [
        "BAB II",
        "Tinjauan Kepustakaan",
        "Information Retrieval",
        "Preprocessing",
        "Sastrawi",
        "BM25",
        "Sentence-BERT",
        "Cosine Similarity",
        "MAP",
        "Latensi",
    ],
    os.path.join(REPORT_DIR, "BAB_III_Metode_Penelitian.md"): [
        "BAB III",
        "Metode Penelitian",
        "Lingkungan Implementasi",
        "Docker Compose",
        "FastAPI",
        "React",
        "Arsitektur Sistem",
        "Crawler",
        "Gadgetren",
        "Jagat Review",
        "Droidlime",
        "SQLite",
        "Ground Truth",
        "Evaluasi",
    ],
    os.path.join(REPORT_DIR, "BAB_IV_Hasil_dan_Pembahasan.md"): [
        "BAB IV",
        "Hasil dan Pembahasan",
        "Karakteristik Korpus",
        "Zipf",
        "Kueri Eksak",
        "Kueri Semantik",
        "Evaluasi",
        "BM25",
        "Sentence-BERT",
    ],
    os.path.join(REPORT_DIR, "BAB_V_Kesimpulan_dan_Saran.md"): [
        "BAB V",
        "Kesimpulan dan Saran",
        "Kesimpulan",
        "Saran",
    ],
    os.path.join(REPORT_DIR, "Daftar_Pustaka.md"): [
        "Daftar Pustaka",
        "Manning",
        "Robertson",
        "Reimers",
        "Gurevych",
        "Sastrawi",
    ],
    os.path.join(REPORT_DIR, "Lampiran_Kontribusi_Anggota.md"): [
        "Lampiran",
        "Kontribusi Anggota",
        "Tabel Kontribusi",
        "Member 1",
        "Member 2",
        "Member 3",
    ],
    os.path.join(PRESENTATION_DIR, "5_MINUTE_DEMO_SCRIPT.md"): [
        "Demo Script",
        "5 Menit",
        "Presentasi",
        "YouTube",
        "Anggota",
        "Pembagian Waktu",
    ],
}

MIN_LENGTH = 200


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.mark.parametrize("path", sorted(REQUIRED_DOCUMENTS.keys()))
def test_document_exists(path: str) -> None:
    assert os.path.isfile(path), f"Document {path} is missing"


@pytest.mark.parametrize("path", sorted(REQUIRED_DOCUMENTS.keys()))
def test_document_is_substantial(path: str) -> None:
    content = _read(path)
    assert len(content) > MIN_LENGTH, (
        f"Document {path} is too short: {len(content)} characters "
        f"(minimum {MIN_LENGTH} required)"
    )


@pytest.mark.parametrize("path", sorted(REQUIRED_DOCUMENTS.keys()))
def test_document_contains_required_headings(path: str) -> None:
    content = _read(path).lower()
    missing = [
        heading
        for heading in REQUIRED_DOCUMENTS[path]
        if heading.lower() not in content
    ]
    assert not missing, (
        f"Document {path} is missing required headings: {', '.join(missing)}"
    )


def test_all_ten_documents_present() -> None:
    assert len(REQUIRED_DOCUMENTS) == 10
