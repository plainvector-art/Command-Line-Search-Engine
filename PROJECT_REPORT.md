# Academic Project Report

## Project Title: LocalSearch — Python Keyword Search Engine
**Academic Challenge:** Project #33 — Keyword Search Engine  
**Author:** Devansh  
**Domain:** Information Retrieval, Natural Language Processing, Software Architecture  

---

## 1. Introduction

As digital text repositories expand, efficient information retrieval becomes a fundamental necessity. Scanning raw text files linearly for specific keywords is computationally expensive and scales poorly as document count increases ($O(N \cdot M)$ complexity). A search engine addresses this challenge by pre-processing raw text documents into an **inverted index** data structure, reducing query lookup time from linear file scans to near-instantaneous key-value lookups ($O(K)$ complexity).

**LocalSearch** is an offline, modular Python application designed to index local text documents, compute term statistics, score relevance using Term Frequency-Inverse Document Frequency (TF-IDF), rank search results logically, and persist index structures locally using standard JSON formatting.

---

## 2. Problem Understanding

Academic Project #33 asks for the implementation of a **Keyword Search Engine** capable of:
1. Indexing local text files (`.txt`).
2. Ranking documents based on relevance to user keyword queries.
3. Operating over a local corpus with clear result visualization.

The baseline starting repository contained a minimal Streamlit prototype (`app.py`) without modular separation, missing a CLI interface, lacking persistent index storage, missing input validation, omitting automated tests, and without context snippet extraction.

---

## 3. Objective

The objective of this project is to build a submission-ready Python keyword search engine that:
- Implements modular clean architecture in `src/`.
- Constructs an efficient inverted index with document metadata and line-level term tracking.
- Implements mathematically sound, explainable TF-IDF relevance scoring.
- Provides a robust CLI menu (`main.py`) alongside an optional Streamlit Web UI (`app.py`).
- Supports local index persistence (Save, Load, Rebuild) using JSON storage.
- Handles bad inputs, missing files, and corrupted datasets gracefully.
- Includes comprehensive unit tests (`pytest`) and technical documentation.

---

## 4. Proposed Approach

To fulfill these objectives, **LocalSearch** uses a pipeline architecture:
1. **Ingestion & Validation**: Scan target folder, validate path existence, verify `.txt` file extensions, and safely read text using UTF-8 encoding.
2. **Tokenization & Normalization**: Convert raw text to lowercase, strip punctuation via Python's efficient `str.maketrans`, and tokenize words into alphanumeric sequences.
3. **Inverted Indexing**: Map each unique word to a dictionary of document filenames and their corresponding line occurrences.
4. **TF-IDF Relevance Scoring**: Apply term frequency normalization ($\text{TF} = \frac{\text{count}}{\text{total\_words}}$) and smoothed inverse document frequency ($\text{IDF} = \log_{10}\left(\frac{N+1}{\text{df}+1}\right) + 1.0$) to calculate document-query match scores.
5. **Persistence**: Serialize inverted index and document metadata to `storage/index.json` and `storage/metadata.json`.
6. **Presentation**: Display ranked documents with score, matched terms, total occurrence count, and context snippets in both CLI and GUI interfaces.

---

## 5. System Architecture

The project follows Object-Oriented Programming (OOP) principles with decoupled responsibilities:

```text
+-----------------------------------------------------------------------+
|                          User Interfaces                              |
|             main.py (CLI Menu)    |    app.py (Streamlit GUI)         |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                           Core Package (src/)                         |
|                                                                       |
|  +-------------------+  +-------------------+  +-------------------+  |
|  |    utils.py       |  |   tokenizer.py    |  |    models.py      |  |
|  |  Path & Query     |  |  Normalization    |  | Document, Result  |  |
|  |  Validation       |  |  & Tokenization   |  | & Stats Dataclass |  |
|  +-------------------+  +-------------------+  +-------------------+  |
|            |                      |                      |            |
|            +----------------------+----------------------+            |
|                                   |                                   |
|                                   v                                   |
|                         +-------------------+                         |
|                         |    indexer.py     |                         |
|                         |  Inverted Index & |                         |
|                         |  Corpus Scanner   |                         |
|                         +-------------------+                         |
|                                   |                                   |
|           +-----------------------+-----------------------+           |
|           |                                               |           |
|           v                                               v           |
| +-------------------+                           +-------------------+ |
| | search_engine.py  |                           |    storage.py     | |
| |  TF-IDF Ranking   |                           | JSON Save / Load  | |
| |  & Snippet Gen    |                           |  & Index Rebuild  | |
| +-------------------+                           +-------------------+ |
+-----------------------------------------------------------------------+
                                                            |
                                                            v
                                                  +-------------------+
                                                  |   storage/*.json  |
                                                  | Local Disk Storage|
                                                  +-------------------+
```

---

## 6. Data Structures

1. **Inverted Index (`Dict[str, Dict[str, List[int]]]`)**:
   - Primary data structure mapping a normalized word to a dictionary of document names and line numbers.
   - Example:
     ```python
     {
       "python": {
         "python.txt": [1, 3, 5],
         "machine_learning.txt": [2]
       }
     }
     ```
2. **Document Metadata (`Dict[str, Document]`)**:
   - Stores filename, absolute path, total word count, character count, and line count for each document.
3. **Term Frequency Map (`Dict[str, Dict[str, int]]`)**:
   - Stores the exact frequency of occurrence of term $t$ in document $d$.
4. **Document Lines Cache (`Dict[str, List[str]]`)**:
   - Caches raw document text split into lines for fast snippet extraction without re-reading files from disk.

---

## 7. Algorithms

### 7.1 Inverted Index Construction Algorithm
1. Scan specified directory for `.txt` files.
2. For each file, read raw content with UTF-8 encoding.
3. Tokenize lines into `(word, line_number)` pairs.
4. Insert `line_number` into `inverted_index[word][filename]`.
5. Compute aggregate word count, character count, and line count.

### 7.2 Snippet Extraction Algorithm
1. Retrieve document lines from `document_lines[filename]`.
2. Iterate through lines to find the first line containing any matched query term.
3. Strip leading/trailing whitespace and truncate to 120 characters if necessary.
4. Surround snippet with quote marks for clean presentation.

---

## 8. Implementation

The implementation uses standard Python standard library utilities:
- `dataclasses.dataclass` for formal data structures (`Document`, `SearchResult`, `CorpusStats`).
- `collections.defaultdict` for nested dictionary manipulation without key existence checks.
- `re.findall(r'\b[a-zA-Z0-9]+\b', text)` for word extraction.
- `json.dump()` and `json.load()` for clean JSON serialization.

---

## 9. Search and Ranking Method

The relevance of document $d$ for query terms $Q = \{t_1, t_2, \dots, t_k\}$ is calculated using **TF-IDF**:

$$\text{Score}(d, Q) = \sum_{t \in Q} \text{TF}(t, d) \times \text{IDF}(t)$$

### Term Frequency (TF)
$$\text{TF}(t, d) = \frac{\text{Count of } t \text{ in } d}{\text{Total Words in } d}$$

### Smoothed Inverse Document Frequency (IDF)
$$\text{IDF}(t) = \log_{10}\left(\frac{N + 1}{\text{df}(t) + 1}\right) + 1.0$$
*Where:*
- $N$ = Total documents in corpus
- $\text{df}(t)$ = Number of documents containing term $t$

*Why Smoothed IDF?*
Standard IDF ($\log \frac{N}{\text{df}}$) becomes 0 when a word appears in all documents ($\text{df}=N$) or causes division by zero if $\text{df}=0$. Adding $1$ to numerator and denominator ensures smooth scaling and non-zero positive weights.

---

## 10. Persistence

The index is stored in JSON format inside the `storage/` directory:
- `storage/index.json`: Serialized inverted index dictionary.
- `storage/metadata.json`: Document properties, word counts, and line cache.

### Persistence Features:
- **Save**: Saves in-memory index to disk after indexing.
- **Auto-Load**: Automatically loads index at application startup.
- **Rebuild**: Clears existing index, rescans folder, and updates JSON files atomically.

---

## 11. Input Validation

The system strictly validates user input:
1. **Folder Path**: Verified using `os.path.exists()` and `os.path.isdir()`. Empty strings or invalid paths are rejected with clear user error messages.
2. **Search Query**: Rejects empty strings and whitespace-only queries (`ValueError`).
3. **Result Limit**: Converts input to integer, ensuring value is positive and within range $[1, 100]$.

---

## 12. Exception Handling

All realistic runtime errors are handled using targeted `try/except` blocks:
- `FileNotFoundError` & `NotADirectoryError`: Triggers clear path guidance.
- `UnicodeDecodeError` & `OSError`: Handles unreadable or corrupted text files gracefully.
- `json.JSONDecodeError`: Catches corrupted index files during load and suggests rebuilding.

---

## 13. Testing

The application includes 14 automated unit tests written for `pytest`:

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

---

## 14. Challenges Encountered

1. **IDF Division by Zero & Log Zero**: Standard IDF formulas fail when term frequency equals total documents or when zero documents match.
2. **Context Snippet Alignment**: Extracting meaningful snippets without loading full file contents repeatedly from disk.
3. **Windows CLI Path Aliasing**: Python executable detection variances across Windows PowerShell environments.

---

## 15. Solutions Implemented

1. Implemented smoothed IDF ($\log_{10}\frac{N+1}{\text{df}+1} + 1.0$) to guarantee non-zero, stable scores.
2. Cached document line arrays during the indexing phase to allow fast $O(L)$ line lookup for snippet generation.
3. Structured `main.py` entrypoint with standard `sys.path` resolution for cross-platform execution.

---

## 16. Limitations

- Support is restricted to plain `.txt` files.
- Term matching requires exact word matches (no stemming or fuzzy spelling correction out of the box).
- Inverted index is held in RAM during active application execution.

---

## 17. Future Scope

- Integration of Porter Stemmer to group term variations (`run`, `running`, `runner`).
- Support for positional phrase queries (e.g. `"machine learning"` exact sequence match).
- Document parser extensions for `.pdf`, `.md`, and `.docx` file formats.

---

## 18. Conclusion

**LocalSearch** successfully transforms the initial codebase into a submission-ready, offline Python keyword search engine. It demonstrates clean modular software architecture, data structure design, mathematical relevance scoring, persistent storage, input validation, robust error handling, automated testing, real PNG screenshot evidence, and comprehensive technical documentation.
