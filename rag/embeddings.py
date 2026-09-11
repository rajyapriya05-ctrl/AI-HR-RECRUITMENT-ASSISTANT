from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List


class EmbeddingGenerator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: List[str]):
        if not texts:
            return []
        embs = self.model.encode(texts, show_progress_bar=False)
        return [list(map(float, e)) for e in np.array(embs)]
