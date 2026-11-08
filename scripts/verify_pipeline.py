#!/usr/bin/env python3
"""
verify_pipeline.py — Automated Pre-Flight Quality Gatekeeper for Indonesian Gadget Search Engine.

Inspired by the contract-first verification pipeline in SiagaKita.
Enforces 7 quality gates before any team member opens a Pull Request:
  1. Directory & Scaffolding Hygiene
  2. Data Layer & Ground Truth Integrity
  3. Offline Index & Embeddings Verification
  4. Academic Report Completeness (USK FMIPA Thesis Standards)
  5. Living Progress Tracker & Workflow Parity
  6. Clean Text & Anti-Emoji Policy Audit
  7. Automated Pytest Regression Test Suite

Usage:
  python3 scripts/verify_pipeline.py [--fast] [--skip-tests] [--report-only]
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys


def find_repo_root() -> str:
    curr = os.path.abspath(os.getcwd())
    while curr != os.path.dirname(curr):
        if os.path.exists(os.path.join(curr, ".git")) or os.path.exists(os.path.join(curr, "docker-compose.yml")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(os.getcwd())


def gate_1_directory_hygiene(root: str) -> bool:
    print("\n--- Gate 1: Directory & Scaffolding Hygiene ---")
    required_dirs = [
        "crawler/spiders",
        "backend/app/engine",
        "frontend/src/components",
        "frontend/src/pages",
        "data/raw",
        "data/processed",
        "data/ground_truth",
        "evaluation_results",
        "docs/report",
        "docs/presentation",
        "docs/screenshots"
    ]
    required_files = [
        "docker-compose.yml",
        "Makefile",
        ".gitignore",
        "README.md",
        "docs/TEAM_WORKFLOW.md",
        "docs/PROGRESS.md",
        "backend/requirements.txt",
        "backend/Dockerfile",
        "frontend/package.json",
        "frontend/Dockerfile"
    ]

    all_passed = True
    for d in required_dirs:
        p = os.path.join(root, d)
        if not os.path.isdir(p):
            print(f"[FAIL] Missing directory: {d}")
            all_passed = False
        else:
            print(f"[PASS] Directory verified: {d}")

    for f in required_files:
        p = os.path.join(root, f)
        if not os.path.isfile(p):
            print(f"[FAIL] Missing root file: {f}")
            all_passed = False
        else:
            print(f"[PASS] File verified: {f}")

    return all_passed


def gate_2_data_layer_integrity(root: str) -> bool:
    print("\n--- Gate 2: Data Layer & Ground Truth Integrity ---")
    all_passed = True

    # 1. Check SQLite
    db_path = os.path.join(root, "data", "gadget.db")
    if not os.path.exists(db_path):
        print(f"[FAIL] SQLite database not found at {db_path}")
        all_passed = False
    else:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM documents")
            count = cursor.fetchone()[0]
            conn.close()
            if count == 0:
                print(f"[WARN] SQLite table 'documents' is empty ({count} rows). Run 'make index' to seed.")
            else:
                print(f"[PASS] SQLite database operational: {count} documents stored.")
        except Exception as e:
            print(f"[FAIL] SQLite verification error: {e}")
            all_passed = False

    # 2. Check Ground Truth
    q_file = os.path.join(root, "data", "ground_truth", "test_queries.json")
    j_file = os.path.join(root, "data", "ground_truth", "relevance_judgments.json")

    for gf in [q_file, j_file]:
        if not os.path.exists(gf):
            print(f"[FAIL] Missing ground truth file: {os.path.relpath(gf, root)}")
            all_passed = False
        else:
            try:
                with open(gf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if len(data) == 0:
                        print(f"[FAIL] Ground truth file is empty: {os.path.relpath(gf, root)}")
                        all_passed = False
                    else:
                        print(f"[PASS] Ground truth verified: {os.path.relpath(gf, root)} ({len(data)} items)")
            except Exception as e:
                print(f"[FAIL] JSON parse error in {os.path.relpath(gf, root)}: {e}")
                all_passed = False

    return all_passed


def gate_3_offline_index_verification(root: str) -> bool:
    print("\n--- Gate 3: Offline Index & Embeddings Verification ---")
    proc_dir = os.path.join(root, "data", "processed")
    bm25_idx = os.path.join(proc_dir, "inverted_index.json")
    sbert_emb = os.path.join(proc_dir, "embeddings.npy")
    doc_ids_file = os.path.join(proc_dir, "doc_ids.json")

    missing = []
    for f in [bm25_idx, sbert_emb, doc_ids_file]:
        if not os.path.exists(f):
            missing.append(os.path.relpath(f, root))

    if missing:
        print(f"[FAIL] Missing offline index files: {', '.join(missing)}")
        print("[HINT] Run 'python3 -m backend.app.engine.indexer' or 'make index' to build indices.")
        return False

    try:
        with open(bm25_idx, "r", encoding="utf-8") as f:
            idx_data = json.load(f)
            vocab_size = len(idx_data.get("inverted_index", {}))
            print(f"[PASS] Inverted Index valid (Vocabulary: {vocab_size} unique terms).")

        import numpy as np
        emb_matrix = np.load(sbert_emb)
        print(f"[PASS] S-BERT Embeddings valid (Matrix shape: {emb_matrix.shape}).")
        return True
    except Exception as e:
        print(f"[FAIL] Error validating index files: {e}")
        return False


def gate_4_academic_report_completeness(root: str) -> bool:
    print("\n--- Gate 4: Academic Report Completeness (USK FMIPA Standards) ---")
    report_files = [
        "docs/report/00_Halaman_Judul_dan_Pengesahan.md",
        "docs/report/01_Abstrak_dan_Abstract.md",
        "docs/report/BAB_I_Pendahuluan.md",
        "docs/report/BAB_II_Tinjauan_Kepustakaan.md",
        "docs/report/BAB_III_Metode_Penelitian.md",
        "docs/report/BAB_IV_Hasil_dan_Pembahasan.md",
        "docs/report/BAB_V_Kesimpulan_dan_Saran.md",
        "docs/report/Daftar_Pustaka.md",
        "docs/report/Lampiran_Kontribusi_Anggota.md",
        "docs/presentation/5_MINUTE_DEMO_SCRIPT.md"
    ]

    all_passed = True
    for rf in report_files:
        p = os.path.join(root, rf)
        if not os.path.exists(p):
            print(f"[FAIL] Missing academic report chapter: {rf}")
            all_passed = False
            continue

        size = os.path.getsize(p)
        if size < 200:
            print(f"[FAIL] Report chapter too short (<200 bytes): {rf} ({size} bytes)")
            all_passed = False
        else:
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            if "TBD" in content or "TODO" in content:
                print(f"[WARN] Placeholder found in {rf}")
            print(f"[PASS] Chapter verified: {rf} ({size} bytes)")

    return all_passed


def gate_5_progress_and_workflow_parity(root: str) -> bool:
    print("\n--- Gate 5: Living Progress Tracker & Workflow Parity ---")
    prog_path = os.path.join(root, "docs", "PROGRESS.md")
    wf_path = os.path.join(root, "docs", "TEAM_WORKFLOW.md")

    if not os.path.exists(prog_path):
        print("[FAIL] Missing docs/PROGRESS.md")
        return False
    if not os.path.exists(wf_path):
        print("[FAIL] Missing docs/TEAM_WORKFLOW.md")
        return False

    with open(prog_path, "r", encoding="utf-8") as f:
        prog_text = f.read()

    checked_tasks = prog_text.count("- [x]")
    total_tasks = checked_tasks + prog_text.count("- [ ]")
    print(f"[PASS] Living Progress Tracker checked: {checked_tasks}/{total_tasks} checklist items completed.")

    if checked_tasks == 0:
        print("[FAIL] No tasks checked in docs/PROGRESS.md! Please check off your completed work.")
        return False

    return True


def gate_6_clean_text_policy_audit(root: str) -> bool:
    print("\n--- Gate 6: Clean Text & Anti-Emoji Policy Audit ---")
    # Disallow decorative pictographic emojis in repository source and docs
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
        "]",
        flags=re.UNICODE
    )

    scan_dirs = ["crawler", "backend/app", "frontend/src", "docs"]
    violations = []

    for s_dir in scan_dirs:
        dir_path = os.path.join(root, s_dir)
        if not os.path.exists(dir_path):
            continue
        for root_dir, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith((".py", ".jsx", ".js", ".html", ".md", ".css")):
                    file_path = os.path.join(root_dir, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            for idx, line in enumerate(f, 1):
                                if emoji_pattern.search(line):
                                    violations.append(f"{os.path.relpath(file_path, root)}:{idx}: {line.strip()[:60]}")
                    except Exception:
                        pass

    if violations:
        print(f"[FAIL] Clean Text Policy Violation: Found {len(violations)} decorative emojis in source text:")
        for v in violations[:5]:
            print(f"  - {v}")
        if len(violations) > 5:
            print(f"  ... and {len(violations) - 5} more.")
        return False

    print("[PASS] Clean Text Policy passed: Zero decorative icons/emojis found in codebase & docs.")
    return True


def gate_7_pytest_regression_suite(root: str, skip: bool = False) -> bool:
    print("\n--- Gate 7: Automated Test Suites (Backend Pytest & Frontend Vitest) ---")
    if skip:
        print("[SKIP] Skipping test suites as requested (--skip-tests).")
        return True

    venv_python = os.path.join(root, ".venv", "bin", "python")
    python_bin = venv_python if os.path.exists(venv_python) else sys.executable

    cmd = [python_bin, "-m", "pytest", "tests/", "-v"]
    env = os.environ.copy()
    env["PYTHONPATH"] = root

    print(f"[RUN] Running Backend Suite: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=root, env=env)

    if result.returncode != 0:
        print(f"[FAIL] Pytest test suite failed with exit code {result.returncode}")
        return False

    frontend_dir = os.path.join(root, "frontend")
    if os.path.isdir(frontend_dir) and shutil.which("npm"):
        print("[RUN] Running Frontend Vite build & Vitest suite...")
        fe_build = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
        if fe_build.returncode != 0:
            print(f"[FAIL] Frontend build failed:\n{fe_build.stderr}")
            return False

        fe_test = subprocess.run(
            ["npm", "test", "--", "--run"],
            cwd=frontend_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
        if fe_test.returncode != 0:
            print(f"[FAIL] Frontend tests failed:\n{fe_test.stderr}")
            return False

        print("[PASS] Frontend build and Vitest suite passed successfully.")

    print("[PASS] Automated test suites passed successfully (100% green).")
    return True


def main():
    parser = argparse.ArgumentParser(description="Pre-Flight Quality Gatekeeper for Indonesian Gadget Search Engine")
    parser.add_argument("--fast", action="store_true", help="Run fast verification without heavy operations")
    parser.add_argument("--skip-tests", action="store_true", help="Skip pytest test suite")
    parser.add_argument("--report-only", action="store_true", help="Only verify report and documentation gates")
    args = parser.parse_args()

    repo_root = find_repo_root()
    print("=" * 70)
    print("INDONESIAN GADGET SEARCH ENGINE — PRE-FLIGHT QUALITY GATEKEEPER")
    print(f"Repository Root: {repo_root}")
    print("=" * 70)

    results = []

    if not args.report_only:
        results.append(("Gate 1: Directory & Scaffolding Hygiene", gate_1_directory_hygiene(repo_root)))
        results.append(("Gate 2: Data Layer & Ground Truth Integrity", gate_2_data_layer_integrity(repo_root)))
        results.append(("Gate 3: Offline Index Verification", gate_3_offline_index_verification(repo_root)))

    results.append(("Gate 4: Academic Report Completeness", gate_4_academic_report_completeness(repo_root)))
    results.append(("Gate 5: Progress & Workflow Parity", gate_5_progress_and_workflow_parity(repo_root)))
    results.append(("Gate 6: Clean Text Policy Audit", gate_6_clean_text_policy_audit(repo_root)))

    if not args.report_only:
        results.append(("Gate 7: Pytest Regression Suite", gate_7_pytest_regression_suite(repo_root, skip=args.skip_tests)))

    print("\n" + "=" * 70)
    print("PRE-FLIGHT QUALITY VERIFICATION SUMMARY")
    print("=" * 70)

    all_passed = True
    for gate_name, status in results:
        status_str = "[PASS]" if status else "[FAIL]"
        print(f"{status_str:<8} | {gate_name}")
        if not status:
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("RESULT: ALL GATES PASSED! The branch is clean and ready for Pull Request.")
        sys.exit(0)
    else:
        print("RESULT: VERIFICATION FAILED. Please resolve all blocking gates before opening a PR.")
        sys.exit(1)


if __name__ == "__main__":
    main()
