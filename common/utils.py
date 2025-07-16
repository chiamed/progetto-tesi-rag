from pydantic import BaseModel
from milvus.client import MilvusHandler
from retriever.indexer import Indexer
from sharepoint.downloader import SharePointDownloader
from retriever.cache import CacheManager

class Setupper(BaseModel):
    """
    Class used to perform setup operations.
    """
    class Config:
        arbitrary_types_allowed = True

    milvus: MilvusHandler
    indexer: Indexer
    model: str = "openai"  # Default model is OpenAI

    @classmethod
    def from_env(cls, model: str = "openai"): # cambia per usare gemini
        """
        Create an instance of Setupper using environment variables.
        """
        milvus = MilvusHandler(model_name=model)
        indexer = Indexer()

        return cls(milvus=milvus, indexer=indexer, model=model)
    
    def download_and_index_documents(self, cache_manager: CacheManager):
        """
        Download documents from SharePoint and index them.
        """
        print("Downloading from SharePoint and indexing...")
        try:
            sp = SharePointDownloader.from_env()
            sp.download_all_files()
        except Exception as e:
            print(f"Error downloading from SharePoint: {e}")
            return
        
        # Index downloaded documents
        for file in sp.dest_folder.iterdir():
            if file.suffix.lower() in [".pdf", ".docx"]:
                already_indexed = cache_manager.exists(file.name)
                if not already_indexed:
                    self.indexer.index_document(str(file), source_name=file.name, model=self.model)
                    cache_manager.set(file.name, "indexed")
                else:
                    print(f"🔁 File already indexed (from cache): {file.name}")

        print("Indexing completed.")

    def setup(self, cache_manager: CacheManager):
        """
        Perform setup operations such as creating Milvus collection and indexing documents.
        """
        #self.milvus.reset_collection()
        self.milvus.create_collection()
        print("Milvus collection created.")

        self.download_and_index_documents(cache_manager)

        
