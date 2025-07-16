from fastapi import FastAPI, Request
from generator.factory import get_llm
from retriever.retriever import Retriever
from dotenv import load_dotenv
from pymilvus import connections
from common.utils import Setupper
from retriever.cache import CacheManager

cache_manager: CacheManager = CacheManager.from_env()

load_dotenv()

# Connection to Milvus
try:
    connections.connect(alias="default", host="localhost", port="19530")
    print("Successfully connected to Milvus")
except Exception as e:
    print(f"Error connecting to Milvus: {e}")


setupper = Setupper.from_env(model="gemini")  # Change the model if necessary
setupper.setup(cache_manager=cache_manager)

# Start FastAPI
app = FastAPI()
retriever = Retriever(embedder_model="gemini", top_k=3)

@app.post("/query")
async def query_rag(request: Request):
    body = await request.json()
    query: str = body.get("prompt")
    provider: str = "gemini"  # Change the provider if necessary

    if not query or not isinstance(query, str):
        return {"error": "Missing or invalid prompt"}

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

# To start the server, use: uvicorn app.main:app --reload