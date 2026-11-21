# Template Laporan Tugas Akhir / Proyek Akhir FMIPA USK

Direktori ini berisi acuan baku format penyusunan Laporan Proyek Akhir Mata Kuliah Penelusuran Informasi (Information Retrieval) FMIPA Universitas Syiah Kuala.

## Berkas Referensi

1. `template_ta_fmipa_usk_2024.pdf`: Salinan resmi dokumen Pedoman Tugas Akhir FMIPA Universitas Syiah Kuala Tahun 2024 (Lampiran 7 s.d. 17).
2. `PEDOMAN_FORMAT_USK.md`: Ringkasan spesifikasi teknis (ukuran font, margin 4-3-3-3 cm, spasi, sistematika bab, dan struktur pengesahan).

## Cara Menghasilkan Laporan

Laporan akhir dikompilasi secara otomatis dari berkas Markdown di `docs/report/*.md` menjadi PDF tunggal `docs/report/Kelompok_4.pdf`:

```bash
make report
```
atau
```bash
python3 -m crawler.build_report_pdf
```
