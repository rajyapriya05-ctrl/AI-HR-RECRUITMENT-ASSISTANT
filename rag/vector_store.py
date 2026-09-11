import os
import chromadb
from chromadb.config import Settings
from typing import List


class VectorStore:
    def __init__(self, persist_directory: str = './data/chroma'):
        os.makedirs(persist_directory, exist_ok=True)
        try:
            self.client = chromadb.Client(Settings(chroma_db_impl='duckdb+parquet', persist_directory=persist_directory))
            try:
                self.col = self.client.get_collection('resumes')
            except Exception:
                self.col = self.client.create_collection('resumes')
        except Exception as e:
            self.client = None
            self.col = None
            print(f"VectorStore init error: {e}")

    def add(self, ids: List[str], documents: List[str], embeddings: List[List[float]], metadatas: List[dict]):
        if not self.col:
            print("VectorStore not initialized, skipping add")
            return
        try:
            self.col.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        except Exception as e:
            print(f"VectorStore add error: {e}")

    def query_candidate(self, query_text: str, candidate: str, top_k: int = 5):
        if not self.col:
            print("VectorStore not initialized, returning empty results")
            return []
        try:
            res = self.col.query(query_texts=[query_text], n_results=top_k, where={'candidate': candidate})
            return res.get('documents', [[]])[0]
        except Exception as e:
            print(f"VectorStore query error: {e}")
            return []
