from typing import List
import numpy as np

def prepare_milvus_data(chunks: List[str], embeddings: List[np.ndarray], source: str) -> List[dict]:
    """
    Prepara i dati da inserire in Milvus con id, vector, metadata

    :param chunks: lista di stringhe
    :param embeddings: lista di np.ndarray
    :param source: nome file o fonte documento
    :return: lista di dict compatibili con Milvus
    """
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks ed embeddings devono avere la stessa lunghezza")

    data = []
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        data.append({
            "id": i,
            "vector": vector.tolist(),
            "metadata": {
                "text": chunk,
                "source": source
            }
        })
    return data
