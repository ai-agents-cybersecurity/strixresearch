# Strix Human-in-the-Loop (HITL) Diagrams

## Complete HITL Architecture

```mermaid
flowchart TB
    subgraph HUMAN["👤 PENTESTER (You)"]
        H1[📊 Monitor TUI Output]
        H2[🖥️ Caido Desktop Proxy]
        H3[⌨️ Provide Real-time Instructions]
        H4[👁️ Inspect Traffic & Findings]
        H5[🎯 Guide Testing Focus]
        H6[✅ Validate & Approve Exploits]
    end

    subgraph STRIX["🤖 STRIX ORCHESTRATOR"]
        O1[🎯 Analyze Target]
        O2[📋 Create Testing Plan]
        O3[👥 Spawn Agents]
        O4[📊 Track Progress]
        O5[📝 Consolidate Findings]
    end

    subgraph SANDBOX["🐳 DOCKER SANDBOX"]
        subgraph AGENTS["👥 Testing Agents"]
            A1[🌐 Recon Agent]
            A2[💉 Injection Agent]
            A3[🔐 Auth Agent]
            A4[🖥️ XSS Agent]
        end

        subgraph TOOLS["🛠️ Tools"]
            T1[🌐 Browser<br/>Playwright]
            T2[🔄 Proxy<br/>Caido Server]
            T3[💻 Terminal]
            T4[🐍 Python]
        end
    end

    subgraph TARGET["🎯 TARGET APPLICATION"]
        APP1[Web App<br/>https://app.com]
        APP2[API<br/>api.app.com]
        APP3[Mobile Backend]
    end

    %% Human interactions
    HUMAN <-->|1. Real-time monitoring| STRIX
    HUMAN <-->|2. Intercept & modify traffic| T2
    HUMAN <-->|3. Inspect browser actions| T1
    HUMAN <-->|4. Provide guidance| SANDBOX

    %% Strix orchestration
    O3 --> AGENTS
    AGENTS --> TOOLS
    TOOLS --> TARGET

    %% Feedback loop
    H6 -->|5. Validate findings| O5
    O5 -->|6. Update strategy| O2

    %% Caido access
    T2 -.->|HTTP/HTTPS Traffic| H2
    H2 -.->|Replay with mods| T2

    classDef human fill:#e1bee7,stroke:#7b1fa2,stroke-width:3px
    classDef strix fill:#bbdefb,stroke:#1976d2,stroke-width:2px
    classDef sandbox fill:#c8e6c9,stroke:#388e3c
    classDef target fill:#ffccbc,stroke:#d84315

    class HUMAN human
    class STRIX strix
    class SANDBOX sandbox
    class TARGET target
```

---

<p align="center">
  <img src="../assets/screenshots/Screenshot from 2026-03-31 22-51-44.png" width="800" alt="Strix TUI with agent sidebar and findings" />
  <br/>
  <em>Strix TUI during a live pentest — the agent sidebar (right) shows all specialized agents and their status, while the main panel displays the executive summary with findings, exploitation results, and recommendations</em>
</p>

---

## HITL Collaboration Workflow

```mermaid
sequenceDiagram
    participant P as Pentester
    participant T as Strix TUI
    participant C as Caido Proxy
    participant AG as Strix Agents
    participant TB as Target Browser
    participant TA as Target App

    Note over P,TA: 🚀 PHASE 1: INITIALIZATION
    P->>T: strix --target https://app.com
    T->>C: Launch Caido Server
    C-->>T: localhost:52341
    T-->>P: Display Caido URL
    P->>C: Open in Caido Desktop
    C-->>P: Ready for inspection

    Note over P,TA: 🔄 PHASE 2: PARALLEL COLLABORATION
    par Autonomous Testing
        AG->>TB: Navigate app
        TB-->>AG: Responses
        AG->>AG: Analyze patterns
    and Human Monitoring
        P->>C: Watch traffic
        P->>C: Inspect requests
        P->>C: Manual testing ideas
    end

    Note over P,TA: ✏️ PHASE 3: INTERCEPT & MODIFY
    P->>C: Find suspicious request
    P->>C: Modify parameters
    P->>C: Forward modified request
    C->>TA: Modified request
    TA-->>C: Response
    C-->>P: Check response
    P->>AG: Share finding via notes
    AG->>AG: Investigate pattern

    Note over P,TA: 🎯 PHASE 4: GUIDED FOCUS
    P->>T: "Focus on /admin/* IDOR"
    T->>AG: Update instructions
    AG->>AG: Targeted testing
    AG->>C: Capture requests
    C-->>P: Show admin traffic

    Note over P,TA: ⚡ PHASE 5: RAPID EXPLOITATION
    P->>C: Discover auth bypass
    P->>AG: "Try this payload"
    AG->>AG: Validate & expand
    AG->>AG: Build PoC
    AG->>T: Report finding

    Note over P,TA: ✅ PHASE 6: VALIDATION
    P->>AG: "Confirm this is exploitable"
    AG->>AG: Develop exploit
    AG->>TA: Test exploit
    TA-->>AG: Success
    AG->>T: Verified finding with PoC
    T-->>P: Display validated vulnerability

    Note over P,TA: 📋 PHASE 7: DOCUMENTATION
    AG->>T: Create vulnerability report
    T->>P: Show report
    P->>P: Review & enhance
    P->>T: Add remediation notes
    T->>T: Finalize report
```

---

## Interactive Control Points

```mermaid
flowchart LR
    subgraph INTERACTIVE["⚡ INTERACTIVE CONTROL POINTS"]
        
        ICP1["🎯 PHASE 1: Pre-Scan
        ══════════════════════
        • Define scope with --instruction
        • Set exclusions
        • Provide credentials
        • Choose scan mode"]
        
        ICP2["🔄 PHASE 2: Mid-Scan
        ══════════════════════
        • Caido proxy inspection
        • Intercept & modify
        • Real-time guidance
        • Pause/resume testing"]
        
        ICP3["📝 PHASE 3: Findings
        ══════════════════════
        • Validate exploits
        • Approve/reject findings
        • Request PoC details
        • Prioritize focus"]
        
        ICP4["🔧 PHASE 4: Exploitation
        ══════════════════════
        • Guide exploitation
        • Custom payload testing
        • Manual override
        • Deep-dive investigation"]
        
    end

    ICP1 <-->|"←→"| ICP2
    ICP2 <-->|"←→"| ICP3
    ICP3 <-->|"←→"| ICP4
    ICP4 <-->|"←→"| ICP1

    style ICP1 fill:#e1bee7,stroke:#7b1fa2
    style ICP2 fill:#fff9c4,stroke:#f9a825
    style ICP3 fill:#c8e6c9,stroke:#388e3c
    style ICP4 fill:#ffccbc,stroke:#d84315
```

---

## Caido Proxy Integration

```mermaid
flowchart TB
    subgraph BROWSER["🌐 BROWSER (Playwright)"]
        B1[Navigate Pages]
        B2[Fill Forms]
        B3[Click Elements]
        B4[Execute JS]
    end

    subgraph CAIDO["🔄 CAIDO PROXY SERVER"]
        C1[Capture All Traffic]
        C2[Request History]
        C3[Sitemap Builder]
        C4[Scope Filters]
        C5[HTTPQL Engine]
    end

    subgraph PENTESTER["👤 PENTESTER ACTIONS"]
        P1[🖱️ Manual Intercept]
        P2[✏️ Modify Request]
        P3[▶️ Forward/Repeat]
        P4[🔍 Filter Traffic]
        P5[📊 Analyze Patterns]
        P6[🎯 Target Discovery]
    end

    subgraph TARGET["🎯 TARGET"]
        T1[Web Application]
        T2[API Endpoints]
        T3[Authentication]
    end

    %% Data flow
    B1 -->|"All requests"| C1
    B2 -->|"All requests"| C1
    B3 -->|"All requests"| C1
    B4 -->|"All requests"| C1

    C1 -->|"Traffic"| C2
    C2 -->|"Filtered"| C5
    C1 -->|"Discovered"| C3
    C3 -->|"Endpoints"| C4

    P1 -->|"Inspect"| C2
    P2 -->|"Modified"| C1
    P3 -->|"Repeat"| C1
    P4 -->|"Query"| C5
    P5 -->|"Analyze"| C5
    P6 -->|"Explore"| C3

    C1 -->|"Modified Requests"| T1
    C1 -->|"Modified Requests"| T2
    C1 -->|"Modified Requests"| T3

    T1 -->|"Responses"| C1
    T2 -->|"Responses"| C1
    T3 -->|"Responses"| C1

    classDef browser fill:#bbdefb,stroke:#1976d2
    classDef caido fill:#fff9c4,stroke:#f9a825
    classDef pentester fill:#e1bee7,stroke:#7b1fa2
    classDef target fill:#ffccbc,stroke:#d84315

    class BROWSER browser
    class CAIDO caido
    class PENTESTER pentester
    class TARGET target
```

---

## Real-Time Collaboration Session

```mermaid
sequenceDiagram
    participant U as User/Pentester
    participant ST as Strix Terminal
    participant CA as Caido Proxy
    participant BR as Browser Agent
    participant TA as Target App

    Note over U,TA: SCENARIO: Discovering IDOR Vulnerability

    U->>ST: Start scan with instructions
    ST->>BR: Launch browser
    BR->>TA: Navigate to /dashboard
    TA-->>BR: Dashboard page
    BR->>ST: Report: Found user ID param

    Note over U: 💡 HUMAN INSIGHT
    U->>CA: Open Caido Desktop
    U->>CA: Review captured traffic
    U->>CA: Notice /api/users/123 pattern
    U->>CA: Try changing to /api/users/1
    CA->>TA: Modified request
    TA-->>CA: Different user data!

    Note over U: 🤖 AI COLLABORATION
    U->>ST: "Try IDOR on all user endpoints"
    ST->>BR: Update task: IDOR testing
    BR->>CA: Capture all user requests
    BR->>ST: Found 5 potential IDORs

    Note over U: ✅ VALIDATION
    U->>CA: Inspect first finding
    U->>CA: Modify and replay request
    CA->>TA: Exploit test
    TA-->>CA: Unauthorized access!
    CA-->>U: Confirmed vulnerability

    U->>ST: "Build full PoC"
    ST->>ST: Generate exploit script
    ST->>ST: Document finding
    ST->>U: IDOR validated with PoC

    Note over U: 📝 ENRICH
    U->>ST: "Also check /api/orders/* pattern"
    ST->>BR: Additional testing
    BR->>ST: Found more IDORs!
    ST->>U: Expanded findings report
```

---

## HITL Decision Tree

```mermaid
flowchart TD
    START([🔍 New Finding Detected]) --> REVIEW{"👤 Review Finding?"}
    
    REVIEW -->|Yes - Low Priority| LOW[📝 Log Finding]
    LOW --> CONTINUE[➡️ Continue Testing]
    
    REVIEW -->|Yes - High Priority| HIGH[🎯 Investigate Deep]
    HIGH --> EXPLOIT{"⚡ Exploit Possible?"}
    
    EXPLOIT -->|Yes - Automated| AUTO[🤖 Let Strix Exploit]
    AUTO --> VALIDATE{✅ Validate?"}
    VALIDATE -->|Yes| POCC[📸 Generate Full PoC]
    VALIDATE -->|No - Need Manual| MANUAL[👤 Manual Testing]
    MANUAL --> POCC
    
    EXPLOIT -->|Requires Creativity| MANUAL2[👤 Custom Exploit]
    MANUAL2 --> POCC
    
    REVIEW -->|Not Valid| FALSEPOS[❌ Mark False Positive]
    FALSEPOS --> CONTINUE
    
    POCC --> REPORT[📄 Document Finding]
    REPORT --> SEVERITY{⚠️ Severity?"}
    
    SEVERITY -->|Critical| ESCALATE[🚨 Escalate Immediately]
    ESCALATE --> DONE
    
    SEVERITY -->|High| HIGHRISK[⚠️ Add to Report]
    HIGHRISK --> DONE
    
    SEVERITY -->|Medium/Low| LOWREPORT[📋 Standard Report]
    LOWREPORT --> DONE
    
    CONTINUE -->|Loop| START
    DONE([✅ Next Finding])
    
    classDef review fill:#e1bee7,stroke:#7b1fa2
    classDef decision fill:#fff9c4,stroke:#f9a825
    classDef action fill:#c8e6c9,stroke:#388e3c
    classDef alert fill:#ffcdd2,stroke:#d84315

    class START,REVIEW,EXPLOIT,VALIDATE,SEVERITY decision
    class LOW,HIGH,AUTO,MANUAL,MANUAL2,POCC,REPORT,HIGHRISK,LOWREPORT action
    class ESCALATE,FALSEPOS alert
    class DONE review
```

---

## Caido Workflow for Manual Testing

```mermaid
flowchart TB
    subgraph DISCOVER["🔍 DISCOVERY PHASE"]
        D1[Launch Strix] --> D2[Caido URL appears]
        D2 --> D3[Open Caido Desktop]
        D3 --> D4[Browse target app]
        D4 --> D5[Traffic captured automatically]
        D5 --> D6[Review sitemap]
    end

    subgraph ANALYZE["📊 ANALYSIS PHASE"]
        D6 --> A1[Filter by scope]
        A1 --> A2[Look for interesting endpoints]
        A2 --> A3[/api/*, /admin/*, /user/*]
        A3 --> A4[Check request parameters]
        A4 --> A5[Look for IDs, tokens, data]
    end

    subgraph TEST["⚡ TESTING PHASE"]
        A5 --> T1[Select request]
        T1 --> T2[Modify parameters]
        T2 --> T3[Add payloads]
        T3 --> T4[Forward request]
        T4 --> T5[Analyze response]
    end

    subgraph VALIDATE["✅ VALIDATION PHASE"]
        T5 --> V1{"Vulnerable?"}
        V1 -->|Yes| V2[Repeat with variations]
        V2 --> V3[Confirm exploitability]
        V3 --> V4[Share with Strix agent]
        V4 --> V5[Request PoC generation]
        
        V1 -->|No| V6[Log & continue]
        V6 --> BACK[🔙 Back to analysis]
    end

    subgraph ENRICH["📝 ENRICHMENT PHASE"]
        V5 --> E1[Strix validates finding]
        E1 --> E2[Generate documentation]
        E2 --> E3[Create exploit script]
        E3 --> E4[Add to report]
    end

    BACK -.-> ANALYZE

    classDef discover fill:#e3f2fd,stroke:#1976d2
    classDef analyze fill:#fff9c4,stroke:#f9a825
    classDef test fill:#c8e6c9,stroke:#388e3c
    classDef validate fill:#e1bee7,stroke:#7b1fa2
    classDef enrich fill:#ffccbc,stroke:#d84315

    class DISCOVER discover
    class ANALYZE analyze
    class TEST test
    class VALIDATE validate
    class ENRICH enrich
```

---

## Feedback Loop System

```mermaid
flowchart LR
    subgraph AGENT["🤖 STRIX AGENT"]
        A1[🔍 Analyze Target]
        A2[💡 Generate Hypotheses]
        A3[⚡ Execute Tests]
        A4[📊 Collect Results]
        A5[🧠 Learn & Adapt]
    end

    subgraph HUMAN["👤 PENTESTER"]
        H1[👁️ Observe Behavior]
        H2[💭 Apply Intuition]
        H3[🎯 Provide Guidance]
        H4[✅ Validate Results]
        H5[🔧 Correct Errors]
    end

    subgraph SHARED["🔗 SHARED CONTEXT"]
        S1[📝 Notes System]
        S2[🔄 Traffic History]
        S3[📋 Findings Board]
        S4[🗺️ Attack Surface Map]
    end

    %% Agent to Human
    A1 -->|"Progress Update"| H1
    A3 -->|"Requests Logged"| S2
    A4 -->|"New Finding"| S3
    A5 -->|"Updated Context"| S4

    %% Human to Agent
    H3 -->|"Instructions"| A2
    H4 -->|"Validation"| A3
    H5 -->|"Correction"| A5
    H2 -->|"Insight"| A1

    %% Shared context
    S1 <-->|"Read/Write"| A1
    S2 <-->|"Query"| A1
    S3 <-->|"Update"| A1
    S4 <-->|"Consult"| A1

    S1 <-->|"Read/Write"| H1
    S2 <-->|"Inspect"| H1
    S3 <-->|"Review"| H1
    S4 <-->|"Explore"| H1

    classDef agent fill:#bbdefb,stroke:#1976d2
    classDef human fill:#e1bee7,stroke:#7b1fa2
    classDef shared fill:#c8e6c9,stroke:#388e3c

    class AGENT agent
    class HUMAN human
    class SHARED shared
```

---

## Common HITL Scenarios

```mermaid
flowchart TD
    START([🎯 Choose Scenario]) --> SCENARIOS
    
    SCENARIOS -->|"1. I found something!"| SCEN1
    SCENARIOS -->|"2. Where do I look?"| SCEN2
    SCENARIOS -->|"3. Strix is stuck"| SCEN3
    SCENARIOS -->|"4. Validate this finding"| SCEN4
    SCENARIOS -->|"5. Customize the scan"| SCEN5

    subgraph SCEN1["🔍 Scenario 1: Manual Discovery"]
        S1A[Use Caido to intercept] --> S1B[Modify request]
        S1B --> S1C[Forward to target]
        S1C --> S1D[Confirmed exploitable?]
        S1D -->|Yes| S1E[Share with Strix via notes]
        S1D -->|No| S1F[Log observation]
        S1E --> S1G[Strix builds PoC & documents]
    end

    subgraph SCEN2["🎯 Scenario 2: Guidance Needed"]
        S2A[Open Caido sitemap] --> S2B[Review discovered endpoints]
        S2B --> S2C[Identify interesting paths]
        S2C --> S2D[/admin/, /api/users/, /upload/]
        S2D --> S2E[Send guidance to Strix]
        S2E --> S2F["Focus on IDOR in /api/users/*"]
    end

    subgraph SCEN3["🔄 Scenario 3: Agent Stuck"]
        S3A[Check current agent status] --> S3B[Identify blockage point]
        S3B --> S3C[Provide workaround]
        S3C --> S3D["Try alternative payload X"]
        S3D --> S3E[Resume agent]
        S3E --> S3F[Monitor progress]
    end

    subgraph SCEN4["✅ Scenario 4: Finding Validation"]
        S4A[Review finding in TUI] --> S4B[Open Caido traffic]
        S4B --> S4C[Replay the request]
        S4C --> S4D[Confirm vulnerability]
        S4D --> S4E["Impact: Can read any user's data"]
        S4E --> S4F[Add remediation notes]
        S4F --> S4G[Approve for report]
    end

    subgraph SCEN5["⚙️ Scenario 5: Customize Scan"]
        S5A[Create instruction file] --> S5B[Specify focus areas]
        S5B --> S5C["XSS in comment fields"]
        S5C --> S5D[Set exclusions]
        S5D --> S5E["Skip /admin area"]
        S5E --> S5F[Provide test credentials]
        S5F --> S5G[Run targeted scan]
    end

    SCEN1 --> END([📋 Continue Testing])
    SCEN2 --> END
    SCEN3 --> END
    SCEN4 --> END
    SCEN5 --> END

    style SCEN1 fill:#c8e6c9,stroke:#388e3c
    style SCEN2 fill:#bbdefb,stroke:#1976d2
    style SCEN3 fill:#fff9c4,stroke:#f9a825
    style SCEN4 fill:#e1bee7,stroke:#7b1fa2
    style SCEN5 fill:#ffccbc,stroke:#d84315
```

---

## Interactive Notes System

```mermaid
flowchart TB
    subgraph NOTES["📝 SHARED NOTES SYSTEM"]
        N1[create_note<br/>category: finding]
        N2[create_note<br/>category: wiki]
        N3[create_note<br/>category: todo]
        N4[create_note<br/>category: idea]
        N5[get_note<br/>note_id]
        N6[update_note<br/>note_id]
        N7[list_notes<br/>category]
        N8[delete_note<br/>note_id]
    end

    subgraph USAGE["💡 USE CASES"]
        U1["Pentester: 'I found XSS here'"
        --> create_note with evidence]
        
        U2["Pentester: 'Investigate this endpoint'
        --> create_note as todo"]
        
        U3["Agent: 'Confirmed vulnerability'
        --> update_note with PoC"]
        
        U4["Both: 'What's the current status?'
        --> list_notes"]
    end

    N1 -.->|"Evidence & Findings"| U1
    N2 -.->|"Architecture & Context"| U2
    N3 -.->|"Task Tracking"| U3
    N4 -.->|"Pentester Ideas"| U4

    U1 --> N6
    U2 --> N6
    U3 --> N6
    U4 --> N7

    classDef notes fill:#fff9c4,stroke:#f9a825
    classDef usage fill:#e1bee7,stroke:#7b1fa2

    class NOTES notes
    class USAGE usage
```

---

## Real-World Testing Scenario

```mermaid
sequenceDiagram
    participant P as Pentester
    participant S as Strix
    participant C as Caido
    participant A as Agent
    participant T as Target

    Note over P,T: SCENARIO: E-Commerce IDOR Discovery

    P->>S: strix --target https://shop.com
    S->>A: Start testing
    A->>T: Browse products
    T-->>A: Product pages

    Note over P: 🔍 PENTESTER FINDS SOMETHING
    P->>C: Open proxy
    P->>C: Browse to /account/orders
    C->>T: GET /api/orders?user_id=123
    T-->>C: Order data for user 123

    P->>C: Modify user_id to 124
    C->>T: GET /api/orders?user_id=124
    T-->>C: Order data for user 124!

    Note over P: 🎯 PENTESTER GUIDES TESTING
    P->>S: "Found IDOR! Check all /api/* endpoints"
    S->>A: Update focus: IDOR testing
    A->>C: Capture all API requests
    A->>A: Test systematic IDOR patterns

    Note over P: 🤖 AGENT EXPANDS FINDINGS
    A->>T: Test /api/users/{id}
    T-->>A: User 1 data
    A->>T: Test /api/profile/{id}
    T-->>A: Profile data
    A->>T: Test /api/addresses/{id}
    T-->>A: Address data

    Note over P: ✅ VALIDATE WITH PENTESTER
    A->>S: "Found 4 confirmed IDORs"
    S-->>P: Display findings
    P->>C: Verify finding #1
    P->>C: Verify finding #2
    P->>C: Verify finding #3
    P->>C: Verify finding #4

    Note over P: 📝 DOCUMENT
    P->>S: "Generate full report"
    S->>S: Create PoC scripts
    S->>S: Document all findings
    S->>S: Calculate CVSS scores
    S-->>P: Final vulnerability report
```

---

## HITL Best Practices Checklist

```mermaid
flowchart TB
    subgraph PREP["✅ PRE-SCAN CHECKLIST"]
        PC1[☐ Define scope clearly]
        PC2[☐ Prepare instruction file]
        PC3[☐ Set up Caido Desktop access]
        PC4[☐ Have test accounts ready]
        PC5[☐ Choose appropriate scan mode]
    end

    subgraph MONITOR["✅ MONITORING CHECKLIST"]
        MC1[☐ Watch TUI for discoveries]
        MC2[☐ Review Caido traffic regularly]
        MC3[☐ Check sitemap for coverage]
        MC4[☐ Note interesting patterns]
        MC5[☐ Track agent progress]
    end

    subgraph INTERACT["✅ INTERACTION CHECKLIST"]
        IC1[☐ Provide guidance on discoveries]
        IC2[☐ Correct agent when needed]
        IC3[☐ Request specific tests]
        IC4[☐ Validate high-priority findings]
        IC5[☐ Use notes to share context]
    end

    subgraph VALIDATE["✅ VALIDATION CHECKLIST"]
        VC1[☐ Manually verify exploits]
        VC2[☐ Check false positives]
        VC3[☐ Assess actual impact]
        VC4[☐ Confirm PoC works]
        VC5[☐ Document remediation steps]
    end

    subgraph REPORT["✅ REPORTING CHECKLIST"]
        RC1[☐ Review all findings]
        RC2[☐ Add human insights]
        RC3[☐ Enhance PoC descriptions]
        RC4[☐ Prioritize by risk]
        RC5[☐ Export final reports]
    end

    PREP --> MONITOR --> INTERACT --> VALIDATE --> REPORT

    style PREP fill:#e3f2fd,stroke:#1976d2
    style MONITOR fill:#fff9c4,stroke:#f9a825
    style INTERACT fill:#e1bee7,stroke:#7b1fa2
    style VALIDATE fill:#c8e6c9,stroke:#388e3c
    style REPORT fill:#ffccbc,stroke:#d84315
```

---

## Summary: When to Intervene

```mermaid
flowchart TD
    START([🤔 Should I intervene?]) --> Q1{"Agent found something?"}
    
    Q1 -->|No, nothing happening| A1[🟡 WAIT & OBSERVE]
    A1 -->|"Still nothing after 5 min"| A2["🎯 Provide guidance<br/>'Try /admin/* testing'"]
    A2 --> BACK
    
    Q1 -->|"Yes - Low severity"| B1["🟢 Let agent handle"]
    B1 --> B2[Monitor progress]
    
    Q1 -->|"Yes - Critical finding"| C1["🔴 IMMEDIATE REVIEW"]
    C1 --> C2[Check in Caido]
    C2 --> C3{Valid?}
    C3 -->|Yes| C4[Validate & escalate]
    C3 -->|No| C5[Mark false positive]
    
    Q1 -->|"Yes - Complex exploit"| D1["🟠 COLLABORATE"]
    D1 --> D2[Provide manual testing]
    D2 --> D3[Share results with agent]
    D3 --> D4[Agent builds full PoC]
    
    Q1 -->|"Need specific test"| E1["🔵 SEND INSTRUCTION"]
    E1 --> E2["'Focus on SQL injection'"]
    E2 --> E3[Agent executes focused test]
    E3 --> BACK

    BACK([👁️ Continue monitoring])
    
    classDef wait fill:#fff9c4,stroke:#f9a825
    classDef auto fill:#c8e6c9,stroke:#388e3c
    classDef urgent fill:#ffcdd2,stroke:#d84315
    classDef collab fill:#bbdefb,stroke:#1976d2
    classDef guide fill:#e1bee7,stroke:#7b1fa2

    class A1,A2 wait
    class B1,B2 auto
    class C1,C2,C3,C4,C5 urgent
    class D1,D2,D3,D4 collab
    class E1,E2,E3 guide
```

---

These diagrams illustrate how **you remain in control** while Strix handles the heavy lifting. The HITL approach combines:
- **Autonomous scanning** for speed and coverage
- **Human intuition** for complex vulnerabilities  
- **Caido proxy** for manual inspection and manipulation
- **Real-time collaboration** via notes and instructions
- **Validation** before final reporting