# Strix Pentesting Process - Mermaid.js Diagram

## Complete Pentesting Workflow

```mermaid
flowchart TB
    subgraph PREP["📋 PRE-ENGAGEMENT"]
        A[🎯 Define Scope] --> B[📝 Create Instruction File]
        B --> C[⚙️ Configure Strix Environment]
        C --> D[🔑 Set API Keys]
        D --> E[🐳 Ensure Docker Running]
    end

    PREP --> PHASE1

    subgraph PHASE1["🔍 PHASE 1: STATIC ANALYSIS (Source Code)"]
        P1A[📂 Clone Repository] --> P1B[🏃 Run Initial Scan]
        P1B --> P1C{"Source Detected?"}
        
        P1C -->|Yes| P1D[🔬 Source-Aware Triage]
        P1D --> P1D1[🔍 Semgrep SAST Scan]
        P1D1 --> P1D2[🌳 AST-Grep Analysis]
        P1D2 --> P1D3[🔑 Secret Detection<br/>Gitleaks + Trufflehog]
        P1D3 --> P1D4[📦 Dependency Scan<br/>Trivy]
        P1D4 --> P1D5[🏗️ Architecture Map]
        
        P1C -->|No| P1E[📊 Proceed to Dynamic Testing]
        
        P1D5 --> P1F[📝 Generate Static Findings Report]
        P1E --> P1F
        P1F --> P1G[🎯 Prioritize Vulnerabilities]
    end

    PHASE1 --> PHASE2

    subgraph PHASE2["⚡ PHASE 2: DYNAMIC VALIDATION (Staging/Dev)"]
        P2A[🚀 Launch Strix Against Staging] --> P2B["🎭 Authenticated Testing"]
        P2B --> P2C[🌐 Browser Automation<br/>XSS, CSRF, Auth Flows]
        P2C --> P2D[🔄 Proxy Interception<br/>IDOR, Injection Testing]
        P2D --> P2E[⚡ Active Exploitation<br/>PoC Development]
        
        P2E --> P2F[✅ Validate Static Findings]
        P2F --> P2G[🆕 Discover New Vulnerabilities]
        
        P2G --> P2H{More Targets?}
        P2H -->|Yes| P2A
        P2H -->|No| P2I[📊 Cross-Reference Results]
        P2I --> P2J[🎯 Prioritize Findings]
    end

    PHASE2 --> PHASE3

    subgraph PHASE3["🏭 PHASE 3: PRODUCTION SCANNING"]
        P3A[⚠️ Safety Review] --> P3B[📋 Confirm Authorization]
        P3B --> P3C[🐢 Conservative Rate Limiting]
        P3C --> P3D[🔍 Read-Only Reconnaissance]
        P3D --> P3E[🎯 Targeted Exploitation<br/>Only High Severity]
        P3E --> P3F[📸 Document All Findings]
        P3F --> P3G[📝 Final Vulnerability Report]
    end

    PHASE3 --> REPORT

    subgraph REPORT["📊 REPORTING & REMEDIATION"]
        R1[📄 Consolidate All Findings] --> R2[🎯 Risk Prioritization<br/>CVSS Scoring]
        R2 --> R3[📝 Generate PoC for Each Finding]
        R3 --> R4[🔧 Auto-Fix Generation<br/>Where Possible]
        R4 --> R5[📤 Export Reports<br/>JSON, HTML, Markdown]
        R5 --> R6[🎯 Hand Off to Dev Team]
    end

    PH1FILL[#e8f4ea]
    P1D -.-> P1D5
    P1G -.-> P2A
    P2J -.-> P3A
    
    classDef phase1 fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef phase2 fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef phase3 fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef report fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    classDef prep fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class PREP prep
    class PHASE1 phase1
    class PHASE2 phase2
    class PHASE3 phase3
    class REPORT report
```

---

## Scan Modes Decision Flow

```mermaid
flowchart TD
    START([🚀 Start Strix]) --> MODE{"📊 Select Scan Mode"}
    
    MODE -->|Quick| Q1[⏱️ ~10 Minutes]
    MODE -->|Standard| S1[⏱️ ~30 Minutes]
    MODE -->|Deep| D1[⏱️ 1-3 Hours]
    
    Q1 --> Q2["🧪 Essential Vulnerabilities Only"]
    S1 --> S2["📋 Standard Security Coverage"]
    D1 --> D2["🔬 Comprehensive Testing"]
    
    Q2 --> Q3["✅ CI/CD Integration"]
    Q3 --> Q4["✅ PR Security Checks"]
    Q4 --> Q5["✅ Changed Files Scope"]
    
    S2 --> S3["✅ Routine Testing"]
    S3 --> S4["✅ Staging Environments"]
    S4 --> S5["✅ Regular Pentests"]
    
    D2 --> D3["✅ Full Vulnerability Classes"]
    D3 --> D4["✅ Business Logic Testing"]
    D4 --> D5["✅ Complex Applications"]
    
    Q5 --> END
    S5 --> END
    D5 --> END
    END([✅ Scan Complete])
    
    classDef quick fill:#c8e6c9,stroke:#2e7d32
    classDef standard fill:#fff9c4,stroke:#f9a825
    classDef deep fill:#ffccbc,stroke:#d84315
    
    class Q1,Q2,Q3,Q4,Q5 quick
    class S1,S2,S3,S4,S5 standard
    class D1,D2,D3,D4,D5 deep
```

---

## Multi-Agent Architecture

```mermaid
flowchart TB
    subgraph ORCHESTRATOR["🎯 Strix Orchestrator Agent"]
        O1[📋 Analyze Target] --> O2[📊 Create Attack Plan]
        O2 --> O3[👥 Spawn Specialized Agents]
        O3 --> O4[🔄 Coordinate Testing]
        O4 --> O5[📝 Consolidate Findings]
    end
    
    subgraph AGENTS["👥 Specialized Testing Agents"]
        A1[🌐 Recon Agent<br/>OSINT, Subdomains, Ports]
        A2[🔍 SAST Agent<br/>Static Code Analysis]
        A3[💉 Injection Agent<br/>SQL, NoSQL, Command]
        A4[🔐 Auth Agent<br/>JWT, Sessions, IDOR]
        A5[🖥️ XSS Agent<br/>Reflected, Stored, DOM]
        A6[⚙️ Logic Agent<br/>Race Conditions, Workflows]
    end
    
    subgraph TOOLS["🛠️ Agent Tools"]
        T1[🌐 Browser<br/>Playwright]
        T2[🔄 Proxy<br/>Caido]
        T3[💻 Terminal<br/>Kali Tools]
        T4[🐍 Python<br/>Custom Exploits]
        T5[🔍 Scanners<br/>Nuclei, SQLMap]
    end
    
    O3 --> A1
    O3 --> A2
    O3 --> A3
    O3 --> A4
    O3 --> A5
    O3 --> A6
    
    A1 --> T1
    A1 --> T2
    A2 --> T3
    A3 --> T2
    A3 --> T4
    A3 --> T5
    A4 --> T2
    A4 --> T4
    A5 --> T1
    A5 --> T2
    A6 --> T4
    A6 --> T5
    
    A1 -->|Findings| O4
    A2 -->|Findings| O4
    A3 -->|Findings| O4
    A4 -->|Findings| O4
    A5 -->|Findings| O4
    A6 -->|Findings| O4
    
    classDef orch fill:#e1bee7,stroke:#7b1fa2
    classDef agent fill:#bbdefb,stroke:#1976d2
    classDef tool fill:#dcedc8,stroke:#558b2f
    
    class ORCHESTRATOR orch
    class AGENTS agent
    class TOOLS tool
```

---

## Vulnerability Testing Flow

```mermaid
flowchart LR
    subgraph DETECTION["🔍 VULNERABILITY DETECTION"]
        D1[🎯 Identify Attack Surface] --> D2[🕵️ Select Attack Vector]
        D2 --> D3[⚡ Attempt Exploitation]
        D3 --> D4{❓ Vulnerable?}
    end
    
    D4 -->|Yes| V1[✅ VULNERABLE]
    D4 -->|No| V2[❌ Not Vulnerable]
    
    V1 --> VAL1[📸 Capture Evidence]
    VAL1 --> VAL2[💻 Develop PoC]
    VAL2 --> VAL3[📝 Document Finding]
    VAL3 --> VAL4[🎯 Assess Impact]
    VAL4 --> VAL5[📊 Calculate CVSS]
    VAL5 --> VAL6[🔧 Generate Fix]
    
    V2 --> END2
    
    VAL6 --> END2([📋 Next Vulnerability])
    
    classDef vuln fill:#ffcdd2,stroke:#d32f2f
    classDef safe fill:#c8e6c9,stroke:#388e3c
    classDef process fill:#e3f2fd,stroke:#1976d2
    
    class D1,D2,D3,D4,DETECTION process
    class V1,VAL1,VAL2,VAL3,VAL4,VAL5,VAL6 vuln
    class V2 safe
```

---

## Complete Pentesting Pipeline

```mermaid
sequenceDiagram
    participant P as Pentester
    participant S as Strix CLI
    participant D as Docker Sandbox
    participant LLM as AI Model
    participant T as Target App
    
    Note over P,L LM: PRE-ENGAGEMENT
    P->>S: Configure environment variables
    P->>S: Define scope & instructions
    
    Note over S,L LM: PHASE 1: STATIC ANALYSIS
    P->>S: strix --target ./repo --scan-mode deep
    S->>D: Launch Kali sandbox
    D->>D: Semgrep scan
    D->>D: Secret detection
    D->>D: Dependency scan
    D->>D: AST analysis
    D->>LLM: Analyze findings
    LLM-->>D: Risk prioritization
    D-->>S: Static findings report
    
    Note over S,L LM: PHASE 2: DYNAMIC VALIDATION
    P->>S: strix -t ./ -t https://staging.app.com
    S->>D: Start browser automation
    D->>T: Navigate & authenticate
    T-->>D: Application response
    D->>LLM: Analyze requests
    LLM-->>D: Attack strategies
    D->>T: Test IDOR vectors
    T-->>D: Potential IDOR response
    D->>D: Develop & validate PoC
    D->>LLM: Confirm vulnerability
    LLM-->>D: Verified finding
    D-->>S: Dynamic findings + PoCs
    
    Note over S,L LM: PHASE 3: PRODUCTION
    P->>S: strix --target https://app.com --instruction "conservative mode"
    S->>D: Configure safety limits
    D->>T: Passive reconnaissance
    D->>T: Targeted high-severity tests
    D-->>S: Production findings
    
    Note over S,L LM: REPORTING
    S->>S: Consolidate all findings
    S->>S: Generate reports (JSON/HTML/MD)
    S-->>P: Final vulnerability report
    P->>P: Hand off to development team
```

---

<p align="center">
  <img src="../assets/screenshots/Screenshot from 2026-03-31 22-53-39.png" width="800" alt="Strix penetration test completion summary" />
  <br/>
  <em>Strix penetration test completion — consolidated findings with remediation priorities and actionable next steps</em>
</p>

---

## Target Types & Input Methods

```mermaid
flowchart TD
    INPUT["🎯 INPUT TARGETS"] --> T1[📁 Local Directory<br/>./my-app]
    INPUT --> T2[🔗 GitHub Repo<br/>https://github.com/org/repo]
    INPUT --> T3[🌐 Web Application<br/>https://app.com]
    INPUT --> T4[🌐 API Endpoint<br/>https://api.app.com]
    INPUT --> T5[🏠 Domain<br/>example.com]
    INPUT --> T6[🔢 IP Address<br/>192.168.1.100]
    INPUT --> T7[📊 Multiple Targets<br/>-t ./ -t https://app.com]
    
    T1 --> OUT1["📋 White-Box Analysis<br/>Source + SAST"]
    T2 --> OUT2["📋 White-Box Analysis<br/>Repo Clone + Scan"]
    T3 --> OUT3["📋 Black-Box Testing<br/>Full Stack"]
    T4 --> OUT4["📋 API Security Testing<br/>REST/GraphQL"]
    T5 --> OUT5["📋 Domain Recon<br/>Subdomains, DNS"]
    T6 --> OUT6["📋 Network Scanning<br/>Port & Service Enum"]
    T7 --> OUT7["📋 Hybrid Testing<br/>Source + Live"]
    
    OUT1 --> FINAL["✅ COMPREHENSIVE<br/>SECURITY ASSESSMENT"]
    OUT2 --> FINAL
    OUT3 --> FINAL
    OUT4 --> FINAL
    OUT5 --> FINAL
    OUT6 --> FINAL
    OUT7 --> FINAL
    
    classDef input fill:#bbdefb,stroke:#1976d2
    classDef output fill:#c8e6c9,stroke:#388e3c
    classDef final fill:#fff9c4,stroke:#f9a825
    
    class T1,T2,T3,T4,T5,T6,T7 input
    class OUT1,OUT2,OUT3,OUT4,OUT5,OUT6,OUT7 output
    class FINAL final
```

---

## Skills & Vulnerability Coverage

```mermaid
mindmap
    root((🛡️ Strix Skills))
        Vulnerabilities
            SQL Injection
            XSS
            IDOR
            CSRF
            SSRF
            XXE
            RCE
            Business Logic
            Race Conditions
        Frameworks
            Django
            Express
            FastAPI
            Next.js
        Protocols
            GraphQL
            WebSocket
            OAuth
            REST API
        Reconnaissance
            Subdomain Enum
            Port Scanning
            OSINT
            Crawling
        Tooling
            Semgrep
            SQLMap
            Nuclei
            Nmap
            FFuf
            Katana
        Cloud
            AWS
            Azure
            GCP
            Kubernetes
        Source Analysis
            Semgrep SAST
            AST-Grep
            Gitleaks
            Trivy
            Tree-sitter
        Custom
            Community Skills
            Your Custom Rules
```

---

You can render these diagrams using any Markdown viewer that supports Mermaid (GitHub, GitLab, Notion, VS Code with Mermaid preview, etc.) or paste them into [mermaid.live](https://mermaid.live) for interactive viewing.