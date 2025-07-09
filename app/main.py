from fastapi import FastAPI, Request
from generator.factory import get_llm
from retriever.retriever import Retriever
from dotenv import load_dotenv
from pymilvus import connections
from common.utils import Setupper
from retriever.cache import CacheManager


cache_manager: CacheManager = CacheManager.from_env()


load_dotenv()

# Connessione a Milvus
try:
    connections.connect(alias="default", host="localhost", port="19530")
    print("Connessione a Milvus riuscita")
except Exception as e:
    print(f"Errore nella connessione a Milvus: {e}")


setupper = Setupper.from_env(model="gemini")  # Cambia il modello se necessario
setupper.setup(cache_manager=cache_manager)

# Avvio FastAPI
app = FastAPI()
retriever = Retriever(embedder_model="gemini", top_k=3)

@app.post("/query")
async def query_rag(request: Request):
    body = await request.json()
    query: str = body.get("prompt")
    provider: str = "gemini" # Cambia il provider se necessario

    if not query or not isinstance(query, str):
        return {"error": "Prompt mancante o non valido"}

    try:
        generate_answer = get_llm(provider)
    except ValueError as e:
        return {"error": str(e)}

    chunks = retriever.retrieve(query)
    answer = generate_answer(query, chunks)

    return {
        "provider": provider,
        "query": query,
        "chunks": chunks,
        "answer": answer
    }

# per avviare il server, usa: uvicorn app.main:app --reload