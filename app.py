"""
LocalSearch — Streamlit Web Interface (Optional GUI)
"""

import os
import sys
import streamlit as st
import pandas as pd

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.indexer import DocumentIndexer
from src.search_engine import SearchEngine
from src.storage import IndexStorage
from src.utils import validate_directory_path, validate_search_query

st.set_page_config(
    page_title="LocalSearch — Keyword Search Engine",
    page_icon="🔍",
    layout="wide"
)

# Initialize Session State objects
if "indexer" not in st.session_state:
    st.session_state.indexer = DocumentIndexer()
    st.session_state.storage = IndexStorage()
    st.session_state.search_engine = SearchEngine(st.session_state.indexer)
    # Attempt auto-load on startup
    st.session_state.storage.load(st.session_state.indexer)

indexer = st.session_state.indexer
search_engine = st.session_state.search_engine
storage = st.session_state.storage

st.title("🔍 LocalSearch — Python Keyword Search Engine")
st.caption("Project #33 — Searchable Local Corpus with TF-IDF Relevance Ranking")

# Sidebar — Configuration & Actions
st.sidebar.header("📁 Index Management")
folder_path = st.sidebar.text_input("Corpus Directory:", "data/documents")

col_btn1, col_btn2 = st.sidebar.columns(2)

if col_btn1.button("Index / Save"):
    is_valid, err_msg = validate_directory_path(folder_path)
    if not is_valid:
        st.sidebar.error(err_msg)
    else:
        with st.spinner("Indexing documents..."):
            count, warnings = indexer.index_directory(folder_path)
            storage.save(indexer, folder_path=folder_path)
            st.sidebar.success(f"Indexed {count} document(s) successfully!")
            if warnings:
                for w in warnings:
                    st.sidebar.warning(w)

if col_btn2.button("Load Index"):
    success, msg = storage.load(indexer)
    if success:
        st.sidebar.success(msg)
    else:
        st.sidebar.error(msg)

if st.sidebar.button("Rebuild Index"):
    is_valid, err_msg = validate_directory_path(folder_path)
    if not is_valid:
        st.sidebar.error(err_msg)
    else:
        with st.spinner("Rebuilding index..."):
            count, msg = storage.rebuild(indexer, folder_path)
            st.sidebar.success(msg)

# Sidebar — Statistics
st.sidebar.markdown("---")
st.sidebar.header("📊 Corpus Statistics")
if indexer.get_document_count() > 0:
    stats = storage.get_corpus_stats(indexer, folder_path=folder_path)
    st.sidebar.metric("Documents Indexed", stats.total_documents)
    st.sidebar.metric("Unique Terms", f"{stats.unique_terms:,}")
    st.sidebar.metric("Total Words", f"{stats.total_words:,}")
    st.sidebar.metric("Avg Document Length", f"{stats.avg_document_length:.1f} words")
    st.sidebar.metric("Index File Size", f"{stats.index_size_bytes / 1024.0:.2f} KB")
else:
    st.sidebar.info("No documents currently indexed.")

# Main Interface — Search Tab
query = st.text_input("Enter Search Query (e.g., 'python machine learning', 'artificial intelligence'):")
limit = st.slider("Max Results:", min_value=1, max_value=20, value=10)

if query:
    is_valid, err_msg = validate_search_query(query)
    if not is_valid:
        st.error(err_msg)
    elif indexer.get_document_count() == 0:
        st.warning("⚠️ No documents currently indexed. Please click 'Index / Save' in the sidebar first.")
    else:
        results = search_engine.search(query, limit=limit)
        
        if results:
            st.success(f"Found {len(results)} matching document(s) for query: '{query}'")
            
            # Format results into DataFrame and cards
            results_data = [res.to_dict() for res in results]
            df = pd.DataFrame(results_data)
            
            st.dataframe(
                df[["rank", "filename", "score", "matched_terms", "occurrences"]],
                use_container_width=True
            )
            
            st.markdown("### 📄 Result Details & Snippets")
            for res in results:
                with st.expander(f"#{res.rank} {res.filename} — Score: {res.score:.4f}"):
                    st.write(f"**Matched Terms:** {', '.join(res.matched_terms)}")
                    st.write(f"**Total Term Occurrences:** {res.occurrences}")
                    st.markdown(f"**Context Snippet:** {res.snippet}")
        else:
            st.warning(f"No results found for query: '{query}'")
