"""
core/vector_store.py
ChromaDB-based vector store with IBM watsonx embeddings for RAG.
Uses PersistentClient so indexed chunks survive page reloads.
Falls back to local sentence-transformers when watsonx creds are absent.
"""
import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Persist DB next to the project root
_DB_PATH = os.path.join(os.path.dirname(__file__), "..", ".chroma_db")


class VectorStore:
    """
    Persistent ChromaDB vector store.
    Embedding backend:
      - Primary  : IBM watsonx Slate embeddings (when creds are present)
      - Fallback : sentence-transformers all-MiniLM-L6-v2 (local, no creds needed)
    """

    COLLECTION_NAME = "study_docs"

    def __init__(self):
        self.client = chromadb.PersistentClient(path=os.path.abspath(_DB_PATH))
        self._use_langchain = False
        self._embedder = None
        self._init_embedder()

    def _init_embedder(self):
        api_key    = os.getenv("WATSONX_API_KEY", "").strip()
        project_id = os.getenv("WATSONX_PROJECT_ID", "").strip()
        url        = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

        if api_key and project_id:
            try:
                from langchain_ibm import WatsonxEmbeddings
                self._embedder = WatsonxEmbeddings(
                    model_id=os.getenv(
                        "EMBEDDING_MODEL_ID", "ibm/slate-125m-english-rtrvr"
                    ),
                    url=url,
                    apikey=api_key,
                    project_id=project_id,
                )
                self._use_langchain = True
                self._collection = self.client.get_or_create_collection(
                    name=self.COLLECTION_NAME
                )
                return
            except Exception:
                pass  # fall through to local embedder

        # Local fallback — no credentials required
        from chromadb.utils import embedding_functions
        self._embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self._collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=self._embedder,
        )

    # ── Write ──────────────────────────────────────────────────────────────────

    def add_chunks(self, chunks: list[str], doc_name: str = "document") -> None:
        """Index a list of text chunks under a document name."""
        if not chunks:
            return

        # De-duplicate: skip chunks whose IDs already exist
        ids       = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": doc_name, "chunk_index": i} for i in range(len(chunks))]

        existing = set(self._collection.get(ids=ids)["ids"])
        new_ids   = [i for i in ids       if i not in existing]
        new_docs  = [chunks[ids.index(i)] for i in new_ids]
        new_meta  = [metadatas[ids.index(i)] for i in new_ids]

        if not new_ids:
            return

        if self._use_langchain:
            embeddings = self._embedder.embed_documents(new_docs)
            self._collection.add(
                ids=new_ids,
                documents=new_docs,
                embeddings=embeddings,
                metadatas=new_meta,
            )
        else:
            self._collection.add(
                ids=new_ids,
                documents=new_docs,
                metadatas=new_meta,
            )

    # ── Read ───────────────────────────────────────────────────────────────────

    def query(self, question: str, n_results: int = 4) -> list[str]:
        """Return the top-n most relevant chunks for a query."""
        if self._collection.count() == 0:
            return []

        safe_n = min(n_results, self._collection.count())

        if self._use_langchain:
            q_embedding = self._embedder.embed_query(question)
            results = self._collection.query(
                query_embeddings=[q_embedding],
                n_results=safe_n,
            )
        else:
            results = self._collection.query(
                query_texts=[question],
                n_results=safe_n,
            )
        return results.get("documents", [[]])[0]

    # ── Maintenance ────────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Delete and recreate the collection (clears all documents)."""
        try:
            self.client.delete_collection(self.COLLECTION_NAME)
        except Exception:
            pass
        self._init_embedder()

    def delete_doc(self, doc_name: str) -> None:
        """Remove all chunks belonging to a specific document."""
        self._collection.delete(where={"source": doc_name})

    @property
    def count(self) -> int:
        """Total number of chunks stored."""
        return self._collection.count()

    def list_sources(self) -> list[str]:
        """Return a deduplicated list of all indexed document names."""
        if self._collection.count() == 0:
            return []
        results = self._collection.get(include=["metadatas"])
        sources = {m["source"] for m in results["metadatas"] if "source" in m}
        return sorted(sources)
