# Vatican Vault
## Intelligence Hidden in Plain Sight — Unlocking Windows Activity Data Across Every Industry

---

> Every Windows PC is a witness. Vatican Vault is the interpreter.

---

## The Opportunity

There are over **1.4 billion active Windows devices** in the world. Every one of them running Windows 10 or 11 has been quietly recording a detailed log of user behavior — applications launched, files accessed, websites visited, documents opened — stored in a structured SQLite database called `ActivitiesCache.db`. Devices running Microsoft Recall capture something even more remarkable: **visual screenshots of everything displayed on screen**, indexed with AI-powered OCR, every few seconds.

This data is not hidden. It requires no special hardware, no network tap, no endpoint agent. It is sitting on the device, structured, queryable, and waiting to be understood.

The problem is not the data. The problem is that until Vatican Vault, **no comprehensive tool existed to read it intelligently**.

Vatican Vault is the platform that changes that.

---

## What Vatican Vault Does

Vatican Vault is an AI-powered forensic analysis and behavioral intelligence platform that ingests Windows Timeline databases (`ActivitiesCache.db`), Windows Recall snapshots (`ukg.db`), and network traffic captures (PCAP/PCAPNG), and transforms them into actionable intelligence through:

- **Timeline reconstruction** — Precise, minute-by-minute activity replay
- **Entity extraction** — Automatic identification of people, organizations, credentials, IP addresses, financial data, and 20+ other entity types from all activity records
- **Behavioral analytics** — Machine learning models that detect anomalies, cluster behavior patterns, and forecast risk
- **Sensitive data detection** — Automatic flagging of credentials, PII, financial data, and regulated content captured in activity records or screenshots
- **Network correlation** — Cross-reference on-device activity against captured network traffic
- **Professional reporting** — Executive summaries, technical analyses, compliance-ready exports, and evidentiary-quality HTML/PDF reports

Vatican Vault runs locally on any machine. No cloud dependency. No data leaves the device unless the operator explicitly exports it. No subscription required for core functionality.

---

## Industry Applications

### Enterprise IT & Security Operations

**The Challenge**: Security teams manage thousands of endpoints with limited visibility into user-level behavior. Traditional SIEM tools capture network events and log aggregates — but miss the granular picture of what users actually did on their machines. When an incident occurs, reconstruction is expensive, slow, and often incomplete.

**Vatican Vault's Role**:

- **Instant incident reconstruction**: Given any endpoint, Vatican Vault generates a minute-by-minute timeline of user activity in seconds, without deploying an agent or touching the live system
- **Insider threat detection**: Behavioral anomaly models identify unusual access patterns, off-hours activity, bulk file access, and data staging consistent with data exfiltration
- **Data loss investigation**: Track exactly which files were accessed, when, by which application, and whether they were subsequently deleted
- **Credential exposure**: Recall screenshot analysis automatically flags sessions where API keys, passwords, or authentication tokens were visible on screen — a critical audit capability for developer and admin workstations
- **Zero-footprint analysis**: Forensic analysis of a database copy leaves no trace on the live endpoint

**Business Value**: Reduce mean-time-to-investigate (MTTI) from days to hours. Enable security teams of five to analyze incidents that previously required external DFIR consultants.

---

### Digital Forensics & Incident Response (DFIR)

**The Challenge**: DFIR practitioners routinely spend 60–80% of their investigation time on data acquisition, parsing, and timeline construction — before any actual analysis begins. Tool fragmentation means analysts must master dozens of specialized parsers, correlate output from disparate formats, and manually build timelines that should be automatic.

**Vatican Vault's Role**:

- **Unified artifact parser**: One tool handles Timeline, Recall, and PCAP — no more context-switching between tools
- **Automated timeline generation**: Click-to-HTML forensic timelines with source attribution, confidence indicators, and direct links back to raw database records
- **Entity relationship mapping**: Automatic knowledge graph construction showing which people, organizations, and assets appear across the activity record
- **Cross-artifact correlation**: Correlate on-device application activity with network traffic — show that the file access at 14:32 was followed by a DNS lookup to a cloud storage provider at 14:34
- **Evidentiary exports**: Reports formatted for legal proceedings, with chain-of-custody metadata and raw data appendices
- **STIX 2.1 and MISP integration**: Export entity and IOC data directly to threat intelligence platforms

**Business Value**: Cut investigation timelines by 50–70%. Enable junior analysts to produce work previously requiring senior specialists. Handle higher caseloads without proportional headcount increases.

---

### Law Enforcement & Criminal Investigations

**The Challenge**: Law enforcement agencies executing search warrants on computers face enormous challenges. The volume of data on modern PCs is overwhelming. Investigators need to quickly answer specific questions — "was this person at this computer at this time?", "did they access this file?", "what were they doing in the hours before the incident?" — without spending weeks on forensic analysis.

**Vatican Vault's Role**:

- **Rapid activity reconstruction**: Generate a complete, human-readable timeline of everything that occurred on a seized device in minutes, not days
- **Alibi verification and refutation**: Precise timestamps for every user action enable investigators to confirm or challenge claims about a person's whereabouts and activities
- **Evidence of intent**: Document access to specific files (instructions, communications, target research) that establish intent and premeditation
- **Corroborating witness**: Recall screenshot analysis provides visual evidence of what the user saw — confirming that they viewed specific content, opened specific messages, or visited specific websites
- **Keyword and entity search**: Search the complete activity record for names, addresses, phone numbers, financial account numbers, or any other entity of interest — without reviewing files manually
- **Child exploitation investigations**: Surface evidence of access to specific content types based on file paths, application names, and OCR-extracted text from Recall

**Business Value**: Faster case development. Richer evidentiary record. Reduced reliance on expensive private DFIR contractors for preliminary analysis.

---

### Military & Intelligence

**The Challenge**: In classified and sensitive environments, insider threats are among the most dangerous risks. A trusted person with legitimate access who decides to steal, leak, or sabotage has built-in cover. Traditional DLP (Data Loss Prevention) tools are evadable. Activity monitoring agents can be disabled or detected. Air-gapped environments may prohibit network-based monitoring entirely.

**Vatican Vault's Role**:

- **Post-incident forensics without live monitoring**: When a suspected leak is discovered, Vatican Vault analyzes the suspect workstation's activity database to reconstruct exactly what was accessed, copied, and transmitted — without any prior monitoring infrastructure
- **Anomaly detection at classification boundaries**: Identify users who accessed classified materials outside their normal operational pattern — off-hours, from unusual applications, in unusual volumes
- **Recall analysis for need-to-know enforcement**: Recall screenshot analysis can identify what classified information was visible on screen, enabling need-to-know audits even for air-gapped systems
- **Exfiltration reconstruction**: Correlate file access events with removable media insertion events, network activity windows, and application launches to build a complete exfiltration timeline
- **Counter-intelligence support**: Entity extraction across activity records can surface previously unknown relationships — a contractor who searched for a competitor's name, or a staff member who researched specific targets

**Business Value**: Close the visibility gap on insider threats that network monitoring cannot see. Enable rapid damage assessment following a suspected compromise.

---

### Human Resources & Employment Law

**The Challenge**: Employment disputes, misconduct investigations, and termination decisions increasingly turn on digital evidence — "did the employee take company files?", "was the employee working during claimed work hours?", "did they share confidential information with a competitor?" HR and legal teams lack tools to answer these questions quickly and defensibly.

**Vatican Vault's Role**:

- **Time and attendance verification**: Timeline data shows exactly when a user was actively working on their company laptop — essential for remote work compliance and disputed timecard investigations
- **Data theft investigations**: Document the precise moment an employee accessed confidential files before resignation, and correlate with external transfers
- **Non-compete and NDA enforcement**: Establish timeline of access to trade secrets and customer data in support of civil litigation
- **Misconduct documentation**: Reconstruct what websites, applications, and content a user accessed on company equipment during work hours
- **Due process support**: Comprehensive timeline evidence supports defensible termination decisions and reduces litigation risk

**Business Value**: Replace expensive e-discovery processes for simple matters. Give HR teams access to the same quality of evidence previously available only through expensive external forensic consultants.

---

### Healthcare & Compliance

**The Challenge**: HIPAA and other healthcare regulations require organizations to audit access to patient records and investigate potential breaches. Traditional audit logs are incomplete — they show which records were queried in the EHR system but miss everything that happened outside the application. Was patient data photographed? Printed? Exported to a personal device?

**Vatican Vault's Role**:

- **HIPAA breach investigation**: Timeline analysis reconstructs a nurse's or administrator's complete session, showing access to patient records followed by activity in personal email, USB file transfers, or cloud uploads
- **PHI exfiltration detection**: Sensitive data scanner automatically flags activity records containing Social Security numbers, medical record numbers, patient names, and other PHI identifiers
- **Recall screenshot audit**: For organizations deploying Recall (or investigating on personal Copilot+ PCs), screenshot analysis can confirm whether patient data was visible during screen-sharing sessions, personal browsing, or unauthorized application use
- **Compliance reporting**: Generate audit-ready reports showing who accessed what data, when, from which applications, with entity-level granularity
- **Incident response timeline**: Produce the breach timeline reports required by HIPAA notification rules within hours of incident discovery

**Business Value**: Meet HIPAA investigation and notification requirements faster. Reduce breach investigation costs. Demonstrate due diligence to regulators.

---

### Financial Services & Regulatory Compliance

**The Challenge**: Financial institutions face strict regulatory requirements around data access, employee conduct, and market integrity. Compliance teams must investigate potential violations — insider trading, customer data misuse, rogue trading — with evidence that meets regulatory and legal standards.

**Vatican Vault's Role**:

- **Insider trading investigation**: Correlate an employee's access to material non-public information (MNPI) with subsequent trading activity — Timeline records show exactly when they opened the deal file, for how long, and what else they did immediately after
- **Customer data protection**: Identify and document unauthorized access to customer account data, correlating database application activity with external file transfers
- **Rogue trading reconstruction**: Rebuild the exact sequence of actions that preceded an unauthorized trade, including research, communications access, and system interactions
- **Regulatory examination support**: Produce comprehensive timelines and entity extraction reports for SEC, FINRA, or FCA examinations — formatted to meet regulatory evidentiary standards
- **SOC 2 and PCI-DSS audits**: Document access patterns to systems in scope, identify anomalous access, and generate compliance reports

**Business Value**: Reduce cost and time of regulatory investigations. Demonstrate robust monitoring and investigation capabilities to examiners. Support defensible disciplinary actions.

---

### Education & Academic Research

**The Challenge**: Academic institutions face increasing concerns about academic integrity, research data security, and export control compliance. Instructors need to verify that exams were completed independently. Research security officers need to monitor access to controlled technology or ITAR-restricted data. IT security teams need to investigate incidents on research computing systems.

**Vatican Vault's Role**:

- **Academic integrity investigations**: Reconstruct a student's or researcher's complete computer session during an exam period — show exactly which applications were open, which websites were visited, and when
- **Research security compliance**: Identify researcher access to controlled technology data, flag transfers to personal cloud storage or external devices
- **Export control audits**: Surface evidence of access to ITAR or EAR-controlled technical data and reconstruct the full context of that access
- **Grant fraud investigation**: Document what research tasks were actually performed and when, compared to claimed work logs

---

## Competitive Landscape

| Capability | Vatican Vault | Traditional DFIR Tools | SIEM/EDR | Recall-Specific Tools |
|-----------|--------------|----------------------|---------|----------------------|
| Windows Timeline parsing | Native, comprehensive | Partial, fragmented | None | None |
| Windows Recall analysis | Native, AI-powered | Limited or none | None | Basic extraction only |
| Behavioral ML analytics | Built-in (Isolation Forest, HDBSCAN) | Rarely | Yes (high cost) | None |
| Entity extraction (NER) | 20+ entity types, hybrid NLP | Manual or limited | None | None |
| Knowledge graphs | Automated generation | Manual | None | None |
| PCAP correlation | Integrated | Separate tool | Separate tool | None |
| Local deployment | Yes (no cloud required) | Yes | Cloud-dependent | Yes |
| REST API | 68 endpoints | Rarely | Yes | None |
| Report formats | HTML, PDF, JSON, STIX, MISP, Excel | Varies | Varies | None |
| Price point | Open platform | $10K–$100K+ licensing | $50K–$500K/yr | Free scripts |

---

## Technical Architecture at a Glance

Vatican Vault is built for reliability, extensibility, and deployment flexibility:

**Core Stack**
- FastAPI (Python) backend with 68 REST endpoints
- SQLAlchemy ORM with async support
- spaCy + sentence-transformers for NLP
- scikit-learn (Isolation Forest, DBSCAN/HDBSCAN) for ML
- PyTorch + torchvision for vision features
- Rich terminal UI + Typer CLI framework

**Deployment Options**
- Single Python script (`python vatican.py`) — zero configuration
- Interactive menu CLI (`python vatican_vault.py`)
- REST API server (`uvicorn app.main:app`)
- Docker Compose (full stack with Redis, Grafana, Prometheus)
- Cloud storage backends (AWS S3, Azure Blob, Google Cloud Storage)

**Security & Privacy**
- All analysis runs locally by default
- No telemetry or data collection
- Optional AI provider integration (Groq, OpenAI, Anthropic) — user-controlled
- JWT authentication and API key management for the REST API
- Data redaction capability to anonymize before sharing reports

**Extensibility**
- Plugin-ready AI provider system (add any LLM endpoint)
- Cloud storage adapter pattern (add any provider)
- Configurable entity extraction patterns (add custom regex/NLP rules)
- Report template system (customize output for any organization)

---

## Who Uses Vatican Vault

Vatican Vault serves professionals across the security and investigative spectrum:

| Role | Primary Use Case |
|------|-----------------|
| DFIR Analyst | Incident reconstruction, timeline generation, evidence export |
| SOC Analyst (L2/L3) | Endpoint investigation, insider threat triage |
| Law Enforcement Detective | Criminal investigation, warrant execution analysis |
| Counter-Intelligence Officer | Insider threat assessment, damage assessment |
| Corporate Investigator | Employee misconduct, data theft, HR disputes |
| Compliance Officer | Regulatory audit support, breach investigation |
| Penetration Tester | Post-engagement evidence of access and impact |
| Threat Intelligence Analyst | Entity extraction, IOC generation, behavioral profiling |
| Security Researcher | Windows activity artifact analysis and publication |

---

## The Market

- **Global DFIR market**: $7.4 billion (2024), growing at 18% CAGR
- **Insider threat detection market**: $4.3 billion (2024), growing at 22% CAGR
- **Endpoint security market**: $21 billion (2024)
- **eDiscovery market**: $16 billion (2024)
- **Windows installed base**: 1.4 billion active devices — every one a potential data source

Vatican Vault sits at the intersection of these markets with a unique value proposition: it turns infrastructure that already exists — Windows Timeline and Recall databases — into a forensic intelligence platform that requires no new agents, no new hardware, and no new data collection.

The data is already there. Vatican Vault is the key.

---

## Summary

Vatican Vault is not a point solution. It is a platform.

It provides security teams with the insider threat visibility they've never had. It gives forensic analysts a unified, intelligent tool that replaces a dozen fragmented scripts. It enables law enforcement to reconstruct digital behavior in hours instead of weeks. It helps compliance teams meet regulatory requirements with evidence they couldn't previously access.

The technology foundation — Windows Timeline and Recall — exists on over a billion devices today and is expanding. As Recall adoption grows with Copilot+ PC hardware, the value of Vatican Vault's analysis capabilities grows with it.

**Vatican Vault: Your Windows PC is keeping secrets. We make sure the right people can read them.**

---

*For demonstrations, partnership inquiries, and technical briefings, contact the Vatican Vault team.*

*For community and open-source collaboration, the platform is available on GitHub.*
