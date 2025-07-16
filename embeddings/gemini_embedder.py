import os
import numpy as np
from typing import List
import google.generativeai as genai

class GeminiEmbedder():
    def __init__(self, model_name: str = "models/embedding-001"):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GOOGLE_API_KEY not found in environment variables")
        print(f"Gemini model for embedding: {self.model_name}")

    def embed_chunks(self, chunks: List[str]) -> List[np.ndarray]:
        """
        Generates embeddings for a list of text chunks using Google Gemini
        """
        if not chunks:
            return []

        embeddings = []
        for chunk in chunks:
            response = genai.embed_content( 
                model=self.model_name,
                content=chunk,
                task_type="RETRIEVAL_DOCUMENT"
            )
            embeddings.append(np.array(response["embedding"]))
        return embeddings
