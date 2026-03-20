# Test Files - Vatican Vault Reference Data
**Purpose:** Permanent reference data for testing, training, and forensic analysis

---

## 📦 PCAP Files Location

**⚠️ IMPORTANT:** PCAP network capture files have been consolidated to the main PCAP folder.

**Primary Location:** `/PCAP/` (project root)

**Available PCAP Files:**
- `The Ultimate PCAP v20251206.pcapng` (14.8 MB) - Primary compliance testing data
- `4SICSGeekLounge151.pcap` (25 MB) - ICS/SCADA network traffic
- `test_sample.pcap` (562 bytes) - Basic validation file

**Archived Version:** This folder contains `The-Ultimate-PCAP.7z` (4.9 MB compressed) for distribution purposes.

**📖 See:** `/PCAP/README.md` for comprehensive PCAP documentation, usage examples, and testing instructions.

---

## Directory Structure

```
Test Files/
├── Test System/                    # Reference database and forensic tool outputs
│   ├── ActivitiesCache.db         # Real Windows Timeline database (4.71 MB, 1,853 activities)
│   ├── ActivitiesCache.db-shm     # SQLite shared memory file (WAL mode)
│   ├── ActivitiesCache.db-wal     # SQLite write-ahead log (transaction log)
│   ├── WindowsTimeline_Output/    # kacos2000 WindowsTimeline parser output
│   ├── Behave_V1_Output/          # TrustedSec Behave analysis output
│   └── README.md                  # Test System documentation
├── Vatican/                        # Windows Recall management resources
│   ├── FORENSIC_KNOWLEDGE_BASE.md # Comprehensive forensic techniques guide
│   ├── *.reg                      # Registry files for Recall enable/disable
│   ├── *.url (8 files)            # Research links and documentation
│   └── notes.txt                  # ActivitiesCache.db location info
├── docs/                          # Microsoft Synthetic PII/PHI Dataset (18.9 MB)
│   ├── CreditCardNumber/         # 8 Excel files with test credit card data
│   ├── SSN/                      # Social Security Number test files
│   ├── CanadianSocialInsuranceNumber/  # Canadian SIN test data
│   ├── USSocialSecurityNumber/   # US SSN formatted/unformatted
│   ├── PII/                      # 40+ international PII files
│   ├── Financial/                # Mixed financial data
│   ├── TestData/                 # FOLDER1-4 with mixed file types
│   ├── Fingerprinting docs/      # Document templates and patient forms
│   ├── USUK Passports/           # Passport test documents
│   ├── Mixed docs with PII/      # Real-world mixed PII scenarios
│   └── _creds/, _pii/            # Additional credential and PII tests
├── Scripts/                       # PowerShell security scripts
└── Other tools/                   # Additional utilities
```

---

## Important: Database Files Setup

The Test System folder should contain all three SQLite database files:
- `ActivitiesCache.db` ✅ (currently in git)
- `ActivitiesCache.db-shm` ⚠️ (add if you have it locally)
- `ActivitiesCache.db-wal` ⚠️ (add if you have it locally)

If you have the `.db-shm` and `.db-wal` files on your local system, add them with:

```bash
cd "Test Files/Test System"
git add -f ActivitiesCache.db-shm ActivitiesCache.db-wal
git commit -m "feat: add SQLite WAL files to Test System reference dataset"
```

The `.gitignore` has been configured with explicit exceptions to allow these test files while blocking production database files elsewhere.

---

## Quick Start

### 1. Analyze ActivitiesCache.db

```python
import sqlite3

conn = sqlite3.connect("Test Files/Test System/ActivitiesCache.db")
cursor = conn.cursor()

# Get all activities
cursor.execute("SELECT COUNT(*) FROM Activity")
print(f"Total activities: {cursor.fetchone()[0]}")

# Top applications
cursor.execute("""
    SELECT AppId, COUNT(*) as count
    FROM Activity
    GROUP BY AppId
    ORDER BY count DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} activities")

conn.close()
```

### 2. Test Sensitive Data Scanner

```python
from backend.app.core.security.sensitive_scanner import SensitiveDataScanner

scanner = SensitiveDataScanner()

# Test with synthetic credit card data
test_text = "Card number: 4111-1111-1111-1111, expires 12/25"
exposures = scanner.scan_text(test_text, "test", 0, "Test", "")

for exp in exposures:
    print(f"Found {exp.exposure_type.value}: {exp.redacted_value}")
```

### 3. Run Comprehensive Tests

```bash
python test_sensitive_scanner.py
```

**Expected Results:**
- Total Tests: 20
- Pass Rate: 100% (20/20) ✅
- Credit Cards: 5/5 ✅
- SSN: 4/4 ✅
- API Keys: 4/4 ✅
- Emails: 3/3 ✅
- International PII: 4/4 ✅ (Belgian, Czech, Finnish, German)

### 4. Enable/Disable Windows Recall

**Disable Recall:**
```cmd
reg import "Test Files/Vatican/Disable_Recall_feature_for_all_users.reg"
```

**Enable Recall (Managed):**
```cmd
reg import "Test Files/Vatican/Enable_Recall_feature_for_all_managed_users.reg"
```

**Remove Policy (Default):**
```cmd
reg import "Test Files/Vatican/Default_enable_Recall_feature_for_home_users.reg"
```

---

## ActivitiesCache.db Details

**Location:** `Test Files/Test System/ActivitiesCache.db`
**Database:** SQLite3
**Size:** 4.71 MB
**Tables:** 8 (Activity, ActivityOperation, Activity_PackageId, etc.)
**Activities:** 1,853
**Date Range:** October 16, 2022 - March 10, 2023 (146 days)
**Applications:** 75+

### Top Applications
1. VirtualBox - 416 activities (22.45%)
2. Windows Explorer - 336 activities (18.13%)
3. Steam Client - 116 activities (6.26%)
4. Notepad - 107 activities (5.77%)
5. Rockstar Social Club - 85 activities (4.59%)

### Table Summary
| Table | Rows | Purpose |
|-------|------|---------|
| Activity | 1,853 | Core activity records |
| Activity_PackageId | 6,296 | Application mappings |
| ActivityOperation | 0 | Sync operations (empty) |
| DataEncryptionKeys | 1 | Encryption keys |
| Metadata | 5 | Database configuration |
| AppSettings | 0 | App-specific settings |
| Asset | 0 | Thumbnails/icons |
| ManualSequence | 1 | Sequence counter |

### Key Fields
- **ClipboardPayload** (BLOB): Clipboard data (empty in test DB for privacy)
- **Payload** (BLOB): Activity details (JSON format)
- **AppId** (TEXT): Application identifier (JSON array)
- **StartTime/EndTime** (DATETIME): Unix epoch timestamps
- **ActivityType** (INT): Activity category (5=app, 6=engagement, 11=settings, 16=sync)

---

## Vatican Folder Resources

**Overview:** The Vatican folder is a forensic knowledge base containing links to websites that detail better forensic testing techniques and tricks, along with registry files for managing Windows Recall.

📖 **[FULL DOCUMENTATION: FORENSIC_KNOWLEDGE_BASE.md](Vatican/FORENSIC_KNOWLEDGE_BASE.md)**

This comprehensive guide includes:
- Detailed tool documentation (ActivitiesCacheParser, RecallSnapshotsExport)
- Forensic analysis workflows and techniques
- Database schema reference
- Python code examples for timeline reconstruction
- Security considerations for defenders and investigators
- Evidence of execution artifact locations
- Clipboard forensics methodologies

### Quick Reference

**Registry Files (*.reg)** - Manage Windows Recall via Group Policy

| File | Effect | Registry Value |
|------|--------|----------------|
| Default_enable_Recall_feature_for_home_users.reg | Remove policy | (delete key) |
| Disable_Recall_feature_for_all_users.reg | Disable Recall | `0x00000000` |
| Enable_Recall_feature_for_all_managed_users.reg | Enable Recall | `0x00000001` |

**Registry Key:** `HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsAI\AllowRecallEnablement`

**Research Links (8 URLs)** - Curated forensic resources

| Resource | Focus Area |
|----------|-----------|
| ActivitiesCacheParser (GitHub) | Python-based Timeline parser |
| RecallSnapshotsExport (GitHub) | Microsoft's snapshot decryption tool |
| Microsoft Learn - Decrypt | Recall snapshot decryption process |
| Microsoft Learn - Manage | Enterprise Recall management |
| inversecos.com | Clipboard forensics techniques |
| darkcybe.github.io | Evidence of execution artifacts |
| Winaero | Recall enable/disable guide |
| Pureinfotech | Local Recall data access |

**notes.txt** - Quick reference for ActivitiesCache.db location and PowerShell commands

---

## Microsoft Synthetic PII/PHI Dataset

### Overview
**Source:** Microsoft Compliance Team
**Purpose:** Testing data loss prevention (DLP) and compliance scanners
**Status:** ✅ **SYNTHETIC DATA** - Safe for testing, not real PII/PHI
**Size:** 18.9 MB
**Files:** 300+ files across 9 categories

### Dataset Characteristics
- ✅ Follows proper schemas of real data
- ✅ Enables accurate compliance testing
- ✅ Validated by Microsoft
- ✅ Safe for development/testing
- ❌ NOT real PII/PHI
- ❌ Do not use for production without proper review

### Categories

#### 1. Credit Card Numbers (276 KB, 8 files)
**Formats:** Visa, Mastercard, AmEx, Discover
**Patterns:**
- 16-digit: `4111-1111-1111-1111`
- 15-digit: `3400-000000-00009`
- With/without separators

**Test Coverage:**
- ✅ Luhn algorithm validation
- ✅ Separator handling (dash, space, none)
- ✅ Mixed with financial data

#### 2. Social Security Numbers (14 files)
**Formats:**
- With dashes: `123-45-6789`
- Without dashes: `123456789`

**Files:**
- Core samples (2 files)
- Formatted SSN (6 employee rosters)
- Unformatted SSN (6 employee rosters)

**Test Coverage:**
- ✅ Format detection (with/without dashes)
- ✅ Validation (area/group/serial numbers)
- ✅ Context detection (HR forms, rosters)

#### 3. Canadian SIN (6 files)
**Format:** `123-456-789`
**Content:** Employee rosters, HR profiles

#### 4. International PII (40+ files, 1.4 MB)
**Countries:** Belgium, Czech Republic, Denmark, Germany, Spain, Finland, France, Greece, Ireland, Italy, Poland, Sweden, UK

**ID Types:**
- National ID cards
- Driver's licenses
- Personal numbers
- Tax identifiers

**File Formats:** .docx, .txt, .pdf, .xlsx

**Test Coverage:**
- ⚠️ Belgian: 25% (patterns not implemented)
- ⚠️ Czech: 25% (patterns not implemented)
- ⚠️ Finnish: 25% (patterns not implemented)
- ✅ German: 100% (phone numbers detected)

#### 5. Financial Data (11 files)
**Content:**
- Transaction logs
- Expense accounts
- Classification samples
- Mixed financial PII

#### 6. Test Data Collections (24 files in 4 folders)
**File Types:** .msg (email), .docx, .pptx, .pdf, .txt, .xlsx
**Content Types:**
- C-Record (Credit cards)
- H-Record (Health/PHI)
- PIIs (General PII)

**Purpose:** Real-world document testing

#### 7. Document Fingerprinting (6 files)
**Content:**
- Office specification templates
- Patient information forms
- Medical evaluation forms

**Purpose:** Template matching, document classification

#### 8. US/UK Passports (5 files)
**Content:**
- Offer letters with passport info
- Visa applications

#### 9. Mixed Documents (160+ files)
**Purpose:** Real-world scenarios with multiple PII types
**Languages:** English, Spanish
**Content:**
- Multiple PII types in single documents
- Admin passwords
- Mixed international formats

---

## Usage Guidelines

### DO ✅
- Use for testing sensitive data scanners
- Use for ML model training
- Use for compliance tool development
- Use for forensic technique validation
- Reference in documentation

### DON'T ❌
- Use in production without review
- Assume this replaces real-world testing
- Treat as real PII/PHI
- Share outside authorized contexts
- Modify or delete these reference files

---

## Test Scripts

### test_sensitive_scanner.py
**Location:** Project root
**Purpose:** Comprehensive scanner testing
**Tests:** 20 tests across 5 categories
**Pass Rate:** 85% (17/20)

**Run:**
```bash
python test_sensitive_scanner.py
```

**Output:**
- Console summary with pass/fail status
- JSON report: `test_outputs/sensitive_scanner_test_report.json`

### comprehensive_poc_demo.py
**Location:** Project root
**Purpose:** End-to-end POC demonstration
**Uses:** ActivitiesCache.db

**Run:**
```bash
python comprehensive_poc_demo.py
```

**Output:**
- `test_outputs/quick_scan_YYYY-MM-DD_HH-MM-SS/`
- scan_summary.json
- activities.json (all 1,853 activities)
- entities_extracted.json
- sentiment_analysis.json
- forensic_report.html

---

## Documentation

### Comprehensive Knowledge Base
**File:** `docs/KNOWLEDGE_BASE.md`

**Contains:**
- Complete ActivitiesCache.db schema
- Forensic SQL queries
- Windows Recall management
- Test data structure
- Integration examples
- Research links summary

### Testing Summary
**File:** `TESTING_SUMMARY.md`

**Contains:**
- Test results (85% pass rate)
- Scanner improvements
- Known limitations
- Files modified

---

## Maintenance

### Adding New Test Data
1. Place files in appropriate `docs/` subdirectory
2. Update this README with file counts
3. Update `docs/KNOWLEDGE_BASE.md` if needed
4. Create corresponding test cases
5. Document any new patterns discovered

### Updating ActivitiesCache.db
If replacing with newer database:
1. Backup existing file
2. Update statistics in this README
3. Update `docs/KNOWLEDGE_BASE.md` statistics
4. Re-run comprehensive_poc_demo.py
5. Verify existing tests still pass

### Adding Vatican Resources
1. Place .reg files in `Vatican/` folder
2. Place .url files in `Vatican/` folder
3. Update this README
4. Update `docs/KNOWLEDGE_BASE.md`
5. Test registry modifications on VM

---

## Support

### For Issues
- Check `docs/KNOWLEDGE_BASE.md` for detailed reference
- Check `TESTING_SUMMARY.md` for test results
- Review Vatican folder links for additional research
- Open issue on GitHub repository

### For Questions
- Database structure: See `docs/KNOWLEDGE_BASE.md` Section 1
- Test data format: See this README and KNOWLEDGE_BASE.md Section 3
- Recall management: See KNOWLEDGE_BASE.md Section 2
- Forensic techniques: See KNOWLEDGE_BASE.md Section 4

---

**Last Updated:** 2026-03-20
**Maintained by:** Vatican Vault Development Team
