# Demonstration and Screenshot Guide — LocalSearch

This guide provides step-by-step instructions for capturing demonstration evidence and screenshots of **LocalSearch — Python Keyword Search Engine** for academic evaluation, project reports, or viva presentations.

---

## 📷 Required Demonstration Screenshots

### 1. Main Application Menu
- **Objective**: Demonstrate the interactive CLI banner and main menu system.
- **Steps**:
  1. Open terminal and run `python main.py`.
  2. Capture the main banner and options 1 through 6.
- **Save file as**: `screenshots/01_main_menu.png`

---

### 2. Successful Document Indexing
- **Objective**: Show directory scanning, document loading, and automatic JSON index saving.
- **Steps**:
  1. From main menu, select option `1`.
  2. Press Enter to select default folder `data/documents`.
  3. Observe success message confirming 5 indexed documents.
- **Save file as**: `screenshots/02_document_indexing.png`

---

### 3. Corpus & Index Statistics
- **Objective**: Display corpus metrics (documents indexed, unique vocabulary, total word count, average document length, index size).
- **Steps**:
  1. From main menu, select option `3`.
  2. Capture the statistics table summary.
- **Save file as**: `screenshots/03_index_statistics.png`

---

### 4. Single Keyword Search
- **Objective**: Demonstrate TF-IDF search, ranking, and context snippet extraction for a single term.
- **Steps**:
  1. From main menu, select option `2`.
  2. Enter query `python`.
  3. Observe ranked documents (`python.txt`, `machine_learning.txt`, `web_development.txt`) with scores and snippets.
- **Save file as**: `screenshots/04_single_keyword_search.png`

---

### 5. Multiple-Keyword Ranked Search
- **Objective**: Demonstrate multi-term query processing and aggregated relevance ranking.
- **Steps**:
  1. From main menu, select option `2`.
  2. Enter query `machine learning`.
  3. Observe top-ranked document `machine_learning.txt` with matched terms `machine, learning` and occurrences count.
- **Save file as**: `screenshots/05_multi_keyword_search.png`

---

### 6. No-Result Search
- **Objective**: Verify application response when no matching documents exist.
- **Steps**:
  1. From main menu, select option `2`.
  2. Enter query `quantumxyz`.
  3. Capture clear notice: `No matching documents found for query: 'quantumxyz'`.
- **Save file as**: `screenshots/06_no_result_search.png`

---

### 7. Invalid Input & Error Handling
- **Objective**: Show input validation handling empty query strings, invalid limits, and invalid folder paths.
- **Steps**:
  1. From main menu, select option `2`.
  2. Press Enter with empty input.
  3. Observe validation error: `Error: Search query cannot be empty or contain only whitespace.`.
- **Save file as**: `screenshots/08_error_handling.png`

---

### 8. Persistence & Auto-Load Functionality
- **Objective**: Show index persistence loading previously saved `storage/index.json`.
- **Steps**:
  1. From main menu, select option `4`.
  2. Observe confirmation: `Successfully loaded index with 5 documents.`.
- **Save file as**: `screenshots/07_persistence_load.png`

---

## 🌐 Streamlit GUI Demonstration (Optional)

To demonstrate the optional Web GUI interface:

1. Run command:
   ```bash
   streamlit run app.py
   ```
2. Navigate to `http://localhost:8501`.
3. Capture the web interface showing search inputs, dataframe results, and expandable snippets.
- **Save file as**: `screenshots/09_streamlit_gui.png`
