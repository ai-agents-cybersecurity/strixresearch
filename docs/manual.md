# STRIX PENTESTER'S STRIP GUIDE

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STRIX COMMAND REFERENCE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INSTALLATION & CONFIG                                                     │
│  ────────────────────                                                       │
│  curl -sSL https://strix.ai/install | bash                                 │
│                                                                             │
│  export STRIX_LLM="openai/gpt-5.4"           # Required                     │
│  export LLM_API_KEY="sk-..."                # Required                     │
│  export PERPLEXITY_API_KEY="pplx-..."        # Optional (web search)       │
│  export STRIX_REASONING_EFFORT="high"        # Optional (none to xhigh)    │
│                                                                             │
│  CORE FLAGS                                                                 │
│  ──────────                                                                 │
│  -t, --target <target>    URL, repo, path, domain, IP (repeatable)         │
│  -n, --non-interactive    Headless mode (CI/CD, no UI)                      │
│  -m, --scan-mode          quick | standard | deep (default: deep)          │
│  --instruction "..."      Custom testing instructions                       │
│  --instruction-file <f>   Instructions from file                            │
│  --scope-mode             auto | diff | full (PR diff-scoping)             │
│  --diff-base <ref>        Branch/commit to compare against                  │
│  --config <file>          Custom config file (JSON)                         │
│                                                                             │
│  SCAN MODES                                                                │
│  ──────────                                                                 │
│  quick     Fast CI/CD checks (~10 min)                                      │
│  standard  Routine testing (~30 min)                                        │
│  deep      Thorough security review (1-3 hours) ← DEFAULT                  │
│                                                                             │
│  EXIT CODES                                                                 │
│  ──────────                                                                 │
│  0   No vulnerabilities found                                              │
│  2   Vulnerabilities found (headless mode only)                             │
│                                                                             │
│  RESULTS                                                                    │
│  ────────                                                                  │
│  Saved to: strix_runs/<run_name>/                                           │
│  • findings.json    Machine-readable results                                │
│  • report.html      HTML report                                            │
│  • report.md        Markdown report                                         │
│  • logs/            Execution logs                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

<p align="center">
  <img src="../assets/screenshots/Screenshot from 2026-03-31 22-52-31.png" width="800" alt="Strix reconnaissance phase starting" />
  <br/>
  <em>Strix deep scan starting — reconnaissance phase begins with target enumeration, HTTP probing, and agent initialization</em>
</p>

---

## Phase 1: Static Analysis of Cloned Repository

### 1.1 Initial Repository Scan

```bash
# Clone the target repository
git clone https://github.com/target/application.git
cd application

# Run deep static analysis (white-box with source)
strix --target ./ --scan-mode deep

# Or standard scan for faster results
strix --target ./ --scan-mode standard
```

### 1.2 Source-Aware SAST Triage

When Strix detects source code, it automatically leverages specialized skills:

```
Source-Aware Triage Stack:
├── semgrep         Fast security-first triage + custom rules
├── ast-grep (sg)   Structural AST pattern hunting
├── tree-sitter     Syntax-aware parsing
├── gitleaks        Secret detection (working tree)
├── trufflehog      Secret detection (full history)
└── trivy           Dependency & misconfiguration scanning
```

### 1.3 Targeted Static Analysis Instructions

```bash
# Focus on specific vulnerability classes
strix --target ./ \
  --instruction "Focus on: SQL injection, command injection, hardcoded secrets"

# SAST for specific languages/frameworks
strix --target ./ \
  --instruction "Run semgrep with Python and Django security rulesets"

# Secret scanning only
strix --target ./ \
  --instruction "Perform thorough secret scanning: API keys, tokens, passwords, SSH keys"

# Dependency vulnerability check
strix --target ./ \
  --instruction "Run trivy fs for dependency vulnerabilities and misconfigurations"
```

### 1.4 PR Diff-Scope for Code Reviews

```bash
# Scope to changed files only (great for PR reviews)
strix -n --target ./ \
  --scan-mode quick \
  --scope-mode diff \
  --diff-base origin/main

# Full diff analysis against a specific branch
strix -n --target ./ \
  --scan-mode standard \
  --scope-mode diff \
  --diff-base develop
```

---

## Phase 2: Dynamic Validation of Static Findings

### 2.1 Live Application Testing (Staging/Development)

```bash
# Authenticated testing with credentials
strix --target https://staging.target.com \
  --instruction "Login with username: testuser, password: TestPass123!

# API testing with authentication
strix --target https://api.staging.target.com \
  --instruction "Use API key: sk_live_xxx in Authorization: Bearer header"

# Multi-target: source + live app together
strix -t ./ \
  -t https://staging.target.com \
  --instruction "Cross-reference source findings with live API endpoints"
```

### 2.2 Custom Testing Instructions for Validation

```bash
# Validate specific findings from static scan
strix --target https://staging.target.com \
  --instruction "Validate these potential SQL injection points found in source:
  1. /api/users?id=<payload>
  2. /api/search?q=<payload>
  3. /api/reports?filter=<payload>"

# Focus on specific attack vectors
strix --target https://staging.target.com \
  --instruction "Focus on:
  - IDOR vulnerabilities in /api/users/{id}
  - JWT token validation bypass
  - Business logic flaws in checkout flow"

# Exclude certain areas
strix --target https://staging.target.com \
  --instruction "Do NOT test /admin/* endpoints. Focus on customer-facing APIs."
```

### 2.3 Instruction File Example

Create `pentest-instructions.md`:

```markdown
# Pentest Instructions for Target Application

## Scope
- https://staging.target.com
- API endpoints: /api/v1/*

## Authentication
- Test user: pentest@example.com
- Test password: P3nt3st!2024
- Admin user: admin@example.com
- Admin password: Adm1n!2024

## Focus Areas
1. Authentication bypass
2. Authorization/IDOR in user resources
3. SQL injection in search
4. Business logic in checkout

## Exclusions
- /internal/*
- /health/*
- Rate limiting tests (will be done separately)

## Known Issues (from static scan)
- Potential SQLi in /api/search (line 142 in search.py)
- Weak JWT secret in config (line 23 in auth.py)
```

Run with:
```bash
strix --target https://staging.target.com \
  --instruction-file ./pentest-instructions.md
```

---

## Phase 3: Production Environment Scanning

### 3.1 Production Testing (Authorized Only!)

```bash
# Read-only reconnaissance first
strix --target https://target.com \
  --scan-mode standard \
  --instruction "Perform passive reconnaissance only. No active exploitation."

# Authenticated production test
strix --target https://target.com \
  --scan-mode deep \
  --instruction "Use production test account:
  - email: pentest_prod@example.com
  - password: ProdT3st!
  - Test only read operations, no writes or modifications"

# API-focused production scan
strix --target https://api.target.com \
  --scan-mode standard \
  --instruction "Focus on public API endpoints. Use provided API key."
```

### 3.2 Production Safety Instructions

```bash
# Rate-limited testing to avoid disruption
strix --target https://target.com \
  --instruction "IMPORTANT: Production environment.
  - Use conservative rate limiting
  - No destructive operations
  - Test during maintenance window if possible
  - Focus on read-only vulnerabilities"

# Compliance-friendly testing
strix --target https://target.com \
  --scan-mode standard \
  --instruction "Perform non-intrusive vulnerability assessment.
  - No brute force or DoS testing
  - No data extraction or exfiltration
  - Focus on high-severity findings only"
```

---

## Advanced Testing Scenarios

### 4.1 Multi-Target Testing

```bash
# Source code + staging + production
strix -t ./ \
  -t https://staging.target.com \
  -t https://target.com

# Multiple domains/applications
strix -t https://app1.target.com \
  -t https://app2.target.com \
  -t https://api.target.com
```

### 4.2 Specific Vulnerability Testing

#### SQL Injection
```bash
strix --target https://target.com \
  --instruction "Focus on SQL injection testing:
  - Parameter: ?id=, ?user=, ?q=, ?search=
  - Methods: POST (body), GET (query), JSON body
  - Use sqlmap for confirmed vulnerabilities"
```

#### XSS/CSRF
```bash
strix --target https://target.com \
  --instruction "Focus on XSS and CSRF:
  - Reflected XSS in search parameters
  - Stored XSS in user profiles
  - DOM-based XSS in client-side JS
  - CSRF tokens in forms"
```

#### Authentication/Authorization
```bash
strix --target https://target.com \
  --instruction "Focus on auth testing:
  - JWT token manipulation (alg None, weak secrets)
  - Session fixation/hijacking
  - OAuth 2.0 misconfigurations
  - IDOR in /api/users/{id} endpoints
  - Privilege escalation to admin"
```

#### Business Logic
```bash
strix --target https://target.com \
  --instruction "Focus on business logic flaws:
  - Race conditions in checkout/payment
  - Workflow bypasses
  - Price manipulation
  - Coupon/promo code reuse
  - Integer overflow in quantities"
```

### 4.3 Framework-Specific Testing

```bash
# Django application
strix --target ./django_app \
  --instruction "Django-specific testing:
  - DEBUG mode enabled
  - Django DEBUG=True exposure
  - SQL injection via ORM
  - CSRF bypass in APIs
  - XSS in template filters"

# Node.js/Express API
strix --target ./express_api \
  --instruction "Node.js/Express testing:
  - Prototype pollution
  - Command injection in child_process
  -eval() usage
  - Path traversal in static files"

# GraphQL API
strix --target https://api.target.com/graphql \
  --instruction "GraphQL security testing:
  - Introspection enabled
  - Depth limiting bypass
  - Alias-based DoS
  - Information disclosure via __schema"
```

---

## Agent Tools Reference

### 5.1 Browser Automation (Playwright)

| Action | Description |
|--------|-------------|
| `launch` | Start browser |
| `goto` | Navigate to URL |
| `click` | Click element at coordinates |
| `type` | Fill form fields |
| `execute_js` | Run JavaScript |
| `new_tab` | Open new tab |
| `switch_tab` | Switch between tabs |
| `get_console_logs` | Capture JS console |
| `save_pdf` | Save page as PDF |

### 5.2 HTTP Proxy (Caido)

| Function | Description |
|----------|-------------|
| `list_requests()` | Query captured traffic with HTTPQL |
| `view_request(id, part)` | Get request/response details |
| `repeat_request(id, mods)` | Replay with modifications |
| `send_request(method, url)` | Send new HTTP request |
| `scope_rules()` | Manage scope allow/deny lists |
| `list_sitemap()` | View discovered endpoints |
| `view_sitemap_entry(id)` | Get sitemap entry details |

**Example - Automated IDOR Testing:**
```python
# Capture user requests
user_reqs = list_requests(
    httpql_filter='req.path.cont:"/users/"',
    page_size=50
)

# Test IDOR with different user IDs
for req in user_reqs['requests'][:10]:
    response = repeat_request(req['id'], {
        'url': req['path'].replace('/users/1', '/users/2')
    })
    if response['status_code'] == 200:
        print(f"POTENTIAL IDOR: {test_id}")
```

### 5.3 Terminal Tools

```bash
# Reconnaissance
subfinder -d target.com
naabu -host target.com
nmap -sV target.com
ffuf -u https://target.com/FUZZ -w wordlist.txt

# Web Testing
dirsearch -u https://target.com
arjun -u https://target.com/api/endpoint
katana -u https://target.com

# Vulnerability Scanning
nuclei -u https://target.com
sqlmap -u "https://target.com/?id=1"
wapiti -u https://target.com

# Source Analysis
semgrep --config p/default ./src
trufflehog filesystem ./
gitleaks detect --source .
trivy fs --scanners vuln ./.
```

---

## Scan Modes Deep Dive

| Mode | Duration | Use Case | Coverage |
|------|----------|----------|----------|
| **quick** | ~10 min | CI/CD, PR checks, changed files | Essential vulns only |
| **standard** | ~30 min | Routine testing, staging | Standard coverage |
| **deep** | 1-3 hrs | Full pentest, critical apps | Comprehensive |

```bash
# Quick scan for CI/CD
strix -n -t ./ --scan-mode quick

# Standard scan for regular testing
strix -t https://staging.target.com --scan-mode standard

# Deep scan for comprehensive assessment
strix -t https://target.com --scan-mode deep
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Install Strix
        run: curl -sSL https://strix.ai/install | bash

      - name: Run Quick Scan
        if: github.event_name == 'pull_request'
        env:
          STRIX_LLM: ${{ secrets.STRIX_LLM }}
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
        run: strix -n -t ./ --scan-mode quick --scope-mode diff

      - name: Run Deep Scan
        if: github.event_name == 'push'
        env:
          STRIX_LLM: ${{ secrets.STRIX_LLM }}
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
        run: strix -n -t ./ --scan-mode deep
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Docker not running | Start Docker Desktop |
| LLM connection failed | Verify API key and model name |
| Scan timeout | Increase `STRIX_SANDBOX_EXECUTION_TIMEOUT` |
| Out of memory | Use smaller scan scope or `quick` mode |
| No vulnerabilities found | Try different scan mode or provide more instructions |

### Debug Mode

```bash
# Enable verbose output
export STRIX_LOG_LEVEL=DEBUG
strix --target target.com

# Use specific model for better results
export STRIX_LLM="anthropic/claude-sonnet-4-6"
```

---

## Ethical Guidelines

> ⚠️ **IMPORTANT:** Only test applications you own or have explicit written permission to test. Unauthorized security testing is illegal.

**Authorized Testing:**
- ✅ Your own applications
- ✅ Client applications with written authorization
- ✅ Bug bounty programs (following their rules)
- ✅ Authorized penetration testing engagements

**Prohibited:**
- ❌ Testing third-party apps without permission
- ❌ Scanning public websites without authorization
- ❌ Any unauthorized access attempts

---

## Quick Command Templates

```bash
# Template 1: Full White-Box Pentest
strix -t ./ -t https://staging.target.com \
  --scan-mode deep \
  --instruction-file ./scope.md

# Template 2: Quick PR Security Check
strix -n -t ./ \
  --scan-mode quick \
  --scope-mode diff \
  --diff-base origin/main

# Template 3: Authenticated API Test
strix --target https://api.target.com \
  --scan-mode standard \
  --instruction "Use Bearer token: $TOKEN. Focus on IDOR and auth bypass."

# Template 4: Reconnaissance Only
strix --target https://target.com \
  --scan-mode quick \
  --instruction "Passive reconnaissance only. No active attacks."

# Template 5: Secret Scanning
strix --target ./ \
  --scan-mode quick \
  --instruction "Run gitleaks and trufflehog. Generate secret report only."
```

---

## Skills Reference

Strix agents can load specialized skills for enhanced testing:

| Category | Skills Available |
|----------|-------------------|
| **Vulnerabilities** | authentication_jwt, business_logic, csrf, idor, rce, sql_injection, ssrf, xss, xxe, race_conditions, path_traversal, information_disclosure |
| **Frameworks** | Django, Express, FastAPI, Next.js specific testing |
| **Technologies** | Supabase, Firebase, Auth0, payment gateways |
| **Protocols** | GraphQL, WebSocket, OAuth testing |
| **Tooling** | nmap, nuclei, ffuf, sqlmap, subfinder, naabu, katana |
| **Cloud** | AWS, Azure, GCP, Kubernetes security |
| **Recon** | OSINT, attack surface mapping |

---

## Support & Resources

- **Documentation:** docs.strix.ai
- **GitHub:** github.com/usestrix/strix
- **Discord:** discord.gg/strix-ai
- **Issues:** github.com/usestrix/strix/issues