from abc import ABC, abstractmethod
from typing import List

import numpy as np


class BaseEmbedder(ABC):
    @abstractmethod
    def embed_chunks(self, chunks: List[str]) -> List[np.ndarray]:
        """
        Metodo da implementare per ogni embedder.
        Deve restituire una lista di vettori numpy, uno per ogni chunk.
        """
        pass