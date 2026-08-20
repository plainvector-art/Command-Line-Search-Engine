"""
Data models for LocalSearch Keyword Search Engine.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Document:
    """Represents an indexed document."""
    doc_id: str
    filename: str
    filepath: str
    word_count: int
    char_count: int
    line_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "filename": self.filename,
            "filepath": self.filepath,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "line_count": self.line_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        return cls(
            doc_id=data["doc_id"],
            filename=data["filename"],
            filepath=data.get("filepath", ""),
            word_count=data.get("word_count", 0),
            char_count=data.get("char_count", 0),
            line_count=data.get("line_count", 0),
        )


@dataclass
class SearchResult:
    """Represents a single ranked search result."""
    rank: int
    filename: str
    score: float
    matched_terms: List[str]
    occurrences: int
    snippet: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rank": self.rank,
            "filename": self.filename,
            "score": round(self.score, 4),
            "matched_terms": self.matched_terms,
            "occurrences": self.occurrences,
            "snippet": self.snippet,
        }


@dataclass
class CorpusStats:
    """Represents summary statistics for an indexed corpus."""
    total_documents: int
    unique_terms: int
    total_words: int
    avg_document_length: float
    index_size_bytes: int
    indexed_directory: str

    def format_summary(self) -> str:
        size_kb = self.index_size_bytes / 1024.0
        return (
            "Corpus Statistics\n"
            "==============================\n"
            f"Indexed Directory:  {self.indexed_directory}\n"
            f"Documents Indexed:  {self.total_documents}\n"
            f"Unique Terms:       {self.unique_terms:,}\n"
            f"Total Words:        {self.total_words:,}\n"
            f"Average Doc Length: {self.avg_document_length:.1f} words\n"
            f"Index Size:         {size_kb:.2f} KB\n"
        )
