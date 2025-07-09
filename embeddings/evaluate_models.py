from typing import Any, List, Dict
from sentence_transformers_embedder import SentenceTransformersEmbedder
from sklearn.metrics.pairwise import cosine_similarity
from gemini_embedder import GeminiEmbedder
from openai_embedder import OpenAIEmbedder

def compare_models(texts: List[str], embedders: Dict[str, Any]):
    embeddings = {}
    for name, embedder in embedders.items():
        embs = embedder.embed_chunks(texts)
        embeddings[name] = embs
        print(f"Modello {name} ha prodotto {len(embs)} embedding(s)")

    # Calcolo similarità cosine tra embedding dello stesso testo tra i modelli
    for i, text in enumerate(texts):
        print(f"\nTesto {i+1}: {text}")
        keys = list(embeddings.keys())
        for j in range(len(keys)-1):
            for k in range(j+1, len(keys)):
                sim = cosine_similarity(
                    embeddings[keys[j]][i].reshape(1, -1),
                    embeddings[keys[k]][i].reshape(1, -1)
                )[0][0]
                print(f"Similarity cosine tra {keys[j]} e {keys[k]}: {sim:.4f}")

# Esempio di utilizzo
texts = [
    "Il progetto prevede l'analisi dei dati",
    "Analisi approfondita dei risultati del progetto",
    "Gestione e archiviazione documenti"
]

embedders = {
    "miniLM": SentenceTransformersEmbedder("all-MiniLM-L6-v2"),
    "mpnet": SentenceTransformersEmbedder("all-mpnet-base-v2"),
    "openai": OpenAIEmbedder("text-embedding-3-small"),
    "gemini": GeminiEmbedder("gemini-embedding-exp-03-07")  
}

compare_models(texts, embedders)