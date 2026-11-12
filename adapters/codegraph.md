# OMNI Capability Adapter: codegraph
> Origin: core_skills (~\.gemini\config\skills\codegraph\SKILL.md)
> Ingested: 2026-11-10 09:34:13
> Classification: DISTINCT_CAPABILITY (Related: codebase-design, Sim: 2%)
> Categories: Code Minimization & Pragmatism, Testing & Quality Assurance, Debugging & Root Cause, Memory & Knowledge Continuity, AST & Code Intelligence, Reverse Engineering & Inspection, Workflow & Planning

# CodeGraph v3.0: Multi-Language Structural AST, Complexity & Remote PR Engine

Dirancang untuk melakukan pemetaan struktur kode mendalam (*deep code intelligence*), analisis *call graph*, *symbol resolution*, skor kompleksitas siklomatis (*McCabe Cyclomatic Complexity*), dan deteksi *blast radius* secara instan baik pada repositori lokal (Python & TypeScript/JavaScript) maupun repositori jarak jauh via GitHub API tanpa perlu melakukan `git clone` penuh.

---

## 1. Kemampuan Inti CodeGraph v3.0

1. **Multi-Language AST Symbol Indexing (Python + TypeScript/JavaScript)**:
   - Python: Mengekstrak seluruh definisi fungsi, kelas, async handlers, decorator, signature parameter, type hints, dan line ranges via module `ast`.
   - TypeScript / JavaScript: Mengekstrak fungsi (`function`), arrow functions (`const foo = () => ...`), kelas (`class`), imports, dan call sites via structural regex parser.
   - Menyimpan indeks terpusat ke `scripts/codegraph_index.json` untuk pencarian O(1).

2. **McCabe Cyclomatic Complexity Engine**:
   - Menghitung poin keputusan logika cabang (`if`, `for`, `while`, `except`, `with`, `assert`, boolean operators) pada setiap simbol.
   - Mengidentifikasi simbol berisiko tinggi (`complexity > 10`) untuk mencegah regresi logika saat submit PR bounty.

3. **Inverted Call Graph & Centrality Analysis**:
   - Memetakan fungsi target (*callees*) ke seluruh pemanggilnya (*callers*) secara lintas-modul.
   - Mengidentifikasi simpul paling sentral (*Top 5 Most Central Architectural Symbols*) yang membutuhkan guardrail ketat.

4. **Multi-Depth Blast Radius Engine**:
   - Menghitung propagasi perubahan kode terhadap modul lain (router, services, tests, database drivers) hingga kedalaman $N$.
   - Kategori risiko: `MINIMAL`, `LOW`, `MEDIUM`, `HIGH/CRITICAL`.

5. **Zero-Disk-Bloat Remote PR Blast Radius Analyzer**:
   - Menganalisis PR upstream langsung via GitHub API (`--remote-pr <repo> <pr_number>`) tanpa kloning lokal.
   - Menghasilkan **Safety Verdict** (`100% CI SAFE`, `MEDIUM RISK`, `HIGH RISK`) dan daftar file downstream yang terdampak.

---

## 2. Arsitektur Alur Analisis

```
Target File / Symbol / Remote PR ──> [AST Parser & Complexity] ──> Extract Symbols, Calls & McCabe Score
                                                   │
                                                   ▼
Global Index ──────────────────────> [Inverted Graph] ──────────> Trace Transitive Callers (Depth N)
                                                   │
                                                   ▼
Modified Patch ────────────────────> [Blast Radius] ────────────> Downstream Impact & Risk Assessment
                                                   │
                                                   ▼
Remote PR Inspection ──────────────> [Safety Verdict] ──────────> 100% CI Safe & Zero-Regression Pass
```

---

## 3. Perintah CLI `graph_explorer.py`

Engine CodeGraph v3.0 tersedia di `scripts/graph_explorer.py` dan `.agents/skills/codegraph/scripts/graph_explorer.py`:

```bash
# 1. Memindai dan membangun indeks seluruh codebase (Python + TS/JS):
python scripts/graph_explorer.py --index

# 2. Menampilkan telemetri, statistik grafik, dan top architectural symbols:
python scripts/graph_explorer.py --stats

# 3. Menghitung dampak perubahan (Blast Radius) suatu fungsi:
python scripts/graph_explorer.py --blast-radius <symbol_name>

# 4. Mencari definisi simbol, signature, kompleksitas, dan seluruh callers:
python scripts/graph_explorer.py --symbol <symbol_name>

# 5. Menampilkan simbol-simbol dengan kompleksitas siklomatis tinggi (> 10):
python scripts/graph_explorer.py --complexity

# 6. Menganalisis blast radius PR jarak jauh (Remote PR) via GitHub API:
python scripts/graph_explorer.py --remote-pr BasedHardware/omi 22221

# 7. Menganalisis struktur satu file secara mendalam:
python scripts/graph_explorer.py --file scripts/dashboard_server.py
```

---

## 4. Protokol Penggunaan Saat Eksekusi Bounty

1. **Pre-Submission Remote PR Audit**:
   - Sebelum mengajukan patch atau setelah push branch, jalankan `python scripts/graph_explorer.py --remote-pr <repo> <pr_number>`.
   - Pastikan Safety Verdict bernilai `100% CI SAFE` sebelum meminta maintainer me-merge.

2. **Complexity Guardrail**:
   - Modifikasi kode dilarang meningkatkan kompleksitas siklomatis fungsi di atas ambang batas 15 tanpa pemecahan modul (*refactoring/helper isolation*).

3. **Hermetic Unit Test Isolation**:
   - Setiap fungsi baru wajib memiliki unit test terisolasi yang menguji semua jalur cabang keputusan (*decision branch coverage*).
