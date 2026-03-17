# Test Reports - User Behavior Analysis Platform v2

## 📊 Latest Test Run

**Generated:** 2026-02-28 03:20:55
**Test Suite:** Standalone Demo Tests
**Total Tests:** 32
**Status:** ✅ ALL TESTS PASSED

### Test Results Summary

| Metric | Value |
|--------|-------|
| Total Tests | 32 |
| Passed | 32 ✓ |
| Failed | 0 ✗ |
| Skipped | 0 ⊘ |
| Success Rate | 100% |
| Execution Time | ~13 seconds |

### Code Coverage

| Metric | Value |
|--------|-------|
| Coverage | 0.01% |
| Covered Lines | 1 / 13,033 |

*Note: Low coverage is expected for demo tests as they don't exercise the main application code.*

## 🌐 Viewing Reports (After Download)

**Important:** If you downloaded this repository as a ZIP file, the HTML reports may show blank screens when opened directly due to browser security restrictions.

**Recommended Method:**

```bash
# Navigate to the Sample_Outputs directory
cd Promo/Sample_Outputs

# Start a local HTTP server
python -m http.server 8000
```

Then open your browser to:
- **Main Report:** `http://localhost:8000/latest/index.html`
- **Coverage:** `http://localhost:8000/latest/coverage_html/index.html`
- **Pytest Details:** `http://localhost:8000/latest/pytest_report.html`

For more detailed viewing instructions, see [HOW_TO_VIEW_REPORTS.md](HOW_TO_VIEW_REPORTS.md)

## 📁 Report Files

The test runner generates multiple report formats for comprehensive analysis:

### 1. Interactive HTML Report
**File:** `reports/[timestamp]/index.html`

Enhanced interactive dashboard featuring:
- 📈 Real-time statistics with animated progress bars
- 🎨 Modern, responsive design
- 🔍 Expandable test suite details
- ⚡ Quick navigation to detailed reports

### 2. Pytest HTML Report
**File:** `reports/[timestamp]/pytest_report.html`

Standard pytest-html report with:
- Detailed test execution logs
- Full stack traces for failures
- Environment information
- Test metadata

### 3. Coverage HTML Report
**File:** `reports/[timestamp]/coverage_html/index.html`

Comprehensive code coverage visualization:
- Line-by-line coverage analysis
- Color-coded coverage indicators
- File-by-file breakdown
- Missing line highlights

### 4. JUnit XML
**File:** `reports/[timestamp]/junit.xml`

Machine-readable test results for:
- CI/CD integration
- Test result aggregation
- Automated reporting
- Jenkins/GitLab CI compatibility

### 5. Coverage JSON
**File:** `reports/[timestamp]/coverage.json`

Programmatic coverage data:
- Detailed coverage metrics
- File-level statistics
- Integration-ready format

## 🚀 Running Tests

### Quick Start

Run all tests and generate reports:

```bash
python tools/testing/run_tests_with_reports.py
```

### Manual Pytest Commands

Run specific test suites:

```bash
# Run all standalone tests
python -m pytest standalone_tests -v

# Run with coverage
python -m pytest standalone_tests -v --cov=standalone_tests --cov-report=html

# Run specific test class
python -m pytest standalone_tests -k "TestBasicFunctionality" -v

# Run with detailed output
python -m pytest standalone_tests -v --tb=long
```

### Backend Tests

To run backend unit tests (requires dependencies):

```bash
cd backend
python -m pytest tests/unit -v
```

To run integration tests:

```bash
cd backend
python -m pytest tests/integration -v
```

## 📋 Test Suites

### Standalone Demo Tests

Located in: `standalone_tests/test_demo.py`

**Test Classes:**

1. **TestBasicFunctionality** (5 tests)
   - Basic arithmetic operations
   - String manipulations

2. **TestDataStructures** (3 tests)
   - List operations
   - Dictionary operations
   - Set operations

3. **TestTimestampGeneration** (2 tests)
   - Timestamp creation
   - Date formatting

4. **TestFileOperations** (2 tests)
   - Path operations
   - Temp directory access

5. **TestMathOperations** (3 tests)
   - Power operations
   - Modulo operations
   - Floor division

6. **TestBooleanLogic** (3 tests)
   - AND operator
   - OR operator
   - NOT operator

7. **TestExceptionHandling** (3 tests)
   - ValueError handling
   - KeyError handling
   - ZeroDivisionError handling

8. **TestPerformance** (2 tests)
   - List comprehension performance
   - String concatenation performance

9. **Parametrized Tests** (9 tests)
   - Parametrized doubling tests (5 cases)
   - Parametrized string length tests (4 cases)

## 🎯 Test Coverage Goals

### Current Coverage Targets

- **Unit Tests:** 80%+ coverage
- **Integration Tests:** 60%+ coverage
- **Critical Paths:** 95%+ coverage

### Improving Coverage

To improve test coverage:

1. **Write More Unit Tests**
   ```bash
   # Add tests in backend/tests/unit/
   ```

2. **Test Edge Cases**
   - Boundary conditions
   - Error scenarios
   - Invalid inputs

3. **Integration Testing**
   - API endpoints
   - Database operations
   - External service integration

## 🔧 Configuration

### Pytest Configuration

Main config: `backend/pytest.ini`
Alternative: `pyproject.toml`

Key settings:
- Test discovery patterns
- Coverage options
- Parallel execution
- Markers for test categories

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit  # Fast, isolated tests
@pytest.mark.integration  # Slower, may need services
@pytest.mark.slow  # Long-running tests
@pytest.mark.api  # API endpoint tests
```

Run specific markers:

```bash
pytest -m unit  # Run only unit tests
pytest -m "not slow"  # Skip slow tests
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run Tests
  run: |
    python tools/testing/run_tests_with_reports.py

- name: Upload Test Reports
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: Sample_Outputs/reports/
```

### GitLab CI Example

```yaml
test:
  script:
    - python tools/testing/run_tests_with_reports.py
  artifacts:
    paths:
      - Sample_Outputs/reports/
    reports:
      junit: Sample_Outputs/reports/*/junit.xml
```

## 🐛 Troubleshooting

### Common Issues

**Issue:** Tests not found
```bash
# Solution: Check test file naming
# Test files must start with "test_"
# Test functions must start with "test_"
```

**Issue:** Import errors
```bash
# Solution: Install dependencies
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt
```

**Issue:** Coverage too low
```bash
# Solution: Run with coverage report to see what's missing
pytest --cov=. --cov-report=term-missing
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Pytest-HTML Plugin](https://pytest-html.readthedocs.io/)

## 🎨 Report Screenshots

The interactive HTML reports feature:
- Modern gradient design
- Animated statistics
- Expandable test suites
- Mobile-responsive layout
- Dark mode compatible

## 📝 Notes

- Reports are timestamped for easy tracking
- Old reports are automatically cleaned before new runs
- All reports are gitignored to prevent repo bloat
- Coverage reports exclude test files themselves

---

**Last Updated:** 2026-02-28
**Report Generator Version:** 1.0
**Platform:** User Behavior Analysis v2.0
