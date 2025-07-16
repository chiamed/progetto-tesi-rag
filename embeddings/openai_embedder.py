from openai import OpenAI
import numpy as np
from typing import List
import os

class OpenAIEmbedder():
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name
        self.client = self._initialize_client()
        print(f"OpenAI model for embeddings: {model_name}")

    def _initialize_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY not found in environment variables")
        return OpenAI(api_key=api_key)

    def embed_chunks(self, chunks: List[str]) -> List[np.ndarray]:
        """
        Generates embeddings for a list of text chunks using OpenAI

        Args:
            chunks: List of strings to convert into embeddings

        Returns:
            List of numpy arrays containing the embeddings
        """
        if not isinstance(chunks, list):
            raise ValueError("Input must be a list of strings")

        if not chunks:
            return []

        response = self.client.embeddings.create(
            input=chunks,
            model=self.model_name,
            #dimensions=768
        )

        embeddings = [np.array(res.embedding) for res in response.data]
        return embeddings