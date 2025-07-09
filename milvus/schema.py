import os

# Usa le variabili d'ambiente se presenti, altrimenti fallback
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "project_docs")

# 1536 per OpenAI text-embedding-3-small / 384 per MiniLM
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))

# Metrica per la similarità (IP = Inner Product)
METRIC_TYPE = "IP"

# Livello di consistenza
CONSISTENCY_LEVEL = "Strong"
