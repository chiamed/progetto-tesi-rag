from typing import Any, List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import numpy as np
from gemini_embedder import GeminiEmbedder
from openai_embedder import OpenAIEmbedder
from sentence_transformers_embedder import SentenceTransformersEmbedder
from dotenv import load_dotenv

load_dotenv()

def compare_models_with_pca(texts: List[str], embedders: Dict[str, Any], n_components: int = 100):
    embeddings = {}
    
    # 1. Compute embeddings for each model
    for name, embedder in embedders.items():
        embs = embedder.embed_chunks(texts)
        embeddings[name] = embs
        print(f"Model {name} produced {len(embs)} embedding(s)")

    # 2. Stack all embeddings
    all_embs = np.vstack([
        np.vstack(embeddings[name]) for name in embeddings
    ])

    # 3. PCA: dimensionality reduction
    pca = PCA(n_components=5)
    all_embs_reduced = pca.fit_transform(all_embs)

    # 4. Reconstruct dictionary of reduced embeddings
    aligned_embeddings = {}
    idx = 0
    for name in embeddings:
        count = len(embeddings[name])
        aligned_embeddings[name] = all_embs_reduced[idx:idx+count]
        idx += count

    # 5. Cosine similarity between each pair of models for each text
    model_names = list(aligned_embeddings.keys())
    for i, text in enumerate(texts):
        print(f"\nText {i+1}: {text}")
        for j in range(len(model_names)-1):
            for k in range(j+1, len(model_names)):
                vec1 = aligned_embeddings[model_names[j]][i].reshape(1, -1)
                vec2 = aligned_embeddings[model_names[k]][i].reshape(1, -1)
                sim = cosine_similarity(vec1, vec2)[0][0]
                print(f"Cosine similarity between {model_names[j]} and {model_names[k]}: {sim:.4f}")

texts = [
    "Il progetto prevede l'analisi dei dati",
    "Analisi approfondita dei risultati del progetto",
    "Gestione e archiviazione documenti"
]

embedders = {
    "bert": SentenceTransformersEmbedder("bert-base-nli-mean-tokens"),
    "mpnet": SentenceTransformersEmbedder("all-mpnet-base-v2"),
    "openai": OpenAIEmbedder("text-embedding-3-small"),
    "gemini": GeminiEmbedder("models/embedding-001")
}

compare_models_with_pca(texts, embedders)