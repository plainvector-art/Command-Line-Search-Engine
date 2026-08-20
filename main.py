"""
LocalSearch — Python Keyword Search Engine
Command Line Interface (CLI) Entrypoint
"""

import sys
import os

# Add local root to sys.path to enable smooth module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.indexer import DocumentIndexer
from src.search_engine import SearchEngine
from src.storage import IndexStorage
from src.utils import (
    validate_directory_path,
    validate_search_query,
    validate_result_limit,
)


def print_banner():
    print("\n" + "=" * 50)
    print("      LocalSearch — Python Keyword Search Engine")
    print("=" * 50)


def print_menu():
    print("\n1. Index Documents")
    print("2. Search Documents")
    print("3. View Index Statistics")
    print("4. Load Saved Index")
    print("5. Rebuild Index")
    print("6. Exit")


def main():
    indexer = DocumentIndexer()
    search_engine = SearchEngine(indexer)
    storage = IndexStorage()
    current_folder = "data/documents"

    # Attempt to load previously saved index at startup
    success, msg = storage.load(indexer)
    if success:
        print(f"\n[System Status]: Auto-loaded existing index ({indexer.get_document_count()} documents).")

    while True:
        print_banner()
        print_menu()

        try:
            choice = input("\nSelect an option (1-6): ").strip()

            if choice == "1":
                # Option 1: Index Documents
                print("\n--- Index Documents ---")
                folder_input = input(f"Enter folder path [default: '{current_folder}']: ").strip()
                target_folder = folder_input if folder_input else current_folder

                is_valid, err_msg = validate_directory_path(target_folder)
                if not is_valid:
                    print(f"\n{err_msg}")
                    continue

                try:
                    count, warnings = indexer.index_directory(target_folder)
                    current_folder = target_folder
                    storage.save(indexer, folder_path=target_folder)
                    print(f"\n[Success]: Successfully indexed {count} document(s) from '{target_folder}'.")
                    print("[Status]: Index automatically saved to local storage.")
                    if warnings:
                        print("\n[Warnings]:")
                        for w in warnings:
                            print(f" - {w}")
                except Exception as e:
                    print(f"\nError indexing directory: {str(e)}")

            elif choice == "2":
                # Option 2: Search Documents
                print("\n--- Search Documents ---")
                if indexer.get_document_count() == 0:
                    print("Error: No documents currently indexed. Please index documents (Option 1) or load index (Option 4).")
                    continue

                query = input("Enter search query: ").strip()
                is_valid, err_msg = validate_search_query(query)
                if not is_valid:
                    print(f"\n{err_msg}")
                    continue

                limit_input = input("Result limit [default 10]: ").strip()
                is_valid_limit, limit_val, limit_err = validate_result_limit(limit_input)
                if not is_valid_limit:
                    print(f"\n{limit_err}")
                    continue

                try:
                    results = search_engine.search(query, limit=limit_val)
                    if not results:
                        print(f"\nNo matching documents found for query: '{query}'")
                    else:
                        print(f"\nSearch Results for: '{query}' (Top {len(results)})")
                        print("=" * 50)
                        for res in results:
                            print(f"#{res.rank} {res.filename}")
                            print(f"   Score:        {res.score:.4f}")
                            print(f"   Matched terms: {', '.join(res.matched_terms)}")
                            print(f"   Occurrences:  {res.occurrences}")
                            print(f"   Snippet:      {res.snippet}")
                            print("-" * 50)
                except Exception as e:
                    print(f"\nError executing search query: {str(e)}")

            elif choice == "3":
                # Option 3: View Index Statistics
                print("\n--- Corpus & Index Statistics ---")
                if indexer.get_document_count() == 0:
                    print("No active index loaded. Statistics unavailable.")
                else:
                    stats = storage.get_corpus_stats(indexer, folder_path=current_folder)
                    print(stats.format_summary())

            elif choice == "4":
                # Option 4: Load Saved Index
                print("\n--- Load Saved Index ---")
                success, msg = storage.load(indexer)
                if success:
                    print(f"\n[Success]: {msg}")
                else:
                    print(f"\n[Notice]: {msg}")

            elif choice == "5":
                # Option 5: Rebuild Index
                print("\n--- Rebuild Index ---")
                folder_input = input(f"Enter folder path to rebuild [default: '{current_folder}']: ").strip()
                target_folder = folder_input if folder_input else current_folder

                is_valid, err_msg = validate_directory_path(target_folder)
                if not is_valid:
                    print(f"\n{err_msg}")
                    continue

                try:
                    count, msg = storage.rebuild(indexer, target_folder)
                    current_folder = target_folder
                    print(f"\n[Success]: {msg}")
                except Exception as e:
                    print(f"\nError rebuilding index: {str(e)}")

            elif choice == "6":
                # Option 6: Exit
                print("\nThank you for using LocalSearch. Goodbye!")
                sys.exit(0)

            else:
                print("\nInvalid selection. Please enter a number between 1 and 6.")

        except KeyboardInterrupt:
            print("\n\nSession terminated by user. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
