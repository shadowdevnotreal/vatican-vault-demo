# Vatican Vault — Promo Package

This folder contains everything needed to demonstrate and present Vatican Vault.

---

## 🎯 FOR INVESTORS: START HERE

**Complete VC Demo Package**: Open **[VC_DEMO_INDEX.html](VC_DEMO_INDEX.html)** for a comprehensive investor presentation with:

- 📊 **VC Materials** - Investment summaries, business model, market analysis, financial projections
- 🏢 **Industry Demo Reports** - 12 professional reports showcasing use cases (DFIR, SOC, Law Enforcement, Healthcare, etc.)
- 📰 **Articles** - Platform history, comprehensive pitch, AI/ML use cases
- 📈 **Live Demo Reports** - Pre-generated forensic analysis outputs
- 🎮 **Interactive Demos** - Scripts and data to run live demonstrations

**Quick Links:**
- **60-Second Pitch**: [VC_Materials/EXECUTIVE_SUMMARY_VC.html](VC_Materials/EXECUTIVE_SUMMARY_VC.html)
- **1-Page Summary**: [VC_Materials/VC_EXECUTIVE_SUMMARY.html](VC_Materials/VC_EXECUTIVE_SUMMARY.html)
- **Full Report (10 pages)**: [VC_Materials/VC_DEMO_REPORT_2026-02-28.html](VC_Materials/VC_DEMO_REPORT_2026-02-28.html)
- **Interactive Package**: [VC_Materials/VC_DEMO_PACKAGE.html](VC_Materials/VC_DEMO_PACKAGE.html)
- **Industry Reports**: [Industry_Demo_Reports/index.html](Industry_Demo_Reports/index.html)

---

## 📦 Contents

### VC_Materials/ ⭐ NEW
Complete investor package with executive summaries and business analysis.

| File | Description |
|------|-------------|
| `VC_DEMO_PACKAGE.html` | **START HERE** - Interactive HTML presentation with product overview, market analysis, traction metrics, and financial projections |
| `EXECUTIVE_SUMMARY_VC.html` | 60-second pitch format - The opportunity, solution, traction, ask, and why now |
| `VC_EXECUTIVE_SUMMARY.html` | 1-page investment summary with tables, metrics, competitive analysis, and financial projections |
| `VC_DEMO_REPORT_2026-02-28.html` | Comprehensive 10-page report covering technical validation, market research, competitive landscape, and detailed financials |

---

### Industry_Demo_Reports/ ⭐ NEW
Professional HTML reports showcasing Vatican Vault for specific industries.

| File | Description |
|------|-------------|
| `index.html` | **START HERE** - Browse all 16 industry-specific demo reports |
| `dfir_report.html` | Digital Forensics & Incident Response investigation report |
| `enterprise_soc_report.html` | Enterprise Security Operations Center insider threat report |
| `law_enforcement_report.html` | Criminal investigation and evidence discovery report |
| `healthcare_report.html` | HIPAA compliance and patient data tracking report |
| `financial_report.html` | Financial services fraud detection and compliance report |
| `hr_employment_report.html` | HR employment investigation and workplace monitoring |
| `mssp_report.html` | Managed Security Service Provider client report |
| `pentest_report.html` | Penetration testing and security assessment report |
| `generic_executive_report.html` | Executive-level summary report |
| `generic_technical_report.html` | Technical analysis deep-dive report |
| `generic_compliance_report.html` | Compliance and regulatory audit report |
| `irm_report.html` | Incident Response Management report |

---

### Articles/
Narrative documents for briefings, presentations, and publications.

| File | Description |
|------|-------------|
| `HISTORY.html` | The full history of Vatican Vault — from Microsoft Project Rome (2015) through Windows Timeline, Windows Recall, and the creation of this platform. A compelling read for any audience. |
| `PITCH.html` | A comprehensive industry pitch covering Vatican Vault's use cases across IT security, DFIR, law enforcement, military/intelligence, HR, healthcare, financial services, and more. Suitable for investors, executives, and technical audiences alike. |
| `ENTITY_EXTRACTION_USECASES.html` | **NEW!** Comprehensive use cases for AI-powered entity extraction — from single desktop to enterprise scale. Includes ROI analysis, deployment models, and success stories across healthcare, finance, legal, and government sectors. |

---

### Demo_Data/
Real and synthetic sample data files for running demonstrations.

| Path | Description |
|------|-------------|
| `Test System/ActivitiesCache.db` | Sample Windows Timeline SQLite database |
| `Test System/Behave_V1_Output/` | Sample chart outputs from v1 analysis |
| `Test System/WindowsTimeline_Output/` | Sample Windows Timeline export |
| `Vatican/` | Forensic reference materials, registry files, and knowledge base |
| `4SICSGeekLounge151.pcap` | Real-world PCAP file for network analysis demos (151 MB) |
| `test_sample.pcap` | Small synthetic PCAP for quick demos |

---

### Demo_Scripts/
Python scripts for running live demonstrations.

| File | Description |
|------|-------------|
| `demo.py` | Comprehensive demo showing Timeline parsing, analytics, and reporting |
| `unified_parser.py` | Demonstrates auto-detection of database types |
| `entity_extraction_demo.py` | **NEW!** Interactive demo of hybrid NLP entity extraction with real-time visualization, use cases, and scaling examples |

**Quick run:**
```bash
source ../venv/bin/activate   # activate the virtual environment
python Demo_Scripts/demo.py

# NEW: Entity Extraction Demo
python Demo_Scripts/entity_extraction_demo.py
```

---

### Demo_Tests/
Automated tests used to verify the platform's capabilities.

| File | Description |
|------|-------------|
| `test_demo.py` | End-to-end demonstration test suite |

**Quick run:**
```bash
source ../venv/bin/activate
pytest Demo_Tests/test_demo.py -v
```

---

### Sample_Outputs/
Pre-generated output reports showing what Vatican Vault produces.

Browse the `reports/` subdirectory for timestamped output folders — each contains HTML reports, JSON exports, and analysis summaries generated from the demo databases.

---

## Running a Full Demo

1. **Install** (one time):
   ```bash
   cd ..   # from the Promo/ folder, go to project root
   python setup.py
   ```

2. **Activate virtual environment**:
   ```bash
   source ../venv/bin/activate
   ```

3. **Run against sample Timeline database**:
   ```bash
   python ../vatican.py --path "Promo/Demo_Data/Test System/ActivitiesCache.db"
   ```

4. **Run interactive menu**:
   ```bash
   python ../vatican_vault.py
   ```

5. **Run the demo script**:
   ```bash
   python Promo/Demo_Scripts/demo.py
   ```

---

## For Presentations

### For Investors (VCs, Angels, Strategic Partners)
1. **Open VC_DEMO_INDEX.html** - Complete investor package homepage
2. **Start with 60-second pitch** - VC_Materials/EXECUTIVE_SUMMARY_VC.html
3. **Show industry reports** - Industry_Demo_Reports/index.html
4. **Run live demo** - Demo_Scripts/entity_extraction_demo.py
5. **Deep dive** - VC_Materials/VC_DEMO_REPORT_2026-02-28.html

### For Technical Audiences (CTOs, Security Teams)
- Use **HISTORY.html** to explain the "why" — the story of how Windows became an activity logger and why that matters
- Use **PITCH.html** to explain the "what" — how Vatican Vault turns that data into intelligence, and who benefits
- Use **Industry_Demo_Reports/** for specific use case demonstrations
- Use the **Sample_Outputs/** reports for live visual demonstrations
- Use the **Demo_Data/** files for live analysis demonstrations

### For Enterprise Buyers (CISOs, Compliance Officers)
- Start with **Industry_Demo_Reports/** matching their vertical (healthcare, financial, SOC, etc.)
- Show **ENTITY_EXTRACTION_USECASES.html** for AI/ML capabilities and ROI analysis
- Demonstrate compliance features with **Sample_Outputs/** reports
- Run live demo with their data (if available)

---

*Vatican Vault — Your Windows PC is keeping secrets. Let's uncover them.*
