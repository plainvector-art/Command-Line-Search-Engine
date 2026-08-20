# LocalSearch — Python Keyword Search Engine

A lightweight, offline Python search engine that indexes local text documents, builds an inverted index, calculates term frequency-inverse document frequency (TF-IDF) relevance scores, and ranks search results with context snippets.

---

## 📌 Problem Statement (Academic Project #33)

> **Problem:** Index local text files and rank documents for keyword queries.  
> **Expected Result:** A searchable local corpus with ranked documents.

---

## 🎯 Objective

**LocalSearch** provides a complete, modular, and defensible offline search solution built entirely using core Python principles, data structures, and open-source libraries. It solves the inefficiency of linear full-text scans by constructing an inverted index and applying mathematical TF-IDF relevance ranking to return the most pertinent text documents for single and multi-keyword queries.

---

## ✨ Features

- **Robust Inverted Indexing**: Scans `.txt` files, normalizes case, removes punctuation, and maps unique terms to document occurrences and line positions.
- **Explainable TF-IDF Ranking**: Uses a smoothed Inverse Document Frequency formula ($\text{IDF} = \log_{10}\left(\frac{N + 1}{\text{df} + 1}\right) + 1.0$) combined with Term Frequency ($\text{TF} = \frac{\text{count}}{\text{total\_words}}$) to rank search results logically.
- **Context Snippets**: Extracts contextual lines surrounding matched query terms.
- **JSON Index Persistence**: Saves and loads index state locally (`storage/index.json` and `metadata.json`), enabling instant search startup without re-indexing.
- **Idempotency & Duplicate Safety**: Re-indexing directories replaces old state cleanly, preventing duplicate or corrupted entries.
- **Comprehensive Validation**: Gracefully handles missing directories, empty queries, invalid inputs, and malformed files without crashing.
- **Corpus Statistics**: Calculates total document count, unique vocabulary size, total word count, average document length, and storage size.
- **Dual Interface**: Includes an interactive CLI menu (`main.py`) and an optional Streamlit Web UI (`app.py`).
- **100% Offline & Open-Source**: Zero paid APIs, zero external network requests.

---

## 🛠️ Technologies Used

- **Python 3.9+** (Standard Library: `os`, `re`, `json`, `math`, `collections`, `dataclasses`)
- **Pytest 8.4.2** (Automated unit testing suite)
- **Streamlit 1.47.1** (Optional web interface)
- **Pandas 2.3.3** (Tabular result formatting in Web UI)

---

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anwitarajendra/Command-Line-Search-Engine.git
   cd Command-Line-Search-Engine
   ```

2. **Create and activate a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 Running the Application

### 1. Interactive Command Line Interface (Core CLI)

Launch the interactive CLI menu:
```bash
python main.py
```
*(On Windows systems with Python launcher: `py -3 main.py`)*

#### Interactive Menu Options:
```text
==================================================
      LocalSearch — Python Keyword Search Engine
==================================================

1. Index Documents
2. Search Documents
3. View Index Statistics
4. Load Saved Index
5. Rebuild Index
6. Exit

Select an option (1-6):
```

### 2. Optional Streamlit Web Interface (GUI)

Launch the web GUI in your browser:
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
Command-Line-Search-Engine/
├── main.py                     # Primary CLI Interactive Entrypoint
├── app.py                      # Optional Streamlit GUI Interface
├── requirements.txt            # Python Package Dependencies
├── LICENSE                     # MIT Open-Source License
├── README.md                   # Project Documentation
├── PROJECT_REPORT.md           # 18-Section Technical Academic Report
├── TEST_CASES.md               # Automated & Manual Test Cases Table
├── DEMO_GUIDE.md               # Step-by-Step Demonstration Guide
│
├── src/                        # Core Engine Modular Package
│   ├── __init__.py
│   ├── models.py               # Document, SearchResult & CorpusStats Dataclasses
│   ├── tokenizer.py            # Case Normalization, Tokenization & Line Tracking
│   ├── indexer.py              # Inverted Indexing & Directory Scanner
│   ├── search_engine.py       # TF-IDF Calculation, Ranking & Snippet Generation
│   ├── storage.py              # JSON Index Persistence (Save/Load/Rebuild)
│   └── utils.py                # Input Validation & Formatting Helpers
│
├── data/
│   └── documents/              # Sample Educational Corpus
│       ├── python.txt
│       ├── machine_learning.txt
│       ├── artificial_intelligence.txt
│       ├── web_development.txt
│       └── databases.txt
│
├── storage/
│   ├── index.json              # Serialized Inverted Index
│   └── metadata.json           # Corpus & Document Metadata
│
├── tests/
│   └── test_search_engine.py   # Pytest Automated Test Suite (11 Test Cases)
│
└── screenshots/
    └── README.md               # Screenshots Directory & Guide
```

---

## ⚙️ How It Works

```text
Text Documents (.txt)
        │
        ▼
   Tokenization  ──► Normalization, Punctuation Stripping & Line Tracking
        │
        ▼
 Inverted Index  ──► Term ──► { Document: [Line Numbers] }
        │
        ▼
 Persistence Layer ──► Save / Load via storage/index.json
        │
        ▼
 Query Processing ──► Multi-keyword Tokenization & Term Filtering
        │
        ▼
 TF-IDF Scoring  ──► TF = count / total_words
                     IDF = log10((N+1)/(df+1)) + 1.0
                     Score = Σ (TF × IDF)
        │
        ▼
Ranked Output   ──► Sort descending, extract snippets, format CLI/GUI
```

---

## 🧪 Testing & Verification

Automated test cases are implemented using `pytest`.

Run all unit tests:
```bash
pytest -v
```

### Test Coverage Highlights:
- ✅ Single keyword search & multi-keyword ranking
- ✅ Case insensitivity (`Python` == `python` == `PYTHON`)
- ✅ No results handling & empty query validation
- ✅ Invalid directory path validation
- ✅ Empty text file indexing
- ✅ Idempotent re-indexing without duplicate postings
- ✅ JSON persistence save, load, and rebuild integrity

---

## ⚠️ Limitations

1. **File Format Support**: Only processes plain text files (`.txt`). PDF or DOCX parsing is not included out of the box.
2. **Exact Term Matching**: Uses standard tokenization without stemming (e.g., `running` and `run` are indexed as separate terms).
3. **In-Memory Query Processing**: The inverted index is loaded into RAM for fast search execution.

---

## 🔮 Future Improvements

- **Porter Stemming / Lemmatization**: Group word variants to improve recall.
- **Boolean Search Operators**: Support `AND`, `OR`, `NOT` logical queries.
- **PDF & Markdown Parser**: Expand document reader to extract text from `.pdf` and `.md` files.
- **Phrase Search**: Support exact phrase matching using positional postings.
