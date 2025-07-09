from generator.openai_llm import generate_answer_openai
from generator.gemini_llm import generate_answer_gemini

def get_llm(provider: str):
    provider = provider.lower()
    if provider == "openai":
        return generate_answer_openai
    elif provider == "gemini":
        return generate_answer_gemini
    else:
        raise ValueError(f"Provider LLM non supportato: {provider}")
