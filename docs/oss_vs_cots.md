## Open Source vs Commercial Strix Versions

Based on the docs and research, here's the key breakdown:

### Open Source (CLI) - Free
- **Apache 2.0 License** - fully open source
- Requires your own Docker, Python 3.12+, and **your own LLM API key**
- You pay for your own LLM token costs separately (~$0.50-$20/scan depending on model and depth)
- Local results saved to `strix_runs/`
- Full security toolkit: HTTP proxy, browser automation, terminal, Python runtime
- CI/CD integration via GitHub Actions
- Can use local models (Ollama, LM Studio) for free
- No managed platform, dashboards, or team features

### Commercial Platform (app.strix.ai)

| Tier | Price | What's Included |
|------|-------|----------------|
| **Basic** | $299/mo | 3 domains, 10 repos, 5 users |
| **Pro** | $750/mo | 10 domains, 50 repos, compliance reports |
| **Enterprise** | Custom | VPC/on-prem, SSO, unlimited scope, dedicated SLA |

**Key Platform Extras:**
- **No LLM config needed** - managed for you, consistent quality
- **Continuous monitoring** across code, cloud, infrastructure
- **One-click autofix** as ready-to-merge PRs
- **SOC 2 / ISO 27001 reports** (Pro+)
- **SSO/SCIM** (Enterprise)
- **Infrastructure testing** (Enterprise)
- **Integrations**: GitHub, Slack, Jira, Linear
- **Dashboards** for vulnerability management across teams

### Summary
The open-source version is the same core engine but requires DIY setup (bring your own LLM). The commercial platform adds managed infrastructure, compliance reporting, team features, and enterprise controls—but at significant monthly cost.