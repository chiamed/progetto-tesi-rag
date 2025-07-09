
from pydantic import BaseModel


class Chunker(BaseModel):
    """
    Class used to split text into chunks.
    """

    # overlap = numero di parole sovrapposte tra chunk consecutivi, utili per mantenere il contesto
    def split_text_into_chunks(self, text: str, max_words: int = 200, overlap: int = 20) -> list[str]:
        """
        Divide il testo estratto in chunk più piccoli per l'elaborazione nel RAG
        """
        words = text.split() # Dividi il testo in parole singole
        chunks = []

        for i in range(0, len(words), max_words - overlap):
            chunk = words[i:i + max_words]
            chunks.append(" ".join(chunk)) # unisce le parole del chunk in una stringa

        return chunks