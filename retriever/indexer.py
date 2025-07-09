from pathlib import Path
from pydantic import BaseModel
from embeddings.openai_embedder import OpenAIEmbedder
from embeddings.gemini_embedder import GeminiEmbedder
from milvus.client import MilvusHandler
from processing.chunker import Chunker 
from processing.parser import Parser

SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

class Indexer(BaseModel):
    """
    Class used to index documents into Milvus.
    """

    def index_document(self, file_path: str, source_name: str | None = None, model: str = "openai"):
        """
        Index a document into Milvus.
        :param file_path: path to the document file
        :param source_name: optional name for the source of the document
        :param model: embedding model to use, either "openai" or "gemini"
        """
        chunker = Chunker()
        parser = Parser()

        path = Path(file_path)
        if not path.exists():
            print(f"File non trovato: {file_path}")
            return

        if path.suffix in SUPPORTED_EXTENSIONS:
            text = parser.extract_text(file_path)
        else:
            print(f"Tipo file non supportato: {path.suffix}")
            return

        if not text.strip():
            print(f"Nessun contenuto utile trovato in {file_path}")
            return

        if (model == "openai"):
            embedder = OpenAIEmbedder()
        else:
            embedder = GeminiEmbedder()
            
        chunks = chunker.split_text_into_chunks(text)
        
        embeddings = embedder.embed_chunks(chunks)

        milvus = MilvusHandler()
        milvus.insert_embeddings(chunks, embeddings, source=source_name or path.name)

        print(f"Indicizzato {file_path} ({len(chunks)} chunk)")
        return True
