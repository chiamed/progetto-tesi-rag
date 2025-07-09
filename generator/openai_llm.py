from openai import OpenAI

client = OpenAI()

def generate_answer_openai(query: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    SYSTEM_PROMPT = "Rispondi alla domanda solo usando le informazioni fornite nel contesto. Se non ci sono abbastanza dati, di' che non sai rispondere."
    USER_PROMPT = f"Rispondi alla seguente domanda in base al contesto fornito.\n\nContesto:\n{context}\n\nDomanda: {query}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT}
            ],
            temperature=1, # livello di creatività della risposta
            max_completion_tokens=500 # numero massimo di "parole spezzate" nella risposta
            # 1 parola = 1.3-1.5 token ca; 500 token = 350-400 parole ca
        )

        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            return "Nessuna risposta ricevuta dal modello."
    except Exception as e:
        return f"Errore durante la generazione della risposta: {e}"

