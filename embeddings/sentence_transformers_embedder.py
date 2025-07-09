from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class SentenceTransformersEmbedder():
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        print(f"Modello SentenceTransformer: {self.model_name}")

    def embed_chunks(self, chunks: List[str]) -> List[np.ndarray]:
        chunks = [chunk for chunk in chunks if chunk.strip()]
        if not chunks:
            return []
        embeddings = self.model.encode(chunks, convert_to_numpy=True)
        return [np.array(emb) for emb in embeddings]
