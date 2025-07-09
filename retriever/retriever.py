from embeddings.openai_embedder import OpenAIEmbedder
from embeddings.gemini_embedder import GeminiEmbedder  # Assicurati di importare GeminiEmbedder
from milvus.client import MilvusHandler

class Retriever:
    def __init__(self, embedder_model: str = "openai", top_k: int = 3):
        if embedder_model == "openai":
            self.embedder = OpenAIEmbedder()
        elif embedder_model == "gemini":
            self.embedder = GeminiEmbedder()
        else:
            raise ValueError(f"Tipo di embedder non supportato: {embedder_model}")
        
        self.milvus = MilvusHandler()
        self.top_k = top_k

    def retrieve(self, query: str) -> list[str]:
        """
        Esegue una ricerca semantica in Milvus a partire da una query testuale

        :param query: stringa con la domanda dell'utente
        :return: lista di chunk di testo rilevanti
        """
        if not query:
            raise ValueError("La query non può essere vuota")

        # 1. Embedding della query
        print("Generazione embedding della query...")
        query_vector = self.embedder.embed_chunks([query])[0]

        # 2. Ricerca in Milvus
        print("Esecuzione ricerca semantica...")
        results = self.milvus.search(query_vector.tolist(), top_k=self.top_k)

        return results
