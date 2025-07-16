from pydantic import BaseModel


class Chunker(BaseModel):
    """
    Class used to split text into chunks.
    """

    # overlap = number of overlapping words between consecutive chunks, useful for maintaining context
    def split_text_into_chunks(self, text: str, max_words: int = 200, overlap: int = 20) -> list[str]:
        """
        Splits the extracted text into smaller chunks for processing in RAG
        """
        words = text.split() # Split the text into individual words
        chunks = []

        for i in range(0, len(words), max_words - overlap):
            chunk = words[i:i + max_words]
            chunks.append(" ".join(chunk)) # Joins the words of the chunk into a string

        return chunks