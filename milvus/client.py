from pymilvus import MilvusClient
import os
from milvus.schema import COLLECTION_NAME, EMBEDDING_DIM
from milvus.utils import prepare_milvus_data

MILVUS_URI = os.getenv("MILVUS_URI")

class MilvusHandler:
    def __init__(self):
        self.client = MilvusClient(uri=MILVUS_URI)
        self.collection_name = COLLECTION_NAME

    def create_collection(self):
        if self.client.has_collection(self.collection_name):
            print(f"Collezione '{self.collection_name}' già esistente")
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=EMBEDDING_DIM,
            metric_type="IP",  # inner product
            consistency_level="Strong",
        )
        print(f"Collezione '{self.collection_name}' creata")

    def reset_collection(self):
        """Utile in fase di sviluppo per pulire tutto"""
        if self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)
            print(f"Collezione '{self.collection_name}' eliminata")
        self.create_collection()

    def insert_embeddings(self, chunks: list[str], embeddings: list, source: str = "manual"):
        """
        Inserisce i chunk e i loro embedding nella collezione Milvus

        :param chunks: lista di stringhe testuali
        :param embeddings: lista di vettori (np.ndarray o list[float])
        :param source: da dove proviene il documento (es. SharePoint, nome file...)
        """
        data = prepare_milvus_data(chunks, embeddings, source)
        self.client.insert(self.collection_name, data=data)
        print(f"Inseriti {len(data)} chunk nella collezione")

    def search(self, query_vector: list[float], top_k: int = 3) -> list[str]:
        """
        Cerca i chunk più simili a un vettore di embedding

        :param query_vector: embedding della query
        :return: lista di stringhe (i testi ritrovati)
        """
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=top_k,
            output_fields=["metadata"]
        )
        top_chunks = [hit["entity"]["metadata"]["text"] for hit in results[0]]
        return top_chunks
