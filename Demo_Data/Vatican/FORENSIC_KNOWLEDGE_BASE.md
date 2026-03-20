# Vatican Folder - Forensic Knowledge Base

**Purpose:** Reference links and techniques for Windows Timeline and Recall forensic analysis

---

## Overview

This knowledge base contains curated resources for forensic investigation of Windows activity tracking systems, specifically focusing on:
- **ActivitiesCache.db** - Windows Timeline database forensics
- **Windows Recall** - AI-powered snapshot system analysis
- **Evidence of Execution** - Application execution artifacts
- **Clipboard Forensics** - Clipboard data recovery techniques

---

## Resource Catalog

### 1. ActivitiesCacheParser Tool

**URL:** https://github.com/bolisettynihith/ActivitiesCacheParser
**Type:** Open-source Python forensic tool
**Author:** Nihith Bolisetty

#### What It Does
Python-based forensic utility for extracting data from Windows Activity Timeline databases. Parses the ActivitiesCache.db SQLite database to extract user activity records.

#### Key Forensic Artifacts
Extracts data from three primary tables:
- **Activity** - Core activity records (timestamps, app usage, files accessed)
- **ActivityOperation** - Operations associated with activities (sync, modifications)
- **Activity_PackageId** - Package identification data (application mappings)

#### Usage
```bash
python ActivitiesCacheParser.py -f <Path-to-ActivitiesCache.db>
```

#### Forensic Value
- User activity timeline reconstruction
- Application usage profiling
- File access history
- Device correlation across multiple systems
- Cloud sync activity tracking

---

### 2. Microsoft RecallSnapshotsExport

**URL:** https://github.com/microsoft/RecallSnapshotsExport
**Type:** Official Microsoft C++ code sample
**Language:** C++ (Visual Studio 2022)

#### What It Does
Demonstrates how to decrypt exported Windows Recall snapshots. Enables developers and forensic analysts to access encrypted snapshot data that users have exported.

#### Export Process
1. User accesses Recall export feature (during/after setup)
2. Microsoft provides a 32-character export code
3. User exports encrypted snapshots to local folder
4. Export code required for decryption

#### File Structure
**Decrypted exports contain:**
- **Image files** (.jpg) - Screenshot data of captured moments
- **Metadata files** (.json) - Associated metadata for each snapshot
- Organized by timestamp for timeline reconstruction

#### Forensic Value
- Visual records of user screen activity
- Temporal activity reconstruction
- Sensitive data exposure detection
- User behavior analysis
- Combined image + metadata creates comprehensive activity log

#### Technical Requirements
- Visual Studio 2022
- C++ compilation environment
- Export code from Microsoft Recall
- JsonHelper.h for metadata processing

---

### 3. Clipboard Forensics

**URL:** https://www.inversecos.com/2022/05/how-to-perform-clipboard-forensics.html
**Type:** Forensic analysis guide
**Status:** ⚠️ Access restricted (403)

#### Known Techniques
Based on ActivitiesCache.db structure, clipboard forensics involves:

**Database Fields:**
- **ClipboardPayload** (BLOB) - Stores clipboard content
- **Payload** (BLOB) - Activity details in JSON format
- **ContentInfo** (TEXT) - Clipboard content metadata

**Forensic Locations:**
1. **ActivitiesCache.db:**
   - `C:\Users\%USERNAME%\AppData\Local\ConnectedDevicesPlatform\L.%USERNAME%\ActivitiesCache.db`
   - Retention: Up to 30 days
   - Contains clipboard history if timeline sync enabled

2. **Memory Forensics:**
   - Clipboard data in process memory
   - Windows clipboard manager (clipbrd.exe)
   - Application-specific clipboard buffers

3. **Clipboard History:**
   - Windows 10/11 Clipboard History feature
   - Cloud sync via Microsoft account
   - Stored in user profile data

**Analysis Methods:**
```python
import sqlite3

conn = sqlite3.connect("ActivitiesCache.db")
cursor = conn.cursor()

# Extract clipboard activities
cursor.execute("""
    SELECT
        Id,
        StartTime,
        EndTime,
        ClipboardPayload,
        Payload
    FROM Activity
    WHERE ClipboardPayload IS NOT NULL
    ORDER BY StartTime DESC
""")

for row in cursor.fetchall():
    print(f"Clipboard activity at: {row[1]}")
    # Decode BLOB data for content
```

---

### 4. Evidence of Execution

**URL:** https://darkcybe.github.io/posts/DFIR_Evidence_of_Execution/
**Type:** DFIR (Digital Forensics & Incident Response) guide
**Status:** ⚠️ Access restricted (403)

#### Windows Execution Artifacts

**Key Locations:**

1. **Prefetch Files**
   - Location: `C:\Windows\Prefetch\`
   - Contains: Application execution history
   - Retention: Last 128 executions (Windows 10/11)

2. **Shimcache (Application Compatibility Cache)**
   - Registry: `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache`
   - Contains: File paths, last modified times, execution flags

3. **AmCache**
   - Location: `C:\Windows\appcompat\Programs\Amcache.hve`
   - Contains: Detailed application execution metadata

4. **ActivitiesCache.db**
   - Location: `C:\Users\%USERNAME%\AppData\Local\ConnectedDevicesPlatform\`
   - Contains: User-level activity timeline
   - Tracks: App launches, focus time, file access

5. **BAM/DAM (Background Activity Moderator)**
   - Registry: `HKLM\SYSTEM\CurrentControlSet\Services\bam\State\UserSettings`
   - Contains: Recent execution with precise timestamps

**Analysis Workflow:**
```
1. Timeline Creation
   - Combine artifacts from multiple sources
   - Normalize timestamps (UTC vs local)
   - Cross-reference execution evidence

2. Application Profiling
   - Identify all executions of specific binary
   - Determine execution frequency
   - Detect anomalous execution patterns

3. Lateral Movement Detection
   - Remote execution artifacts (PsExec, WMI)
   - Network share access
   - Service creation/modification
```

---

### 5. Windows Recall Management

**Microsoft Learn URLs:**
- Decrypt Snapshots: https://learn.microsoft.com/en-us/windows/ai/recall/decrypt-exported-snapshots
- Manage Recall: https://learn.microsoft.com/en-us/windows/client-management/manage-recall

**Status:** ⚠️ Access restricted (403)

#### Enterprise Management (Known Details)

**Group Policy Controls:**
- Registry Key: `HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsAI\AllowRecallEnablement`
- Values:
  - `0x00000000` - Disable Recall for all users
  - `0x00000001` - Enable Recall for managed users
  - (deleted) - Default (allow home users)

**Data Storage:**
- Encrypted snapshots stored locally
- User-controlled retention periods
- Export requires 32-character code
- Sensitive content filtering available

**Privacy Controls:**
- Per-application exclusions
- Content filtering rules
- Screenshot frequency settings
- Local processing (no cloud by default)

---

### 6. Recall Configuration Guides

**Winaero:** https://winaero.com/disable-recall-windows/
**Pureinfotech:** https://pureinfotech.com/access-recall-ai-data-locally-stored-windows-11/
**Status:** ⚠️ Access restricted (403)

#### Known Configuration Methods

**PowerShell:**
```powershell
# Enable Recall feature
Enable-WindowsOptionalFeature -Online -FeatureName "Recall"

# Disable Recall feature
Disable-WindowsOptionalFeature -Online -FeatureName "Recall"
```

**Registry Files (Included in Vatican Folder):**

1. **Default_enable_Recall_feature_for_home_users.reg**
   - Removes Group Policy restriction
   - Allows default behavior (enabled for home users)

2. **Disable_Recall_feature_for_all_users.reg**
   - Sets `AllowRecallEnablement = 0`
   - Blocks Recall for all users

3. **Enable_Recall_feature_for_all_managed_users.reg**
   - Sets `AllowRecallEnablement = 1`
   - Forces Recall enabled in enterprise

---

## Forensic Analysis Workflow

### Phase 1: Data Collection

```bash
# Collect ActivitiesCache.db
Copy-Item "C:\Users\*\AppData\Local\ConnectedDevicesPlatform\*\ActivitiesCache.db" -Destination ".\evidence\"

# Collect Recall data (if present)
Copy-Item "C:\Users\*\AppData\Local\Microsoft\Windows\Recall\*" -Destination ".\evidence\recall\" -Recurse

# Collect Prefetch
Copy-Item "C:\Windows\Prefetch\*" -Destination ".\evidence\prefetch\"

# Export Registry keys
reg export "HKLM\SYSTEM\CurrentControlSet\Services\bam" ".\evidence\bam_registry.reg"
reg export "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsAI" ".\evidence\recall_policy.reg"
```

### Phase 2: Database Analysis

```python
import sqlite3
import json
from datetime import datetime

def analyze_activities_cache(db_path):
    """Comprehensive ActivitiesCache.db analysis"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get activity summary
    cursor.execute("""
        SELECT
            COUNT(*) as total_activities,
            MIN(StartTime) as first_activity,
            MAX(EndTime) as last_activity
        FROM Activity
    """)
    summary = cursor.fetchone()
    print(f"Total Activities: {summary[0]}")
    print(f"Date Range: {summary[1]} to {summary[2]}")

    # Application usage
    cursor.execute("""
        SELECT
            AppId,
            COUNT(*) as count,
            SUM(julianday(EndTime) - julianday(StartTime)) * 24 * 60 as total_minutes
        FROM Activity
        WHERE AppId IS NOT NULL
        GROUP BY AppId
        ORDER BY count DESC
        LIMIT 20
    """)

    print("\nTop Applications:")
    for app, count, minutes in cursor.fetchall():
        print(f"  {app}: {count} activities, {minutes:.1f} minutes")

    # Clipboard activities
    cursor.execute("""
        SELECT
            StartTime,
            EndTime,
            ClipboardPayload
        FROM Activity
        WHERE ClipboardPayload IS NOT NULL
        ORDER BY StartTime DESC
        LIMIT 10
    """)

    print("\nClipboard Activities:")
    for start, end, payload in cursor.fetchall():
        print(f"  {start}: {len(payload)} bytes")

    conn.close()

# Usage
analyze_activities_cache("./evidence/ActivitiesCache.db")
```

### Phase 3: Timeline Reconstruction

```python
def create_timeline(db_path, output_csv):
    """Export comprehensive timeline to CSV"""
    import csv

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.StartTime,
            a.EndTime,
            a.AppId,
            a.ActivityType,
            a.Payload,
            ap.AppActivityId
        FROM Activity a
        LEFT JOIN Activity_PackageId ap ON a.Id = ap.ActivityId
        ORDER BY a.StartTime
    """)

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Start', 'End', 'Application', 'Type', 'Payload', 'PackageId'])

        for row in cursor.fetchall():
            # Decode JSON payload if present
            payload = row[4]
            if payload:
                try:
                    payload = json.loads(payload)
                except:
                    payload = str(payload)[:100]

            writer.writerow([
                row[0],  # Start
                row[1],  # End
                row[2],  # AppId
                row[3],  # Type
                str(payload),  # Payload
                row[5]   # PackageId
            ])

    conn.close()
    print(f"Timeline exported to {output_csv}")

# Usage
create_timeline("./evidence/ActivitiesCache.db", "./timeline.csv")
```

---

## Key Forensic Techniques

### 1. Temporal Analysis
- Cross-reference timestamps across multiple artifacts
- Detect time manipulation attempts
- Identify activity patterns and anomalies

### 2. Application Profiling
- Track all executions of suspicious binaries
- Correlate with network activity
- Identify persistence mechanisms

### 3. Clipboard Data Recovery
- Extract sensitive data from clipboard history
- Detect credential exposure
- Track copy-paste activities

### 4. Visual Timeline Reconstruction
- Combine Recall snapshots with ActivitiesCache data
- Create comprehensive user activity narrative
- Identify sensitive data exposure moments

### 5. Cloud Sync Analysis
- Track cross-device activity synchronization
- Identify data exfiltration via cloud sync
- Correlate timeline data across multiple devices

---

## Security Considerations

### For Defenders

**Detection Opportunities:**
- Monitor ActivitiesCache.db access patterns
- Alert on bulk database exports
- Detect Recall snapshot decryption attempts
- Track Group Policy modifications

**Privacy Controls:**
- Implement application exclusions
- Configure data retention policies
- Enable content filtering
- Regular data purging

### For Forensic Investigators

**Best Practices:**
- Preserve original database files (including .db-shm and .db-wal)
- Document collection timestamps
- Use read-only analysis methods
- Export to neutral formats (CSV, JSON)
- Maintain chain of custody

**Common Pitfalls:**
- Overwriting WAL files during analysis
- Missing cloud-synced data
- Ignoring timezone conversions
- Incomplete artifact collection

---

## Tools Reference

### Open Source
- **ActivitiesCacheParser** - Python-based parser
- **DB Browser for SQLite** - Manual database analysis
- **Eric Zimmerman Tools** - Comprehensive Windows forensics suite
- **WindowsTimeline** (kacos2000) - PowerShell parser

### Microsoft Official
- **RecallSnapshotsExport** - Recall snapshot decryption
- **Timeline export** - Built-in Windows feature

### Commercial
- **Magnet AXIOM** - Automated timeline analysis
- **X-Ways Forensics** - Low-level database examination
- **Cellebrite** - Mobile and Windows timeline correlation

---

## Database Schema Reference

### ActivitiesCache.db Tables

**Activity (Primary table)**
```sql
CREATE TABLE Activity (
    Id TEXT PRIMARY KEY,
    AppId TEXT,
    AppActivityId TEXT,
    ActivityType INTEGER,
    Payload BLOB,           -- JSON activity data
    ClipboardPayload BLOB,  -- Clipboard content
    StartTime DATETIME,
    EndTime DATETIME,
    LastModifiedTime DATETIME,
    ExpirationTime DATETIME,
    Tag TEXT,
    Group TEXT,
    MatchId TEXT,
    LastModifiedOnClient DATETIME
);
```

**Activity_PackageId (Application mapping)**
```sql
CREATE TABLE Activity_PackageId (
    ActivityId TEXT,
    Platform TEXT,
    PackageName TEXT,
    AppActivityId TEXT,
    FOREIGN KEY (ActivityId) REFERENCES Activity(Id)
);
```

**ActivityOperation (Sync operations)**
```sql
CREATE TABLE ActivityOperation (
    OperationId TEXT PRIMARY KEY,
    ActivityId TEXT,
    OperationType INTEGER,
    StartTime DATETIME,
    EndTime DATETIME,
    OperationOrder INTEGER,
    Payload BLOB
);
```

---

## Future Research Areas

1. **AI-Powered Analysis**
   - Automated sensitive data detection in Recall snapshots
   - ML-based anomaly detection in activity timelines
   - OCR integration for screenshot text extraction

2. **Cross-Platform Correlation**
   - Linking Windows Timeline with mobile device activity
   - Cloud service integration analysis
   - Multi-device user profiling

3. **Advanced Persistence Detection**
   - Timeline-based persistence mechanism identification
   - Behavioral analysis for threat hunting
   - Correlation with EDR telemetry

4. **Privacy-Preserving Forensics**
   - Selective data extraction techniques
   - Encrypted analysis workflows
   - Compliance-aware investigation methods

---

## Related Resources in Test System

- **ActivitiesCache.db** - Reference test database
- **WindowsTimeline_Output/** - Parsed timeline data examples
- **Behave_V1_Output/** - Behavioral analysis visualizations
- **Registry files** - Recall management configurations

---

**Last Updated:** 2026-03-20
**Maintained by:** Behave v2 Project
**Version:** 1.0
