"""
Automated unit tests for LocalSearch Keyword Search Engine.
Covers indexing, searching, ranking, validation, persistence, and edge cases.
"""

import os
import shutil
import tempfile
import pytest

from src.indexer import DocumentIndexer
from src.search_engine import SearchEngine
from src.storage import IndexStorage
from src.utils import (
    validate_directory_path,
    validate_search_query,
    validate_result_limit,
)


@pytest.fixture
def temp_corpus_dir():
    """Creates a temporary corpus directory populated with test text files."""
    temp_dir = tempfile.mkdtemp()

    files = {
        "python.txt": "Python is a popular programming language used for machine learning and web development.",
        "machine_learning.txt": "Machine learning algorithms discover patterns in data. Python libraries support machine learning.",
        "artificial_intelligence.txt": "Artificial intelligence covers neural networks, computer vision, and robotics.",
        "empty.txt": "",
    }

    for fname, text in files.items():
        with open(os.path.join(temp_dir, fname), "w", encoding="utf-8") as f:
            f.write(text)

    yield temp_dir

    # Cleanup temp directory
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_storage_dir():
    """Creates a temporary directory for persistent JSON storage."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


# Test 1 — Normal single keyword search
def test_normal_single_keyword_search(temp_corpus_dir):
    indexer = DocumentIndexer()
    indexer.index_directory(temp_corpus_dir)
    search_engine = SearchEngine(indexer)

    results = search_engine.search("python")
    assert len(results) > 0
    filenames = [r.filename for r in results]
    assert "python.txt" in filenames
    assert "machine_learning.txt" in filenames


# Test 2 — Multiple keywords search & ranking
def test_multiple_keyword_search(temp_corpus_dir):
    indexer = DocumentIndexer()
    indexer.index_directory(temp_corpus_dir)
    search_engine = SearchEngine(indexer)

    results = search_engine.search("machine learning")
    assert len(results) >= 2
    # Check score ranking order: highest score first
    assert results[0].score >= results[1].score
    assert "machine_learning.txt" in [r.filename for r in results]


# Test 3 — No results search
def test_no_results_search(temp_corpus_dir):
    indexer = DocumentIndexer()
    indexer.index_directory(temp_corpus_dir)
    search_engine = SearchEngine(indexer)

    results = search_engine.search("xyznonexistentterm")
    assert len(results) == 0


# Test 4 — Empty query validation
def test_empty_query_validation(temp_corpus_dir):
    indexer = DocumentIndexer()
    indexer.index_directory(temp_corpus_dir)
    search_engine = SearchEngine(indexer)

    with pytest.raises(ValueError, match="Search query cannot be empty"):
        search_engine.search("")

    with pytest.raises(ValueError, match="Search query cannot be empty"):
        search_engine.search("   ")

    is_valid, err = validate_search_query("")
    assert not is_valid
    assert "empty" in err.lower()


# Test 5 — Invalid folder validation
def test_invalid_folder_validation():
    indexer = DocumentIndexer()

    with pytest.raises(FileNotFoundError):
        indexer.index_directory("/nonexistent/directory/path/12345")

    is_valid, err = validate_directory_path("/nonexistent/directory/path/12345")
    assert not is_valid
    assert "does not exist" in err.lower()


# Test 6 — Case-insensitive search
def test_case_insensitive_search(temp_corpus_dir):
    indexer = DocumentIndexer()
    indexer.index_directory(temp_corpus_dir)
    search_engine = SearchEngine(indexer)

    r_lower = search_engine.search("python")
    r_upper = search_engine.search("PYTHON")
    r_mixed = search_engine.search("PyThOn")

    assert len(r_lower) == len(r_upper) == len(r_mixed)
    assert r_lower[0].filename == r_upper[0].filename == r_mixed[0].filename
    assert pytest.approx(r_lower[0].score, 0.0001) == r_upper[0].score


# Test 7 — Empty document handling
def test_empty_document_handling(temp_corpus_dir):
    indexer = DocumentIndexer()
    count, warnings = indexer.index_directory(temp_corpus_dir)

    # empty.txt should be indexed without crashing
    assert "empty.txt" in indexer.documents
    assert indexer.documents["empty.txt"].word_count == 0
    assert count == 4


# Test 8 — Re-indexing idempotency
def test_reindexing_idempotency(temp_corpus_dir):
    indexer = DocumentIndexer()
    count1, _ = indexer.index_directory(temp_corpus_dir)
    terms_count1 = indexer.get_unique_term_count()

    # Re-index the same directory
    count2, _ = indexer.index_directory(temp_corpus_dir)
    terms_count2 = indexer.get_unique_term_count()

    assert count1 == count2 == 4
    assert terms_count1 == terms_count2


# Test 9 — Persistence save and load
def test_persistence_save_load(temp_corpus_dir, temp_storage_dir):
    indexer1 = DocumentIndexer()
    indexer1.index_directory(temp_corpus_dir)

    storage = IndexStorage(storage_dir=temp_storage_dir)
    saved = storage.save(indexer1, folder_path=temp_corpus_dir)
    assert saved

    # Load into new indexer
    indexer2 = DocumentIndexer()
    loaded, msg = storage.load(indexer2)
    assert loaded
    assert indexer2.get_document_count() == indexer1.get_document_count()

    engine1 = SearchEngine(indexer1)
    engine2 = SearchEngine(indexer2)

    res1 = engine1.search("machine")
    res2 = engine2.search("machine")

    assert len(res1) == len(res2)
    assert res1[0].filename == res2[0].filename
    assert pytest.approx(res1[0].score, 0.0001) == res2[0].score


# Test 10 — Rebuild index with new file content
def test_rebuild_index(temp_corpus_dir, temp_storage_dir):
    indexer = DocumentIndexer()
    storage = IndexStorage(storage_dir=temp_storage_dir)

    count, msg = storage.rebuild(indexer, temp_corpus_dir)
    assert count == 4

    engine = SearchEngine(indexer)
    res_before = engine.search("blockchain")
    assert len(res_before) == 0

    # Add a new file to corpus
    with open(os.path.join(temp_corpus_dir, "crypto.txt"), "w", encoding="utf-8") as f:
        f.write("Blockchain and crypto ledgers use cryptography.")

    count_after, msg_after = storage.rebuild(indexer, temp_corpus_dir)
    assert count_after == 5

    res_after = engine.search("blockchain")
    assert len(res_after) == 1
    assert res_after[0].filename == "crypto.txt"


# Test 11 — Validation helpers
def test_result_limit_validation():
    valid, limit, err = validate_result_limit("5")
    assert valid and limit == 5

    valid, limit, err = validate_result_limit("-3")
    assert not valid
    assert "positive" in err.lower()

    valid, limit, err = validate_result_limit("abc")
    assert not valid
    assert "invalid" in err.lower()
