import os

# Use environment variables if present, otherwise fallback
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "project_docs")

# 1536 for OpenAI / 768 for Gemini
OPENAI_EMBEDDING_DIM = int(os.getenv("OPENAI_EMBEDDING_DIM", "1536"))
GEMINI_EMBEDDING_DIM = int(os.getenv("GEMINI_EMBEDDING_DIM", "768"))

# Metric for similarity (IP = Inner Product)
METRIC_TYPE = "IP"

# Consistency level
CONSISTENCY_LEVEL = "Strong"
