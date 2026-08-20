# Automated and Manual Test Cases — LocalSearch

The following test suite verifies the functionality, validation, persistence, and edge-case behavior of **LocalSearch — Python Keyword Search Engine**.

All automated test cases are implemented in `tests/test_search_engine.py` and executed using `pytest`.

---

## 📊 Summary of Test Execution

```text
Framework: Pytest 8.4.2
Python Version: 3.9.10
Total Test Cases: 11
Passed: 11
Failed: 0
Execution Time: 0.28s
```

---

## 🧪 Detailed Test Matrix

| Test ID | Scenario | Input | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Normal Single Keyword Search | `"python"` | Returns matching documents containing term `"python"`, ranked by TF-IDF score. | Returned `python.txt` and `machine_learning.txt` with scores > 0. | **PASS** |
| **TC-02** | Multiple Keywords Search & Ranking | `"machine learning"` | Returns documents matching any query term, ranked by aggregated score descending. | Returned `machine_learning.txt` (#1, Score 0.4497) followed by `python.txt` (#2, Score 0.0526). | **PASS** |
| **TC-03** | No Results Search | `"xyznonexistentterm"` | Returns empty result list without throwing an error or crashing. | Returned 0 results with message `"No matching documents found"`. | **PASS** |
| **TC-04** | Empty Query Validation | `""` or `"   "` | Throws `ValueError` and displays clean validation error message. | Raised `ValueError("Search query cannot be empty")` and rejected input. | **PASS** |
| **TC-05** | Invalid Directory Path | `"/nonexistent/path"` | Throws `FileNotFoundError` and displays path validation error message. | Raised `FileNotFoundError` and returned controlled validation error. | **PASS** |
| **TC-06** | Case-Insensitive Search | `"Python"`, `"python"`, `"PYTHON"` | Produces identical search results and identical scores regardless of case. | All 3 inputs returned identical ranking order and identical TF-IDF scores. | **PASS** |
| **TC-07** | Empty File Handling | `empty.txt` (0 bytes) | Indexes empty document safely without division-by-zero or crashing. | Indexed `empty.txt` with `word_count=0` without error. | **PASS** |
| **TC-08** | Idempotent Re-indexing | Index same directory twice | Vocabulary count and total indexed documents remain constant without duplicates. | Indexed count remained 4 and unique terms count remained identical. | **PASS** |
| **TC-09** | Persistence Save and Load | Save index → Load into new instance | Loaded index produces identical search results and scores as original instance. | Loaded index retrieved identical document list and matching scores. | **PASS** |
| **TC-10** | Rebuild Index with New Content | Add `crypto.txt` → Rebuild | Rebuilt index immediately includes new document in query search results. | Query `"blockchain"` returned newly added `crypto.txt` after rebuild. | **PASS** |
| **TC-11** | Result Limit Validation | Limit input `"-3"` or `"abc"` | Rejects negative or non-numeric limit inputs with validation message. | Rejected invalid limits and defaulted to 10 for standard usage. | **PASS** |

---

## 🏃 Running Automated Tests

To re-run the complete test suite:

```bash
python -m pytest -v
```

Output verification:
```text
tests/test_search_engine.py::test_normal_single_keyword_search PASSED
tests/test_search_engine.py::test_multiple_keyword_search PASSED
tests/test_search_engine.py::test_no_results_search PASSED
tests/test_search_engine.py::test_empty_query_validation PASSED
tests/test_search_engine.py::test_invalid_folder_validation PASSED
tests/test_search_engine.py::test_case_insensitive_search PASSED
tests/test_search_engine.py::test_empty_document_handling PASSED
tests/test_search_engine.py::test_reindexing_idempotency PASSED
tests/test_search_engine.py::test_persistence_save_load PASSED
tests/test_search_engine.py::test_rebuild_index PASSED
tests/test_search_engine.py::test_result_limit_validation PASSED

============================= 11 passed in 0.28s ==============================
```
