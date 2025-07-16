from typing import List
import numpy as np

def prepare_milvus_data(chunks: List[str], embeddings: List[np.ndarray], source: str) -> List[dict]:
    """
    Prepare data to insert into Milvus with id, vector, metadata

    :param chunks: list of strings
    :param embeddings: list of np.ndarray
    :param source: file name or document source
    :return: list of dict compatible with Milvus
    """
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must have the same length")

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
