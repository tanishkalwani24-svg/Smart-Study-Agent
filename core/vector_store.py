"""
core/vector_store.py
ChromaDB-based vector store.
Uses PersistentClient so indexed chunks survive page reloads.
Falls back to local sentence-transformers when watsonx creds are absent.
The embedding model is cached at module level so it is only loaded once
per server process — not on every page navigation.
"""
import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Persist DB next to the project root
_DB_PATH = os.path.join(os.path.dirname(__file__), "..", ".chroma_db")

# Module-level embedding function cache — loaded only once
_embedder_cache = None
_use_langchain_cache = None


def _get_embedder():
    """Return a cached embedder, building it only on first call."""
    global _embedder_cache, _use_langchain_cache

    if _embedder_cache is not None:
        return _embedder_cache, _use_langchain_cache

    api_key    = os.getenv("WATSONX_API_KEY", "").strip()
    project_id = os.getenv("WATSONX_PROJECT_ID", "").strip()
    url        = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    # Only try IBM embeddings if BOTH keys are present, non-placeholder,
    # and Groq is NOT the active backend (no point calling IBM when using Groq)
    try:
        import streamlit as st
        groq_key = st.secrets.get("GROQ_API_KEY", "") or os.getenv("GROQ_API_KEY", "")
    except Exception:
        groq_key = os.getenv("GROQ_API_KEY", "")
    groq_key = groq_key.strip()
    if api_key and project_id and "your_" not in api_key and not groq_key:
        try:
            from langchain_ibm import WatsonxEmbeddings
            embedder = WatsonxEmbeddings(
                model_id   = os.getenv("EMBEDDING_MODEL_ID", "ibm/slate-125m-english-rtrvr"),
                url        = url,
                apikey     = api_key,
                project_id = project_id,
            )
            # Quick smoke-test so we fail fast instead of on first query
            embedder.embed_query("test")
            _embedder_cache       = embedder
            _use_langchain_cache  = True
            return _embedder_cache, _use_langchain_cache
        except Exception:
            pass  # fall through to local

    # Local fallback: use chromadb's built-in fast embedding (ONNX, no torch load)
    from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
    _embedder_cache      = ONNXMiniLM_L6_V2()
    _use_langchain_cache = False
    return _embedder_cache, _use_langchain_cache


class VectorStore:
    """
    Persistent ChromaDB vector store.
    Embedding backend is built once and cached at module level.
    """

    COLLECTION_NAME = "study_docs"

    def __init__(self):
        self.client = chromadb.PersistentClient(path=os.path.abspath(_DB_PATH))
        self._embedder, self._use_langchain = _get_embedder()

        if self._use_langchain:
            self._collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME
            )
        else:
            self._collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                embedding_function=self._embedder,
            )

    # ── Write ──────────────────────────────────────────────────────────────────

    def add_chunks(self, chunks: list[str], doc_name: str = "document") -> None:
        """Index a list of text chunks under a document name."""
        if not chunks:
            return

        ids       = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": doc_name, "chunk_index": i} for i in range(len(chunks))]

        existing  = set(self._collection.get(ids=ids)["ids"])
        new_ids   = [i for i in ids       if i not in existing]
        new_docs  = [chunks[ids.index(i)] for i in new_ids]
        new_meta  = [metadatas[ids.index(i)] for i in new_ids]

        if not new_ids:
            return

        if self._use_langchain:
            embeddings = self._embedder.embed_documents(new_docs)
            self._collection.add(
                ids=new_ids, documents=new_docs,
                embeddings=embeddings, metadatas=new_meta,
            )
        else:
            self._collection.add(
                ids=new_ids, documents=new_docs, metadatas=new_meta,
            )

    # ── Read ───────────────────────────────────────────────────────────────────

    def query(self, question: str, n_results: int = 4) -> list[str]:
        """Return the top-n most relevant chunks for a query."""
        if self._collection.count() == 0:
            return []
        safe_n = min(n_results, self._collection.count())
        if self._use_langchain:
            results = self._collection.query(
                query_embeddings=[self._embedder.embed_query(question)],
                n_results=safe_n,
            )
        else:
            results = self._collection.query(
                query_texts=[question], n_results=safe_n,
            )
        return results.get("documents", [[]])[0]

    # ── Maintenance ────────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Delete and recreate the collection."""
        try:
            self.client.delete_collection(self.COLLECTION_NAME)
        except Exception:
            pass
        if self._use_langchain:
            self._collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME
            )
        else:
            self._collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                embedding_function=self._embedder,
            )

    def delete_doc(self, doc_name: str) -> None:
        self._collection.delete(where={"source": doc_name})

    @property
    def count(self) -> int:
        return self._collection.count()

    def list_sources(self) -> list[str]:
        if self._collection.count() == 0:
            return []
        results = self._collection.get(include=["metadatas"])
        return sorted({m["source"] for m in results["metadatas"] if "source" in m})
