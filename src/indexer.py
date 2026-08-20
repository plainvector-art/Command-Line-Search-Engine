"""
Document indexer for scanning text files and building inverted index.
"""

import os

from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from src.models import Document
from src.tokenizer import tokenize, tokenize_lines


class DocumentIndexer:
    """
    Scans a directory of text documents and constructs an inverted index
    mapping terms to document occurrences and line positions.
    """

    def __init__(self, supported_extension: str = ".txt"):
        self.supported_extension = supported_extension.lower()
        self.inverted_index: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: defaultdict(list))
        self.documents: Dict[str, Document] = {}
        self.document_lines: Dict[str, List[str]] = {}
        self.term_frequencies: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def scan_directory(self, folder_path: str) -> List[str]:
        """
        Validates folder path and returns a list of supported text file paths.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Directory '{folder_path}' does not exist.")
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"Path '{folder_path}' is not a directory.")

        valid_files = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.lower().endswith(self.supported_extension):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    valid_files.append(full_path)
        return valid_files

    def index_directory(self, folder_path: str) -> Tuple[int, List[str]]:
        """
        Indexes all valid documents in the specified directory.
        Clears existing in-memory index to ensure idempotency.
        Returns total documents indexed and a list of warning/error messages.
        """
        file_paths = self.scan_directory(folder_path)
        
        # Reset internal index state for clean idempotency
        self.inverted_index = defaultdict(lambda: defaultdict(list))
        self.documents = {}
        self.document_lines = {}
        self.term_frequencies = defaultdict(lambda: defaultdict(int))

        warnings: List[str] = []
        indexed_count = 0

        for file_path in file_paths:
            filename = os.path.basename(file_path)
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                
                lines = content.splitlines()
                self.document_lines[filename] = lines
                
                words = tokenize(content)
                word_count = len(words)
                char_count = len(content)
                line_count = len(lines)

                # Store document metadata
                doc_obj = Document(
                    doc_id=filename,
                    filename=filename,
                    filepath=os.path.abspath(file_path),
                    word_count=word_count,
                    char_count=char_count,
                    line_count=line_count
                )
                self.documents[filename] = doc_obj

                # Tokenize lines for line position tracking
                tokens_with_pos = tokenize_lines(lines)
                for word, line_num, _ in tokens_with_pos:
                    self.inverted_index[word][filename].append(line_num)
                    self.term_frequencies[word][filename] += 1

                indexed_count += 1

            except Exception as e:
                warnings.append(f"Skipped '{filename}': {str(e)}")

        return indexed_count, warnings

    def get_document_count(self) -> int:
        return len(self.documents)

    def get_unique_term_count(self) -> int:
        return len(self.inverted_index)

    def get_total_word_count(self) -> int:
        return sum(doc.word_count for doc in self.documents.values())

    def get_average_document_length(self) -> float:
        if not self.documents:
            return 0.0
        return self.get_total_word_count() / len(self.documents)
