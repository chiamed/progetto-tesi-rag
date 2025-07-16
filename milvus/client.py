from pymilvus import MilvusClient
import os
from milvus.schema import COLLECTION_NAME, GEMINI_EMBEDDING_DIM, OPENAI_EMBEDDING_DIM
from milvus.utils import prepare_milvus_data

MILVUS_URI = os.getenv("MILVUS_URI")

class MilvusHandler:
    def __init__(self, model_name: str = "openai"):
        self.client = MilvusClient(uri=MILVUS_URI)
        self.collection_name = COLLECTION_NAME
        if model_name.lower() == "openai":
            self.embedding_dim = OPENAI_EMBEDDING_DIM
        elif model_name.lower() == "gemini":
            self.embedding_dim = GEMINI_EMBEDDING_DIM
        else:
            raise ValueError(f"Modello embedding non supportato: {model_name}")

    def create_collection(self):
        if self.client.has_collection(self.collection_name):
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=self.embedding_dim,
            metric_type="IP",  # inner product
            consistency_level="Strong",
        )

    def reset_collection(self):
        """Useful during development to clear everything"""
        if self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)
        self.create_collection()

    def insert_embeddings(self, chunks: list[str], embeddings: list, source: str = "manual"):
        """
        Inserts chunks and their embeddings into the Milvus collection

        :param chunks: list of textual strings
        :param embeddings: list of vectors (np.ndarray or list[float])
        :param source: source of the document (e.g., SharePoint, file name...)
        """
        data = prepare_milvus_data(chunks, embeddings, source)
        self.client.insert(self.collection_name, data=data)
        print(f"Inserted {len(data)} chunks into the collection")

    def search(self, query_vector: list[float], top_k: int = 3) -> list[str]:
        """
        Searches for the chunks most similar to an embedding vector

        :param query_vector: embedding of the query
        :return: list of strings (retrieved texts)
        """
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=top_k,
            output_fields=["metadata"]
        )
        top_chunks = [hit["entity"]["metadata"]["text"] for hit in results[0]]
        return top_chunks
