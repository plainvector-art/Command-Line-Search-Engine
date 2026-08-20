"""
Text processing and tokenization utilities.
"""

import re
import string
from typing import List, Tuple, Dict


def normalize_text(text: str) -> str:
    """
    Normalizes text by converting to lowercase and stripping punctuation.
    """
    if not text:
        return ""
    # Strip punctuation using maketrans for high efficiency
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator).lower()


def tokenize(text: str) -> List[str]:
    """
    Tokenizes raw text into a list of normalized words.
    Ignores punctuation and whitespace.
    """
    if not text:
        return []
    # Extract alphanumeric word tokens
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    return words


def tokenize_lines(lines: List[str]) -> List[Tuple[str, int, int]]:
    """
    Tokenizes lines of text, tracking (word, line_number (1-indexed), word_position).
    Useful for extracting snippets and location tracking.
    """
    tokens = []
    global_pos = 0
    for line_idx, line in enumerate(lines, start=1):
        words = re.findall(r'\b[a-zA-Z0-9]+\b', line.lower())
        for word in words:
            tokens.append((word, line_idx, global_pos))
            global_pos += 1
    return tokens
