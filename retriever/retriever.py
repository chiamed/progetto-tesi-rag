from embeddings.openai_embedder import OpenAIEmbedder
from embeddings.gemini_embedder import GeminiEmbedder 
from milvus.client import MilvusHandler

class Retriever:
    def __init__(self, embedder_model: str = "openai", top_k: int = 3):
        if embedder_model == "openai":
            self.embedder = OpenAIEmbedder()
        elif embedder_model == "gemini":
            self.embedder = GeminiEmbedder()
        else:
            raise ValueError(f"Unsupported embedder type: {embedder_model}")
        
        self.milvus = MilvusHandler()
        self.top_k = top_k

    def retrieve(self, query: str) -> list[str]:
        """
        Performs semantic search in Milvus based on a textual query

        :param query: string containing the user's question
        :return: list of relevant text chunks
        """
        if not query:
            raise ValueError("The query cannot be empty")

        # 1. Embedding the query
        print("Generating query embedding...")
        query_vector = self.embedder.embed_chunks([query])[0]

        # 2. Semantic search in Milvus
        print("Performing semantic search...")
        results = self.milvus.search(query_vector.tolist(), top_k=self.top_k)

        return results
