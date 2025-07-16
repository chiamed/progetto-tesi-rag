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
            temperature=1, # level of creativity in the response
            max_completion_tokens=500 # nmax number of tokens in the response
            # 1 word = ~1.3-1.5 token, 500 tokens = ~300-400 words
        )

        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            return "No response received from the model."
    except Exception as e:
        return f"Error while generating the response: {e}"

