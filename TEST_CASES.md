# Automated and Manual Test Cases — LocalSearch

The following test suite verifies the functionality, validation, persistence, and edge-case behavior of **LocalSearch — Python Keyword Search Engine**.

All 14 automated test cases are implemented in `tests/test_search_engine.py` and executed using `pytest`.

---

## 📊 Summary of Test Execution

```text
Environment: Windows 11 (Python 3.9.10)
Framework: Pytest 8.4.2
Total Test Cases: 14
Passed: 14
Failed: 0
Execution Time: 0.20s
Status: ALL TESTS PASSED
```

---

## 🧪 Detailed Test Matrix

| Test ID | Scenario | Input | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Normal Single Keyword Search | `"python"` | Returns matching documents containing term `"python"`, ranked by TF-IDF score. | Returned `python.txt` (#1, Score 0.0811) and `web_development.txt` (#2, Score 0.0226) with scores > 0. | **PASS** |
| **TC-02** | Multiple Keywords Search & Ranking | `"machine learning"` | Returns documents matching any query term, ranked by aggregated score descending. | Returned `machine_learning.txt` (#1, Score 0.2121) followed by `artificial_intelligence.txt` (#2, Score 0.0452) and `python.txt` (#3, Score 0.0406). | **PASS** |
| **TC-03** | No Results Search | `"xyznonexistentterm"` | Returns empty result list without throwing an error or crashing. | Returned 0 results with message `"No matching documents found"`. | **PASS** |
| **TC-04** | Empty Query Validation | `""` or `"   "` | Throws `ValueError` and displays clean validation error message. | Raised `ValueError("Search query cannot be empty")` and rejected input. | **PASS** |
| **TC-05** | Invalid Directory Path | `"/nonexistent/path"` | Throws `FileNotFoundError` and displays path validation error message. | Raised `FileNotFoundError` and returned controlled validation error. | **PASS** |
| **TC-06** | Case-Insensitive Search | `"Python"`, `"python"`, `"PYTHON"` | Produces identical search results and identical scores regardless of case. | All 3 inputs returned identical ranking order and identical TF-IDF scores. | **PASS** |
| **TC-07** | Empty File Handling | `empty.txt` (0 bytes) | Indexes empty document safely without division-by-zero or crashing. | Indexed `empty.txt` with `word_count=0` without error. | **PASS** |
| **TC-08** | Idempotent Re-indexing | Index same directory twice | Vocabulary count and total indexed documents remain constant without duplicates. | Indexed count remained 4 and unique terms count remained identical. | **PASS** |
| **TC-09** | Persistence Save and Load | Save index → Load into new instance | Loaded index produces identical search results and scores as original instance. | Loaded index retrieved identical document list and matching scores. | **PASS** |
| **TC-10** | Rebuild Index with New Content | Add `crypto.txt` → Rebuild | Rebuilt index immediately includes new document in query search results. | Query `"blockchain"` returned newly added `crypto.txt` after rebuild. | **PASS** |
| **TC-11** | Result Limit Validation | Limit input `"-3"` or `"abc"` | Rejects negative or non-numeric limit inputs with validation message. | Rejected invalid limits and defaulted to 10 for standard usage. | **PASS** |
| **TC-12** | Unsupported File Format Handling | `document.pdf`, `image.png` | Safely ignores binary or unsupported file extensions during scanning. | Indexed 4 `.txt` files and ignored `.pdf` and `.png` without crashing. | **PASS** |
| **TC-13** | Corrupted JSON Persistence Handling | Malformed JSON in `storage/index.json` | Catches `JSONDecodeError` cleanly without crashing application. | Returned `(False, "Index file is corrupted or unreadable: ...")`. | **PASS** |
| **TC-14** | Missing Index File Handling | Attempt load from empty folder | Catches missing storage files cleanly and prompts user to index documents. | Returned `(False, "No saved index found. Please index documents first.")`. | **PASS** |

---

## 🏃 Running Automated Tests

To re-run the complete test suite:

```bash
python -m pytest -v
```

Output verification:
```text
tests/test_search_engine.py::test_normal_single_keyword_search PASSED    [  7%]
tests/test_search_engine.py::test_multiple_keyword_search PASSED         [ 14%]
tests/test_search_engine.py::test_no_results_search PASSED               [ 21%]
tests/test_search_engine.py::test_empty_query_validation PASSED          [ 28%]
tests/test_search_engine.py::test_invalid_folder_validation PASSED       [ 35%]
tests/test_search_engine.py::test_case_insensitive_search PASSED         [ 42%]
tests/test_search_engine.py::test_empty_document_handling PASSED         [ 50%]
tests/test_search_engine.py::test_reindexing_idempotency PASSED          [ 57%]
tests/test_search_engine.py::test_persistence_save_load PASSED           [ 64%]
tests/test_search_engine.py::test_rebuild_index PASSED                   [ 71%]
tests/test_search_engine.py::test_result_limit_validation PASSED         [ 78%]
tests/test_search_engine.py::test_unsupported_file_format_ignored PASSED [ 85%]
tests/test_search_engine.py::test_corrupted_json_handling PASSED         [ 92%]
tests/test_search_engine.py::test_missing_index_file_handling PASSED     [100%]

============================= 14 passed in 0.20s ==============================
```
