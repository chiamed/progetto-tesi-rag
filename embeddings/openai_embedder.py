from openai import OpenAI
import numpy as np
from typing import List
import os

class OpenAIEmbedder():
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name
        self.client = self._initialize_client()
        print(f"Modello OpenAI per embedding: {model_name}")

    def _initialize_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY non trovato nelle variabili d'ambiente")
        return OpenAI(api_key=api_key)

    def embed_chunks(self, chunks: List[str]) -> List[np.ndarray]:
        """
        Genera embedding per una lista di chunk di testo usando OpenAI

        Argomenti:
            chunks: Lista di stringhe da convertire in embedding

        Output:
            Lista di numpy array contenenti gli embedding
        """
        if not isinstance(chunks, list):
            raise ValueError("Input deve essere una lista di stringhe")

        if not chunks:
            return []

        response = self.client.embeddings.create(
            input=chunks,
            model=self.model_name
        )

        embeddings = [np.array(res.embedding) for res in response.data]
        return embeddings