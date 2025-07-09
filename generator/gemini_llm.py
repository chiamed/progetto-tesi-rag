import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_answer_gemini(query: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    SYSTEM_PROMPT = "Rispondi solo usando le informazioni fornite nel contesto. Se non ci sono abbastanza dati, di' che non sai rispondere."
    USER_PROMPT = f"Rispondi alla seguente domanda in base al contesto fornito.\n\nContesto:\n{context}\n\nDomanda: {query}"

    try:
        response = model.generate_content(
            [SYSTEM_PROMPT, USER_PROMPT],
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 500
            }
        )
        return response.text.strip()
    except Exception as e:
        return f"Errore durante la generazione della risposta: {e}"
