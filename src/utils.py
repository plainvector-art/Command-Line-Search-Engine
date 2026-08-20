"""
Validation and formatting utility functions.
"""

import os
from typing import Tuple


def validate_directory_path(path: str) -> Tuple[bool, str]:
    """
    Validates a folder path string.
    Returns (is_valid: bool, error_message: str).
    """
    if not path or not path.strip():
        return False, "Error: Folder path cannot be empty."

    clean_path = path.strip()
    if not os.path.exists(clean_path):
        return False, f"Error: The selected folder '{clean_path}' does not exist."

    if not os.path.isdir(clean_path):
        return False, f"Error: The path '{clean_path}' exists but is not a directory."

    return True, ""


def validate_search_query(query: str) -> Tuple[bool, str]:
    """
    Validates a search query string.
    Returns (is_valid: bool, error_message: str).
    """
    if not query or not query.strip():
        return False, "Error: Search query cannot be empty or contain only whitespace."

    return True, ""


def validate_result_limit(limit_input: str) -> Tuple[bool, int, str]:
    """
    Validates result count limit.
    Returns (is_valid: bool, limit_int: int, error_message: str).
    """
    if not limit_input or not limit_input.strip():
        return True, 10, ""  # Default to 10

    try:
        val = int(limit_input.strip())
        if val <= 0:
            return False, 0, "Error: Result limit must be a positive integer greater than 0."
        if val > 100:
            return False, 0, "Error: Result limit cannot exceed 100."
        return True, val, ""
    except ValueError:
        return False, 0, "Error: Invalid input. Please enter a valid number."
