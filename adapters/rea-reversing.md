# OMNI Capability Adapter: rea-reversing
> Origin: core_skills (~\.gemini\config\skills\rea-reversing\SKILL.md)
> Ingested: 2026-11-10 09:34:14
> Classification: DISTINCT_CAPABILITY (Related: codegraph, Sim: 2%)
> Categories: Testing & Quality Assurance, Frontend & Human Design, AST & Code Intelligence, Reverse Engineering & Inspection, Workflow & Planning

# REA Reverse Engineering & Binary Inspection Skill (v1.0)
**Engine**: `morluto/rea` (`rea-agents`) | **Tujuan**: Menghasilkan Pendapatan Finansial via Bug Bounty & Analisis Software Klien

---

## 1. Nilai Finansial & Kasus Penggunaan (Cari Uang)

Skill ini dirancang untuk mengubah biner, aplikasi mobile, dan desktop tertutup menjadi sumber pendapatan nyata:

1. **Bug Bounty (HackerOne / Bugcrowd / Intigriti)**:
   - **Ekstraksi Secrets**: Menemukan hardcoded token, API keys (AWS, Stripe, Firebase, JWT secrets), dan private private URLs di dalam APK / Electron app.
   - **Hidden API Surface Discovery**: Membedah rute API privat dan parameter tersembunyi yang tidak terlihat di web frontend biasa.
   - **Insecure IPC / Deeplink Exploits**: Menemukan kerentanan Android Intent redirection, exported activities, dan unsafe Electron IPC bridges.
2. **Reverse Engineering untuk Interoperabilitas & Scraping Berbayar**:
   - Membedah algoritma enkripsi parameter, signature hashing (`X-Signature`), atau handshake protocol pada klien tertutup untuk membangun scraper/integrator otomatis bagi klien korporat.
3. **Audit Kepatuhan & Keamanan Software Klien**:
   - Menghasilkan laporan audit keamanan statis berbasis bukti nyata untuk penawaran jasa security consulting.

---

## 2. Cara Kerja & Arsitektur

```
[Target: APK / ASAR / Binary / Bundle]
                  │
                  ▼
   [rea-agents MCP / CLI Runner]
   ├── 1. Format Detection (ELF, PE, Mach-O, Dex, JS)
   ├── 2. Structural Decompilation & AST Parsing
   └── 3. Boundary & Cross-Component Tracing
                  │
                  ▼
 [rea_inspector.py Secret & Surface Scanner]
   ├── Regex Pattern Matching (AWS, Stripe, Firebase, Private Keys)
   ├── Endpoint / URL Extractor (REST, GraphQL, WebSocket)
   └── Vulnerability Surface Classifier
                  │
                  ▼
 [Laporan Bug Bounty / Financial Lead Markdown]
```

---

## 3. Perintah Eksekusi Cepat (CLI)

Gunakan wrapper otonom di `scripts/rea_inspector.py`:

```powershell
# 1. Pindai file APK target untuk mencari hardcoded secrets dan private API endpoints
python .agents\skills\rea-reversing\scripts\rea_inspector.py --target "path\to\target.apk" --output "reports\target_apk_audit.json"

# 2. Pindai folder Electron app atau file .asar
python .agents\skills\rea-reversing\scripts\rea_inspector.py --target "path\to\app.asar" --type electron

# 3. Pindai binary native (PE .exe/.dll atau ELF)
python .agents\skills\rea-reversing\scripts\rea_inspector.py --target "path\to\binary.exe" --type native
```

Atau jalankan langsung modul `rea-agents` via `npx`:

```powershell
# Analisis aplikasi JavaScript / Electron
npx -y rea-agents@latest analyze-javascript-application "path/to/extracted/app" --json

# Setup REA MCP Server terhubung ke agen AI
npx rea-agents setup
```

---

## 4. Standar Pelaporan Temuan Bug Bounty

Setiap temuan bernilai finansial wajib didokumentasikan dengan struktur berikut:
1. **Target**: Nama file APK/Binary dan versi hash (SHA-256).
2. **Kategori Vulnerability**: Misal `Information Disclosure: Hardcoded Sensitive API Credential` (CWE-798).
3. **Lokasi Temuan**: Nama file, kelas, fungsi, dan offset offset string.
4. **Bukti Validasi (Proof of Concept)**: Bukti bahwa credential valid (misal cek status STS untuk AWS key atau API ping).
5. **Dampak Finansial & Mitigasi**: Risiko eskalasi privilege dan cara perbaikan.
