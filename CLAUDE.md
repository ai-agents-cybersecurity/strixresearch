# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **research and documentation repository** for [Strix](https://docs.strix.ai/) — an autonomous AI-powered penetration testing platform. There is no application code to build, test, or lint. The repo contains documentation, research papers, configuration templates, DGX setup scripts, sample pentest run outputs, and a deliberately vulnerable Flask app for testing.

## Repository Structure

- **`docs/`** — Core Strix documentation: command reference (`manual.md`), pentesting workflow diagrams (`process.md`), human-in-the-loop patterns (`hitl.md`), autonomous mode (`autonomy.md`), TLPT framework (`tltp.md`), evidence capture, OSS vs COTS comparison
- **`research/`** — Deep-dive analyses: multi-agent architecture (`multi_agent_architecture_deep_dive.md`), official Strix vs provoiceservices fork comparison, Caido proxy documentation, pip vs repo installation
- **`templates/e2e_template_blueprint/`** — End-to-end pentest configuration templates: `pentest-config.yaml` (5-phase YAML config), `.env.strix` (environment variables), `full-pentest-instructions.md` (instruction file for `--instruction-file` flag)
- **`scripts_dgx/`** — DGX Spark setup scripts for local LLM backends (Ollama and SGLang). Gitignored but present locally
- **`guides/ebanking-vulnerable/`** — Intentionally vulnerable Flask e-banking app with 10+ OWASP vulnerability categories, used as a Strix test target
- **`strix_runs/`** — Sample pentest output (events.jsonl, reports, vulnerability findings). Gitignored but present locally for reference
- **`assets/screenshots/`** — UI screenshots from Strix runs

## Key Concepts

### Strix Architecture
Strix uses a **multi-agent orchestration** pattern: a central orchestrator agent coordinates specialized testing agents (Recon, SAST, Injection, Auth, XSS, Logic, API). All HTTP traffic flows through a **Caido proxy** for interception/replay. Browser automation uses **Playwright**. The LLM backend is swappable via LiteLLM (OpenAI-compatible interface).

### Three Deployment Models
1. **Cloud API** — `STRIX_LLM="openai/gpt-5.4"` with provider API key
2. **Ollama (local)** — `STRIX_LLM="ollama/llama3.3:70b"`, setup via `scripts_dgx/setup-strix-ollama.sh`
3. **SGLang on DGX** — `STRIX_LLM="openai/gpt-oss-120b"`, setup via `scripts_dgx/setup-strix-sglang-dgx.sh`

### Three-Phase Testing Process
1. **Phase 1: Static Analysis** — Source code scanning (Semgrep, Gitleaks, Trivy)
2. **Phase 2: Dynamic Validation** — Live testing against staging/UAT (Playwright + Caido)
3. **Phase 3: Production Scanning** — Conservative read-only recon (rate-limited)

### Two Operation Modes
- **Interactive (HITL)** — `strix --target <t>` — TUI + Caido proxy for human collaboration
- **Headless/Autonomous** — `strix -n --target <t>` — No human needed, CI/CD friendly. Exit codes: 0=clean, 2=vulns found, 1=error

### Official vs Fork
The repo compares official `usestrix/strix` (single orchestrator, sequential) with the `provoiceservices/strix-pentest` fork (graph-of-agents, parallel execution, shared knowledge graph).

## Running the Vulnerable Test App

```bash
cd guides/ebanking-vulnerable
pip install -r requirements.txt
python app.py
# Runs on http://localhost:5000
# Default accounts: admin/admin123, john_doe/password123, jane_smith/welcome1
```

## Common Strix Commands

```bash
# Quick PR diff scan
strix -n -t ./ --scan-mode quick --scope-mode diff --diff-base origin/main

# Full autonomous deep scan
strix -n --target https://example.com --scan-mode deep

# Multi-target with instruction file
strix -n --target ./ --target https://staging.example.com --scan-mode deep --instruction-file ./scope.md

# Authenticated API test
strix -n --target https://api.example.com --scan-mode standard --instruction "Use Bearer token: $TOKEN"
```

## Working in This Repo

- All documentation is **Markdown**. Some docs use **Mermaid diagrams** (in `process.md`).
- Configuration templates use **YAML** (`pentest-config.yaml`) and shell env files (`.env.strix`).
- The `.gitignore` excludes `strix_runs/`, `scripts_dgx/`, generated pentest output directories, and real config files (keeps only templates/examples).
- When editing templates, preserve the `!template` / `example` naming convention so `.gitignore` rules work correctly.
- The ebanking app (`guides/ebanking-vulnerable/app.py`) is **intentionally vulnerable** — do not "fix" its security issues, they are the test cases.
