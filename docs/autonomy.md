# Full Autonomous Mode in Strix

---

## TL;DR: Strix IS Already Fully Autonomous! 🎯

There is **no separate "yolo mode" or "autonomous mode" flag**. Strix is designed from the ground up to be an **autonomous AI pentester**. What you're looking for is achieved by combining flags.

---

## The "Full Autonomous" Command

```bash
# This IS full autonomous mode:
strix -n --target https://target.com --scan-mode deep
```

| Flag | Purpose |
|------|---------|
| `-n` | Non-interactive (no TUI, no prompts) |
| `--scan-mode deep` | Maximum coverage, thorough testing |
| `--target` | Your target |

<p align="center">
  <img src="../assets/screenshots/Screenshot from 2026-03-31 22-58-16.png" width="800" alt="Strix launched from Windsurf IDE in autonomous mode" />
  <br/>
  <em>Launching Strix in autonomous mode from Windsurf IDE on DGX Spark — reconnaissance begins immediately after invocation with no human interaction required</em>
</p>

---

## Autonomy Levels

```mermaid
flowchart TD
    START["🎯 Choose Autonomy Level"] --> LEVELS
    
    LEVELS -->|"1. Minimal (HITL)"| L1["Interactive TUI + Human Oversight"]
    LEVELS -->|"2. Semi-Autonomous"| L2["Interactive, Human Reviews Findings"]
    LEVELS -->|"3. FULL AUTONOMOUS ⭐"| L3["No TUI, No Prompts, Unattended"]
    
    L1 --> CMD1["strix --target <target>"]
    L2 --> CMD2["strix -n --target <target>"]
    L3 --> CMD3["strix -n --target <target> --scan-mode deep"]
    
    L3 -.->|"Can add"| FULL1["+ --instruction 'guidance'"]
    FULL1 -.->|"Can add"| FULL2["+ --instruction-file ./scope.md"]
    FULL2 -.->|"Can add"| FULL3["+ -t <additional targets>"]
    
    style L3 fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    style CMD3 fill:#c8e6c9,stroke:#388e3c
```

---

## Autonomous Modes Comparison

```mermaid
flowchart LR
    subgraph MODES["⚙️ STRIX AUTONOMY MODES"]
        
        INTERACTIVE["🎨 INTERACTIVE MODE
        ═══════════════════════
        strix --target <target>
        
        • Full TUI interface
        • Real-time progress
        • Human can intervene
        • Pentester monitoring
        • Caido proxy access"]
        
        HEADLESS["⚡ HEADLESS/AUTONOMOUS
        ═══════════════════════
        strix -n --target <target>
        
        • No TUI (just CLI output)
        • Prints findings in real-time
        • No human intervention
        • Perfect for automation
        • CI/CD ready
        • Exit code: 0=clean, 2=vulns found"]
        
        FULL_AUTO["🚀 FULL AUTONOMOUS (DEEP)
        ═══════════════════════
        strix -n --target <target> \\
              --scan-mode deep
        
        • Maximum penetration
        • All vulnerability classes
        • Business logic testing
        • Full exploitation
        • Comprehensive PoCs
        • Complete reports"]
        
    end

    INTERACTIVE -->|"Remove TUI"| HEADLESS
    HEADLESS -->|"Maximize coverage"| FULL_AUTO

    style HEADLESS fill:#fff9c4,stroke:#f9a825
    style FULL_AUTO fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
```

---

## Complete Autonomous Commands

### Level 1: Semi-Autonomous (CI/CD Ready)
```bash
strix -n --target https://target.com --scan-mode quick
```
**Use:** PR checks, fast feedback

### Level 2: Autonomous (Standard)
```bash
strix -n --target https://target.com --scan-mode standard
```
**Use:** Regular pentests, staging testing

### Level 3: FULL AUTONOMOUS (Recommended for Unattended) ⭐
```bash
strix -n --target https://target.com --scan-mode deep
```
**Use:** Comprehensive security review, bug bounty, unattended scanning

### Level 4: Full Autonomous + Multi-Target
```bash
strix -n \
  --target ./ \
  --target https://staging.target.com \
  --scan-mode deep \
  --instruction-file ./scope.md
```
**Use:** Full white-box + black-box combined testing

---

## Environment Variables for Maximum Autonomy

```bash
# Core config (required)
export STRIX_LLM="openai/gpt-5.4"
export LLM_API_KEY="sk-..."

# Performance tuning
export STRIX_REASONING_EFFORT="high"      # Thorough analysis
export STRIX_SANDBOX_EXECUTION_TIMEOUT=120 # Tool timeout (seconds)
export LLM_TIMEOUT=300                     # LLM timeout (seconds)

# Optional: Add OSINT capabilities
export PERPLEXITY_API_KEY="pplx-..."

# Run!
strix -n --target https://target.com --scan-mode deep
```

---

## What "Full Autonomous" Means in Strix

```mermaid
flowchart TB
    subgraph AUTONOMOUS["🤖 FULL AUTONOMOUS EXECUTION"]
        A1["🎯 Analyze Target"] --> A2["🕵️ Reconnaissance"]
        A2 --> A3["🌐 Browser Automation"]
        A3 --> A4["🔄 HTTP Proxy Testing"]
        A4 --> A5["💉 Exploitation Attempts"]
        A5 --> A6["✅ PoC Validation"]
        A6 --> A7["📝 Report Generation"]
        A7 --> A8["📤 Export Results"]
        
        A2 -.->|"Automatic"| A3
        A3 -.->|"Automatic"| A4
        A4 -.->|"Automatic"| A5
        A5 -.->|"Automatic"| A6
    end

    subgraph EXTRAS["📋 Can Be Pre-Configured"]
        E1["Credentials in --instruction"]
        E2["Scope in --instruction-file"]
        E3["Focus areas: IDOR, XSS, etc."]
        E4["Exclusions: /admin/*"]
    end

    E1 -.->|"Optional guidance"| AUTONOMOUS
    E2 -.->|"Optional guidance"| AUTONOMOUS
    E3 -.->|"Optional guidance"| AUTONOMOUS
    E4 -.->|"Optional guidance"| AUTONOMOUS

    style AUTONOMOUS fill:#c8e6c9,stroke:#388e3c
    style EXTRAS fill:#e3f2fd,stroke:#1976d2
```

---

## Exit Codes (Automation-Friendly)

| Exit Code | Meaning | When Used |
|-----------|---------|-----------|
| `0` | ✅ No vulnerabilities found | Clean scan |
| `2` | ⚠️ Vulnerabilities found | Headless mode (`-n`) |
| `1` | ❌ Error/Interrupted | Any mode |

```bash
# Example automation script
#!/bin/bash
strix -n --target https://target.com --scan-mode deep

if [ $? -eq 2 ]; then
    echo "⚠️ Vulnerabilities found! Check strix_runs/"
    # Send alert, create ticket, etc.
else
    echo "✅ No vulnerabilities found"
fi
```

---

## Quick Reference: "YOLO" Command

```bash
# The equivalent of "full yolo mode" - just run and forget:
strix -n \
  --target https://target.com \
  --scan-mode deep \
  --instruction "Test everything. Full exploitation. Maximum severity focus."
```

---

## Summary

**There is NO separate "autonomous mode" flag** - Strix is designed to be autonomous by default. The `-n` flag simply removes the TUI for headless operation:

| Mode | Command | Human Needed? |
|------|---------|---------------|
| Interactive | `strix --target <t>` | Yes (monitoring) |
| Headless | `strix -n --target <t>` | Optional |
| **Full Autonomous** | `strix -n --target <t> --scan-mode deep` | **No** ⭐ |

**Recommendation for your pentesters:** Use `strix -n --target <target> --scan-mode deep` for unattended, fully autonomous scanning.