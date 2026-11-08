# Indonesian Gadget Search Engine — Agent Bootstrap Guide

This repository contains the final project for the **Penelusuran Informasi (Information Retrieval) 2025/2026** course at **FMIPA Universitas Syiah Kuala (USK)**.

---

## 1. Session Start Protocol (Mandatory for All AI Agents)

Whenever an AI agent starts a session in this repository:
1. **Identify the Active Member & Role**:
   - **Member 1 (Frontend & UI Lead)**: Responsible for `frontend/` (React, Vite, Tailwind, SplitView, Dashboard Recharts, slides).
   - **Member 2 (Fadhlur - Core IR & Backend Lead)**: Responsible for `backend/` (Preprocessing Sastrawi, Inverted Index Okapi BM25, Sentence-BERT, Evaluator, Docker Compose).
   - **Member 3 (Data & Academic Report Lead)**: Responsible for `crawler/`, `data/raw/`, and `docs/report/` (USK FMIPA thesis format Bab I–V, video recording).
2. **Read Living Documents**:
   - Read `docs/TEAM_WORKFLOW.md` for role boundaries, branch strategy, and git rules.
   - Read `docs/PROGRESS.md` to identify pending tasks, parallel vs dependent workflows, and current milestones.
3. **Check Branch**:
   - Never commit directly to `main`. Ensure work happens on `feature/frontend-ui`, `feature/core-ir-engine`, `feature/crawler-data`, or `docs/academic-report`.

---

## 2. Directory Isolation Rules

To prevent merge conflicts during multi-member collaboration:
- **Member 1 Workspace**: Only touches `frontend/` (components, pages, styles, `api.js`).
- **Member 2 (Fadhlur) Workspace**: Only touches `backend/` (engine, API endpoints, db, docker-compose).
- **Member 3 Workspace**: Only touches `crawler/`, `data/raw/`, and `docs/report/`.
- **Shared Files**: Root configuration (`Makefile`, `docker-compose.yml`, `data/ground_truth/`, `docs/PROGRESS.md`). Edits to shared files must be coordinated.

---

## 3. Mandatory Pre-PR Quality Gatekeeper

Before opening any Pull Request or asking for review, the agent **MUST** run the automated pre-flight quality verification script:

```bash
python3 scripts/verify_pipeline.py
```
or
```bash
make verify
```

All 7 quality gates must report `[PASS]`:
1. Gate 1: Directory & Scaffolding Hygiene
2. Gate 2: Data Layer & Ground Truth Integrity
3. Gate 3: Offline Index Verification (`inverted_index.json` & `embeddings.npy`)
4. Gate 4: Academic Report Completeness (USK FMIPA standards in `docs/report/`)
5. Gate 5: Living Progress Tracker & Workflow Parity (`docs/PROGRESS.md`)
6. Gate 6: Clean Text Policy Audit (Zero decorative pictographic emojis)
7. Gate 7: Automated Pytest Regression Test Suite (155+ tests green)

---

## 4. Progress Tracking Mandate

Every time a task or feature is completed:
- Open `docs/PROGRESS.md`
- Check off the completed item (`- [x]`)
- Update the component status table if the milestone advanced
- Commit the updated `docs/PROGRESS.md` as part of the feature commit or PR.

---

## 5. Mandatory GitHub Issue Linking in Pull Requests

When preparing or opening a Pull Request:
- The PR description **MUST** link to the associated GitHub Issue using standard closing keywords:
  - `Closes #1` or `Closes #2` for Frontend UI tasks (Member 1).
  - `Closes #3` or `Closes #4` for Core IR & Backend tasks (Member 2 Fadhlur).
  - `Closes #5` or `Closes #6` for Crawler & Academic Report tasks (Member 3).
  - `Closes #7` for Delivery, Docker, and Video tasks (All Members).
- Any PR submitted without an explicit issue link is considered non-compliant and will be rejected.

---

## 6. Issue Creation Protocol for Additional Tasks & Bugfixes

If unexpected bugs, additional tasks, or scope extensions arise:
1. **Create GitHub Issue First**: Run `ghx issue create` with standard title prefix (`[Frontend]`, `[Core IR]`, `[Data]`, `[Report]`, `[Bugfix]`) and proper labels (`frontend`, `core-ir`, `crawler-data`, `report`, `demo`, `enhancement`, `bug`).
2. **Register in `docs/PROGRESS.md`**: Add the issue link and task items to the tracker.
3. **Closing Explanatory Comments**: Always provide a detailed comment when closing or modifying an issue's status.

---

## 7. Clean Text Policy

Never use decorative icons or emojis in code, docstrings, commit messages, PR descriptions, or documentation files. Use standard Markdown headers, clean bullet points, or Lucide SVG icons in frontend components.

---

## 6. Language Conventions

- **Codebase & Engineering Docs**: Formal technical English for code, comments, docstrings, unit tests, commit messages, and technical specs.
- **Academic Report**: Formal academic Indonesian for `docs/report/` (Bab I–V, Abstrak, Lembar Pengesahan) compliant with USK FMIPA thesis guidelines.
- **Conversational Dialogue**: Adapts to the human partner's language (Indonesian).
