# Strix: pip install vs Clone Repository

**Short answer: NO, they are NOT the same**, but both give you a working `strix` command. Here's the full comparison:

---

## Installation Methods Comparison

```mermaid
flowchart TD
    START["Choose Installation Method"] --> OPTIONS
    
    OPTIONS --> PIP["1️⃣ pip install<br/>pip install strix-agent"]
    OPTIONS --> SCRIPT["2️⃣ Official Script<br/>curl -sSL https://strix.ai/install | bash"]
    OPTIONS --> REPO["3️⃣ Clone Repository<br/>git clone + poetry install"]
    
    PIP --> PIP_USE["🔧 End Users<br/>Standard Usage"]
    
    SCRIPT --> SCRIPT_USE["🔧 End Users<br/>Recommended"]
    
    REPO --> REPO_USE["👨‍💻 Developers<br/>Contributing/Testing"]
    
    PIP_USE --> PIP_PROS["✅ Pros: Simple, PyPI-managed<br/>❌ Cons: Version lag, no code access"]
    SCRIPT_USE --> SCRIPT_PROS["✅ Pros: Easy, self-contained binary<br/>❌ Cons: Version lag"]
    REPO_USE --> REPO_PROS["✅ Pros: Latest code, can modify<br/>❌ Cons: Manual setup, dev skills needed"]
    
    style PIP fill:#c8e6c9,stroke:#388e3c
    style SCRIPT fill:#c8e6c9,stroke:#388e3c
    style REPO fill:#fff9c4,stroke:#f9a825
```

---

## Detailed Comparison Table

| Feature | `pip install strix-agent` | `curl ... | bash` | `git clone + poetry` |
|---------|--------------------------|----------------------|----------------------|----------------------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐ Easy | ⭐⭐⭐ Manual |
| **Version** | Latest PyPI release | Latest release | **Latest commit (unreleased)** |
| **Code Access** | ❌ No | ❌ No | ✅ Yes |
| **Can Modify** | ❌ No | ❌ No | ✅ Yes |
| **Contributing** | ❌ No | ❌ No | ✅ Yes |
| **Dependencies** | Managed by pip | Bundled | Poetry managed |
| **Recommended For** | End users | Most users | Developers |
| **Docker Setup** | Manual | Auto-checked | Manual |
| **Updates** | `pip install -U` | Re-run script | `git pull` |

---

## Method 1: pip install (Standard Users)

```bash
# Quick install
pip install strix-agent

# Or with pipx (recommended - isolated environment)
pipx install strix-agent

# Verify
strix --version
```

**What you get:**
- Latest **released version** from PyPI
- All dependencies managed by pip
- Ready to use immediately
- ❌ Cannot modify source code
- ❌ May lag behind GitHub by days/weeks

---

## Method 2: Official Install Script (Recommended)

```bash
# The easy way
curl -sSL https://strix.ai/install | bash

# Verify
strix --version
```

**What you get:**
- Pre-built binary (platform-specific)
- Automatic Docker check
- PATH setup
- ✅ **Recommended for most users**
- ❌ Cannot modify source code

---

## Method 3: Clone Repository (Developers)

```bash
# Clone the repo
git clone https://github.com/usestrix/strix.git
cd strix

# Install dependencies
poetry install

# OR for development with extras
poetry install --with dev

# OR with specific extras (Vertex AI, etc.)
poetry install --extras vertex

# Run from source
poetry run strix --version

# Or install in editable mode
pip install -e .
```

**What you get:**
- ✅ **Latest code** (including unreleased features)
- ✅ Can **modify and test** code
- ✅ Can **contribute** back
- ✅ Access to **skills, docs, tests**
- ✅ Development tooling (linting, testing)
- ❌ Manual dependency management
- ❌ Requires Python/dev environment knowledge

---

## When to Use Each Method

```mermaid
flowchart LR
    subgraph USER_TYPE["👤 User Type"]
        PENTESTER["🎯 Pentester<br/>(Standard Usage)"]
        DEV["👨‍💻 Security Researcher<br/>(Want to Hack/Extend)"]
        CONTRIBUTOR["🤝 Contributor<br/>(Submit PRs)"]
    end
    
    subgraph RECOMMENDED["📋 Recommended Method"]
        PENTESTER -->|"pip install strix-agent"| REC1["✅ pip install or<br/>Official script"]
        DEV -->|"git clone + poetry"| REC2["✅ Clone repo"]
        CONTRIBUTOR -->|"git clone + poetry"| REC3["✅ Clone repo"]
    end
    
    style REC1 fill:#c8e6c9,stroke:#388e3c
    style REC2 fill:#fff9c4,stroke:#f9a825
    style REC3 fill:#fff9c4,stroke:#f9a825
```

| Scenario | Best Method |
|----------|-------------|
| Running pentests for clients | `pip install` or script |
| Quick testing of an app | `pip install` or script |
| Want latest features (unreleased) | Clone repo |
| Contributing to Strix | Clone repo |
| Modifying/extending Strix | Clone repo |
| Testing a specific branch/fix | Clone repo |
| CI/CD pipeline | `pip install` or script |

---

## For Your Pentesters: Recommendation

**For your pentesters doing actual security testing:**

```bash
# ✅ RECOMMENDED: Use pip or official script
pipx install strix-agent

# OR
curl -sSL https://strix.ai/install | bash
```

**For developers/contributors:**

```bash
# Clone for latest features
git clone https://github.com/usestrix/strix.git
cd strix
poetry install --with dev
```

---

## Quick Decision Guide

```
┌─────────────────────────────────────────────────────────────┐
│              WHICH INSTALLATION METHOD?                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Do you need to:                                           │
│                                                             │
│  1. JUST RUN STRIX for pentesting?                         │
│     → pip install strix-agent  ✅                          │
│                                                             │
│  2. Want the easiest setup?                                │
│     → curl -sSL https://strix.ai/install | bash  ✅        │
│                                                             │
│  3. Want LATEST code (unreleased features)?                │
│     → git clone + poetry install  ✅                       │
│                                                             │
│  4. Want to MODIFY or EXTEND Strix?                        │
│     → git clone + poetry install  ✅                       │
│                                                             │
│  5. Want to CONTRIBUTE to the project?                     │
│     → git clone + poetry install  ✅                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Version Access Comparison

```mermaid
timeline
    title : Version Timeline
    
    section Releases
    v0.8.0 : Jan 2026
    v0.8.1 : Feb 2026
    v0.8.2 : Mar 2026
    v0.8.3 : Apr 2026 : PyPI Release
    
    section Source (GitHub)
    New Feature A : Merged Apr 15
    New Feature B : Merged Apr 18
    Bug Fix X : Merged Apr 20
    
    section PyPI vs GitHub
    PyPI : v0.8.3 (Apr 2026) - May lag 1-2 weeks
    GitHub main : All features above - Always latest
```

---

## Running Strix on DGX Spark

For local LLM inference without cloud API costs, Strix can run on NVIDIA DGX Spark with Ollama or SGLang backends. The following screenshots show the DGX Spark environment:

<p align="center">
  <img src="../assets/screenshots/Screenshot from 2026-03-31 22-56-55.png" width="700" alt="DGX Spark Ubuntu system information" />
  <br/>
  <em>NVIDIA DGX Spark running Ubuntu — the hardware platform used for local LLM inference with Strix</em>
</p>

<p align="center">
  <img src="../assets/screenshots/Screenshot from 2026-03-31 22-57-19.png" width="800" alt="DGX Dashboard with GPU utilization and JupyterLab" />
  <br/>
  <em>DGX Dashboard showing system memory (11.88 GB used) and GPU utilization alongside JupyterLab — Strix leverages GPU-accelerated local inference for private, cost-free operation</em>
</p>

<p align="center">
  <img src="../assets/screenshots/Screenshot from 2026-03-31 22-59-57.png" width="800" alt="Ollama list showing local LLM models" />
  <br/>
  <em>Local LLM models available via Ollama on DGX Spark — large parameter models including qwen3.5:122b (81 GB), nemotron-3-super:120b (86 GB), and gpt-oss:120b (65 GB) for private inference</em>
</p>

---

## TL;DR

| Question | Answer |
|----------|--------|
| **Same functionality?** | ✅ Yes (when using latest release) |
| **Same version?** | ❌ No (pip/script may lag behind GitHub) |
| **Can modify code?** | ❌ pip/script = No / ✅ Repo = Yes |
| **Recommended for pentesters?** | ✅ pip/script |
| **Recommended for developers?** | ✅ Clone repo |
| **Recommended for contributors?** | ✅ Clone repo |