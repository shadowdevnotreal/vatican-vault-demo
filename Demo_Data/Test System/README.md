# Test System - Reference Database and Tool Outputs

**Purpose:** Real Windows Timeline database and reference outputs from forensic analysis tools

---

## Quick Start

### Adding Database Files to Git

If you have the `ActivitiesCache.db-shm` and `ActivitiesCache.db-wal` files on your local system, add them to git with:

```bash
cd "Test Files/Test System"
git add -f ActivitiesCache.db-shm ActivitiesCache.db-wal
git commit -m "feat: add SQLite WAL files to Test System reference dataset"
```

The `.gitignore` has been configured to allow these specific test files while blocking production database files elsewhere.

---

## Contents

### 1. ActivitiesCache.db
**Type:** Windows Timeline Database (SQLite3)
**Size:** 4.71 MB
**Source:** Real Windows 10/11 system
**Activities:** 1,853 activity records
**Date Range:** October 16, 2022 - March 10, 2023 (146 days)
**Applications:** 75+ tracked applications

**Location (Original):**
```
C:\Users\%USERNAME%\AppData\Local\ConnectedDevicesPlatform\L.%USERNAME%\ActivitiesCache.db
```

**Tables:**
- Activity (1,853 rows) - Core activity records
- Activity_PackageId (6,296 rows) - Application mappings
- ActivityOperation (0 rows) - Sync operations
- DataEncryptionKeys (1 row) - Encryption keys
- Metadata (5 rows) - Database configuration
- AppSettings, Asset, ManualSequence (empty/minimal)

**Top Applications:**
1. VirtualBox - 416 activities (22.45%)
2. Windows Explorer - 336 activities (18.13%)
3. Steam Client - 116 activities (6.26%)
4. Notepad - 107 activities (5.77%)
5. Rockstar Social Club - 85 activities (4.59%)

**Usage:**
```python
import sqlite3
conn = sqlite3.connect("Test Files/Test System/ActivitiesCache.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM Activity")
print(f"Total activities: {cursor.fetchone()[0]}")
conn.close()
```

**Database Files (All 3 Required):**
- `ActivitiesCache.db` - Main database file (4.71 MB)
- `ActivitiesCache.db-shm` - Shared memory file (SQLite WAL mode)
- `ActivitiesCache.db-wal` - Write-Ahead Log file (transaction log)

**Important:** All three files must be kept together in this folder for testing and demo purposes. While .db-shm and .db-wal are normally temporary files created when a database is opened in WAL mode, these are preserved as part of the reference test dataset to maintain the complete database state.

**Git Configuration:** The `.gitignore` has been configured with explicit exceptions to allow these Test System database files while blocking production database files elsewhere in the codebase.

---

### 2. WindowsTimeline_Output/
**Tool:** kacos2000's WindowsTimeline Parser
**Source:** https://github.com/kacos2000/WindowsTimeline
**Purpose:** Extract and analyze Windows Timeline data

**Output Files:**
- `WindowsTimeline.csv` (910 KB) - Complete timeline export
- `ApplicationExecutionList.csv` (5.3 KB) - Application execution tracking
- `DatabaseActivityPolicies.json` (4.1 KB) - Privacy/sync policies
- `Device_info.txt` (1.1 KB) - Device information
- `File_Info.csv` (530 B) - Database file metadata

**Description:**
This folder contains the output from kacos2000's WindowsTimeline PowerShell script, which parses ActivitiesCache.db and exports forensic artifacts in CSV/JSON format. The tool is specifically designed for DFIR (Digital Forensics and Incident Response) analysis.

**Key Artifacts:**
- **Timeline Data:** Complete activity timeline with timestamps, apps, and metadata
- **Execution Evidence:** First/last execution times for applications
- **Privacy Policies:** Cloud sync settings and data retention policies
- **Device Correlation:** Links activities to specific devices

**Forensic Value:**
- Timeline reconstruction for incident response
- Application usage profiling
- Evidence of execution
- Data exfiltration detection
- User behavior analysis

**Tool Features:**
- Parses all 8 tables in ActivitiesCache.db
- Decodes JSON payloads from Activity.Payload BLOB
- Correlates Activity and Activity_PackageId tables
- Exports in analyst-friendly CSV format
- Includes device and policy information

**Usage:**
```powershell
# Original command used:
.\Get-WindowsTimeline.ps1 -Path "ActivitiesCache.db" -Output "WindowsTimeline_Output"
```

---

### 3. Behave_V1_Output/
**Tool:** TrustedSec's Behave
**Source:** TrustedSec forensic analysis toolkit
**Purpose:** Advanced timeline analysis and visualization

**Output Files:**
- `gen_report_exported_database.csv` (535 KB) - Complete database export
- `gen_report_Activity_Applications.csv` (3.5 KB) - Application summary
- `gen_report_ApplicationLaunch_StartTime.csv` (7.8 KB) - Launch times
- `gen_report_useractivity_start_and_end.csv` (1.6 KB) - Activity windows
- `gen_fig_top10_apps_bars.jpg` (288 KB) - Bar chart visualization
- `gen_fig_top10_apps_pie.jpg` (295 KB) - Pie chart visualization
- `gen_fig_useractivity_bar.jpg` (549 KB) - Activity bar chart
- `gen_fig_useractivity_heatmap.jpg` (210 KB) - Activity heatmap
- `Paths_Unique.txt` (0 B) - Unique file paths

**Description:**
Behave is TrustedSec's Python-based tool for analyzing Windows Timeline data with advanced visualization capabilities. It generates both CSV reports and graphical representations of user activity patterns.

**Key Features:**
- **Statistical Analysis:** Application usage frequency, time distribution
- **Visualizations:** Charts, graphs, heatmaps for pattern recognition
- **Timeline Export:** Complete activity data in structured CSV
- **Behavioral Profiling:** User activity patterns and anomalies

**Visualizations Included:**
1. **Top 10 Apps (Bar Chart):** Application usage ranked by activity count
2. **Top 10 Apps (Pie Chart):** Proportional distribution of app usage
3. **User Activity (Bar Chart):** Activity volume over time
4. **User Activity (Heatmap):** Temporal patterns and peak usage times

**Forensic Value:**
- Visual pattern recognition for anomaly detection
- Statistical analysis of user behavior
- Temporal correlation of activities
- Evidence presentation for reports
- Baseline establishment for UEBA

**CSV Reports:**
- **exported_database.csv:** Complete activity records with all metadata
- **Activity_Applications.csv:** Per-application statistics and metrics
- **ApplicationLaunch_StartTime.csv:** Execution timeline for all apps
- **useractivity_start_and_end.csv:** Activity session boundaries

---

## Comparison: WindowsTimeline vs Behave

| Feature | WindowsTimeline | Behave |
|---------|----------------|--------|
| **Language** | PowerShell | Python |
| **Output Format** | CSV, JSON, TXT | CSV, JPG |
| **Visualizations** | No | Yes (4 charts) |
| **Database Coverage** | All 8 tables | Activity table focused |
| **Use Case** | Raw data extraction | Analysis + visualization |
| **Speed** | Fast | Slower (generates images) |
| **Forensic Focus** | Evidence extraction | Behavioral analysis |
| **Best For** | Timeline reconstruction | Pattern recognition |

---

## Usage in Vatican Vault

### 1. Database Analysis
```python
from backend.app.database.timeline_db import TimelineDatabase

# Use the test database
db = TimelineDatabase("Test Files/Test System/ActivitiesCache.db")

# Extract activities
activities = db.get_activities(limit=100)
stats = db.get_app_statistics()
```

### 2. CSV Import for Testing
```python
import pandas as pd

# Load WindowsTimeline CSV export
timeline_df = pd.read_csv("Test Files/Test System/WindowsTimeline_Output/WindowsTimeline.csv")

# Load Behave export
behave_df = pd.read_csv("Test Files/Test System/Behave_V1_Output/gen_report_exported_database.csv")

# Compare extraction methods
print(f"WindowsTimeline rows: {len(timeline_df)}")
print(f"Behave rows: {len(behave_df)}")
```

### 3. Reference for ML Training
```python
# Use as training data for Vatican Vault ML models
# - Application classification
# - Timeline pattern recognition
# - Anomaly detection baseline
```

### 4. Validation Testing
```python
# Validate Vatican Vault extraction against known tools
# Compare our parser output with WindowsTimeline and Behave
# Ensure we extract the same artifacts
```

---

## Tool Installation

### kacos2000 WindowsTimeline
```powershell
# Clone repository
git clone https://github.com/kacos2000/WindowsTimeline

# Run parser
cd WindowsTimeline
.\Get-WindowsTimeline.ps1 -Path "C:\Path\To\ActivitiesCache.db"
```

**Requirements:**
- PowerShell 5.1+
- Windows OS
- Read access to ActivitiesCache.db

### TrustedSec Behave
```bash
# Clone repository
git clone https://github.com/trustedsec/behave

# Install dependencies
pip install -r requirements.txt

# Run analysis
python behave.py -db "ActivitiesCache.db" -o "output_folder"
```

**Requirements:**
- Python 3.7+
- pandas, matplotlib, seaborn
- SQLite3 library

---

## Forensic Analysis Workflow

### Step 1: Extract Database
```powershell
# From target system
copy "C:\Users\%USERNAME%\AppData\Local\ConnectedDevicesPlatform\L.%USERNAME%\ActivitiesCache.db" .
```

### Step 2: Parse with WindowsTimeline
```powershell
.\Get-WindowsTimeline.ps1 -Path "ActivitiesCache.db" -Output "timeline_output"
```

**Output:** Raw CSV data for timeline reconstruction

### Step 3: Analyze with Behave
```bash
python behave.py -db "ActivitiesCache.db" -o "behave_output"
```

**Output:** Statistical analysis and visualizations

### Step 4: Analyze with Vatican Vault
```bash
python vatican_vault.py
# Select option 2: Deep Forensic Analysis
# Or option 3: Timeline Analysis Only
```

**Output:** Comprehensive forensic report with:
- Timeline reconstruction
- Sensitive data exposure scanning
- Entity extraction (emails, URLs, credentials)
- Sentiment analysis for UEBA
- HTML forensic report

---

## Database Structure Reference

See `docs/KNOWLEDGE_BASE.md` for complete schema documentation including:
- All 8 table structures with column descriptions
- Forensic SQL queries for each analysis type
- Activity type classification
- Payload BLOB parsing techniques
- Clipboard data extraction
- Evidence of execution queries

---

## Best Practices

### For Testing
✅ Use ActivitiesCache.db as reference database
✅ Compare Vatican Vault output with WindowsTimeline CSV
✅ Validate parsing accuracy against both tools
✅ Use Behave visualizations to verify pattern detection

### For Training
✅ Use CSV exports for ML model training
✅ Extract labeled data from known activities
✅ Build baseline models from clean data
✅ Test anomaly detection against normal patterns

### For Forensics
✅ Cross-reference findings across all three tools
✅ Use WindowsTimeline for raw data extraction
✅ Use Behave for visual pattern recognition
✅ Use Vatican Vault for sensitive data scanning
✅ Combine outputs in final forensic report

---

## Maintenance

### Updating Test Database
If replacing ActivitiesCache.db with newer data:
1. Backup existing database
2. Copy new ActivitiesCache.db to this folder
3. Re-run WindowsTimeline parser
4. Re-run Behave analysis
5. Update statistics in this README
6. Update `docs/KNOWLEDGE_BASE.md`
7. Re-run Vatican Vault tests to ensure compatibility

### Regenerating Tool Outputs
To recreate WindowsTimeline or Behave outputs with new database:
```bash
# WindowsTimeline
.\Get-WindowsTimeline.ps1 -Path "ActivitiesCache.db" -Output "WindowsTimeline_Output"

# Behave
python behave.py -db "ActivitiesCache.db" -o "Behave_V1_Output"
```

---

## Reference Links

**kacos2000 WindowsTimeline:**
- GitHub: https://github.com/kacos2000/WindowsTimeline
- Blog: https://kacos2000.github.io/

**TrustedSec Behave:**
- GitHub: https://github.com/trustedsec/behave (Note: May be in TrustedSec blog/resources)

**Windows Timeline Forensics:**
- See `Test Files/Vatican/` folder for additional research links
- Microsoft documentation on Windows Timeline
- DFIR blog posts on ActivitiesCache.db analysis

---

**Last Updated:** 2026-03-20
**Maintained by:** Vatican Vault Development Team
