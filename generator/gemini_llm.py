import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_answer_gemini(query: str, context_chunks: list[str]) -> str:
    context = "\n\n".join([f"- {chunk.strip()}" for chunk in context_chunks])
 
    prompt = (
        "Usa **solo** le informazioni nel contesto seguente per rispondere alla domanda. "
        "Se le informazioni non sono presenti o non sono sufficienti, rispondi 'Non lo so'.\n\n"
        f"Contesto:\n{context}\n\n"
        f"Domanda: {query}"
    )

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 512
            }
        )
        return response.text.strip()
    except Exception as e:
        return f"Error while generating the response: {e}"