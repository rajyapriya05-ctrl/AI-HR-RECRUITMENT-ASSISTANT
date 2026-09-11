import os
from pypdf import PdfReader
import docx
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

logger = logging.getLogger(__name__)


def extract_text(path: str) -> str:
    _, ext = os.path.splitext(path.lower())
    if ext == '.pdf':
        try:
            r = PdfReader(path)
            return '\n'.join([p.extract_text() or '' for p in r.pages])
        except Exception:
            return ''
    if ext in ('.docx', '.doc'):
        try:
            d = docx.Document(path)
            return '\n'.join([p.text for p in d.paragraphs])
        except Exception:
            return ''
    if ext == '.txt':
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return ''
    return ''


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 200) -> List[str]:
    if not text:
        return []
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        c = tokens[i:i+chunk_size]
        chunks.append(' '.join(c))
        i += chunk_size - overlap
    return chunks


class EmbeddingGenerator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            logger.exception("Failed to load embedding model: %s", e)
            self.model = None

    def embed_texts(self, texts: List[str]):
        if not texts:
            return []
        if self.model is None:
            logger.warning("Embedding model not available, returning zero vectors")
            return [[0.0] * 384 for _ in texts]
        embs = self.model.encode(texts, show_progress_bar=False)
        return [list(map(float, e)) for e in np.array(embs)]
