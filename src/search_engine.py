"""
Search engine implementation providing TF-IDF calculation, relevance ranking, and snippet generation.
"""

import math
from collections import defaultdict
from typing import List, Dict, Set
from src.indexer import DocumentIndexer
from src.models import SearchResult
from src.tokenizer import tokenize


class SearchEngine:
    """
    Search engine that evaluates keyword queries over an inverted index
    using smoothed TF-IDF ranking.
    """

    def __init__(self, indexer: DocumentIndexer):
        self.indexer = indexer

    def calculate_idf(self, term: str) -> float:
        """
        Calculates smoothed Inverse Document Frequency (IDF).
        Formula: log10((N + 1) / (df + 1)) + 1
        Where N = total documents, df = document frequency for term.
        """
        total_docs = self.indexer.get_document_count()
        if total_docs == 0:
            return 0.0

        postings = self.indexer.inverted_index.get(term, {})
        doc_freq = len(postings)

        # Smoothed IDF formula preventing zero division or negative values
        idf = math.log10((total_docs + 1) / (doc_freq + 1)) + 1.0
        return idf

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """
        Searches the indexed corpus for matching keywords.
        Returns ranked list of SearchResult objects sorted by TF-IDF score descending.
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty or blank.")

        query_terms = tokenize(query)
        if not query_terms:
            return []

        doc_scores: Dict[str, float] = defaultdict(float)
        matched_terms_per_doc: Dict[str, Set[str]] = defaultdict(set)
        occurrences_per_doc: Dict[str, int] = defaultdict(int)

        for term in query_terms:
            if term in self.indexer.inverted_index:
                idf = self.calculate_idf(term)
                postings = self.indexer.inverted_index[term]

                for doc_id, line_numbers in postings.items():
                    doc_obj = self.indexer.documents.get(doc_id)
                    if not doc_obj or doc_obj.word_count == 0:
                        continue

                    # Term Frequency = term count in document / total words in document
                    tf = len(line_numbers) / doc_obj.word_count
                    tf_idf = tf * idf

                    doc_scores[doc_id] += tf_idf
                    matched_terms_per_doc[doc_id].add(term)
                    occurrences_per_doc[doc_id] += len(line_numbers)

        if not doc_scores:
            return []

        # Sort results from highest relevance score to lowest
        sorted_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)

        results: List[SearchResult] = []
        rank = 1

        for doc_id, score in sorted_docs[:limit]:
            matched_terms = sorted(list(matched_terms_per_doc[doc_id]))
            occurrences = occurrences_per_doc[doc_id]
            snippet = self._generate_snippet(doc_id, matched_terms)

            result = SearchResult(
                rank=rank,
                filename=doc_id,
                score=score,
                matched_terms=matched_terms,
                occurrences=occurrences,
                snippet=snippet
            )
            results.append(result)
            rank += 1

        return results

    def _generate_snippet(self, doc_id: str, matched_terms: List[str]) -> str:
        """
        Extracts a clean snippet from the document lines containing matched terms.
        """
        lines = self.indexer.document_lines.get(doc_id, [])
        if not lines:
            return "No content preview available."

        # Find the first line containing any matched term
        for line in lines:
            line_lower = line.lower()
            if any(term in line_lower for term in matched_terms):
                cleaned_line = line.strip()
                if len(cleaned_line) > 120:
                    return f'"{cleaned_line[:117]}..."'
                return f'"{cleaned_line}"'

        # Fallback to first non-empty line
        for line in lines:
            if line.strip():
                cleaned_line = line.strip()
                if len(cleaned_line) > 120:
                    return f'"{cleaned_line[:117]}..."'
                return f'"{cleaned_line}"'

        return "No text available."
