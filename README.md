# Strix Research

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Strix Docs](https://img.shields.io/badge/docs-strix.ai-green)](https://docs.strix.ai/)
[![Research](https://img.shields.io/badge/type-research-orange)]()

Research and documentation for [Strix](https://docs.strix.ai/) — an autonomous AI-powered penetration testing platform.

## Overview

This repository contains comprehensive research, documentation, and templates for using Strix in professional security testing engagements. It covers everything from basic usage patterns to advanced autonomous pentesting workflows.

## Contents

| Document | Description |
|----------|-------------|
| [`docs/manual.md`](docs/manual.md) | Complete command reference and usage guide |
| [`docs/process.md`](docs/process.md) | Pentesting workflow diagrams (Mermaid) |
| [`docs/hitl.md`](docs/hitl.md) | Human-in-the-Loop (HITL) architecture and collaboration patterns |
| [`docs/autonomy.md`](docs/autonomy.md) | Full autonomous mode configuration |
| [`docs/tltp.md`](docs/tltp.md) | Threat-Led Penetration Testing (TLPT) framework |
| [`docs/pip_vs_repo.md`](docs/pip_vs_repo.md) | Installation methods comparison |
| [`docs/oss_vs_cots.md`](docs/oss_vs_cots.md) | Open source vs commercial platform comparison |
| [`docs/evidence capture.md`](docs/evidence%20capture.md) | Screenshot and evidence collection capabilities |
| [`research/what_is_caido.md`](research/what_is_caido.md) | What is Caido and its role in Strix |
| [`research/strix_vs_fork_comparison.md`](research/strix_vs_fork_comparison.md) | Official Strix vs provoiceservices fork comparison |
| [`research/multi_agent_architecture_deep_dive.md`](research/multi_agent_architecture_deep_dive.md) | Deep dive: Specialized agents & collaborative discovery |
| [`guides/ebanking-vulnerable/`](guides/ebanking-vulnerable/) | Practical pentesting guides |
| [`templates/e2e_template_blueprint/`](templates/e2e_template_blueprint/) | End-to-end autonomous pentest templates |

## Official Strix vs Fork Comparison

| Aspect | Official Strix (`usestrix/strix`) | Fork (`provoiceservices/strix-pentest`) |
|--------|-----------------------------------|----------------------------------------|
| **Architecture** | Single orchestrator + agents | **Graph of Agents** — distributed workflow |
| **Agent Execution** | Sequential/Parallel (standard) | **Parallel execution** with dynamic coordination |
| **Scalability** | Standard (single-node) | **Distributed** — multi-target parallel testing |
| **Collaboration** | Standard reporting | **Real-time discovery sharing** between agents |
| **Best For** | Most pentesting engagements | **Large-scale, complex, multi-target environments** |
| **Maintenance** | Official (20k+ stars) | Community-maintained |

See full comparison: [`research/strix_vs_fork_comparison.md`](research/strix_vs_fork_comparison.md)

## Quick Start

```bash
# Install Strix
pip install strix-agent

# Or use the official installer
curl -sSL https://strix.ai/install | bash

# Run a quick scan
strix --target https://example.com --scan-mode quick

# Run full autonomous pentest
strix -n --target https://example.com --scan-mode deep
```

## Documentation

Official documentation: [https://docs.strix.ai/](https://docs.strix.ai/)

## License

Apache 2.0

---

*This is an independent research project documenting Strix capabilities and best practices.*
