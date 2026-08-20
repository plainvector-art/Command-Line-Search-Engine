"""
JSON-based persistence manager for saving, loading, and rebuilding search engine indexes.
"""

import json
import os
from typing import Dict, Any, Tuple
from src.indexer import DocumentIndexer
from src.models import Document, CorpusStats


class IndexStorage:
    """
    Manages persistence of inverted index and metadata using local JSON storage.
    """

    INDEX_FILENAME = "index.json"
    METADATA_FILENAME = "metadata.json"

    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = storage_dir

    def _ensure_storage_dir(self):
        """Ensures the storage directory exists."""
        os.makedirs(self.storage_dir, exist_ok=True)

    def get_index_file_path(self) -> str:
        return os.path.join(self.storage_dir, self.INDEX_FILENAME)

    def get_metadata_file_path(self) -> str:
        return os.path.join(self.storage_dir, self.METADATA_FILENAME)

    def save(self, indexer: DocumentIndexer, folder_path: str = "") -> bool:
        """
        Saves current inverted index and document metadata to JSON files.
        """
        try:
            self._ensure_storage_dir()
            
            # Serialize inverted index
            index_path = self.get_index_file_path()
            serializable_index = {
                term: dict(postings)
                for term, postings in indexer.inverted_index.items()
            }
            with open(index_path, "w", encoding="utf-8") as f:
                json.dump(serializable_index, f, indent=2)

            # Serialize document metadata
            metadata_path = self.get_metadata_file_path()
            serializable_metadata = {
                "folder_path": folder_path,
                "documents": {
                    doc_id: doc_obj.to_dict()
                    for doc_id, doc_obj in indexer.documents.items()
                },
                "document_lines": indexer.document_lines
            }
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(serializable_metadata, f, indent=2)

            return True
        except (OSError, IOError, TypeError) as e:
            raise IOError(f"Failed to save index to '{self.storage_dir}': {str(e)}")

    def load(self, indexer: DocumentIndexer) -> Tuple[bool, str]:
        """
        Loads index and metadata into the provided indexer.
        Returns (success: bool, status_message: str).
        """
        index_path = self.get_index_file_path()
        metadata_path = self.get_metadata_file_path()

        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
            return False, "No saved index found. Please index documents first."

        try:
            with open(index_path, "r", encoding="utf-8") as f:
                loaded_index = json.load(f)

            with open(metadata_path, "r", encoding="utf-8") as f:
                loaded_metadata = json.load(f)

            # Reconstruct indexer state
            indexer.inverted_index.clear()
            for term, postings in loaded_index.items():
                for doc_id, lines in postings.items():
                    indexer.inverted_index[term][doc_id] = lines

            indexer.documents.clear()
            raw_docs = loaded_metadata.get("documents", {})
            for doc_id, doc_data in raw_docs.items():
                indexer.documents[doc_id] = Document.from_dict(doc_data)

            indexer.document_lines = loaded_metadata.get("document_lines", {})
            indexed_folder = loaded_metadata.get("folder_path", "")

            return True, f"Successfully loaded index with {len(indexer.documents)} documents."

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            return False, f"Index file is corrupted or unreadable: {str(e)}"
        except OSError as e:
            return False, f"Failed to read index file: {str(e)}"

    def rebuild(self, indexer: DocumentIndexer, folder_path: str) -> Tuple[int, str]:
        """
        Rebuilds the index from scratch by rescanning folder_path and saving.
        """
        count, warnings = indexer.index_directory(folder_path)
        self.save(indexer, folder_path=folder_path)
        warning_msg = f" ({len(warnings)} warnings)" if warnings else ""
        return count, f"Index successfully rebuilt for '{folder_path}' with {count} documents{warning_msg}."

    def get_corpus_stats(self, indexer: DocumentIndexer, folder_path: str = "") -> CorpusStats:
        """
        Calculates and returns CorpusStats object.
        """
        index_size = 0
        index_path = self.get_index_file_path()
        metadata_path = self.get_metadata_file_path()
        if os.path.exists(index_path):
            index_size += os.path.getsize(index_path)
        if os.path.exists(metadata_path):
            index_size += os.path.getsize(metadata_path)

        return CorpusStats(
            total_documents=indexer.get_document_count(),
            unique_terms=indexer.get_unique_term_count(),
            total_words=indexer.get_total_word_count(),
            avg_document_length=indexer.get_average_document_length(),
            index_size_bytes=index_size,
            indexed_directory=folder_path or "In-memory corpus"
        )
