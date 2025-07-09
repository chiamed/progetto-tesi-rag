import requests
import streamlit as st
import time

# Streamed response emulator
def response_generator(input: str = ""): # cambia provider in "gemini" se vuoi usare Gemini per generazione risposte
    # Prepara il corpo della richiesta
    payload = {
        "prompt": input
    }

    try:
        response = requests.post("http://localhost:8000/query", json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "Nessuna risposta ricevuta.")
    except Exception as e:
        answer = f"Errore durante la richiesta: {e}"

    # Generazione risposta a parole
    for word in answer.split():
        yield word + " "
        time.sleep(0.05)


st.title("Esplora i documenti aziendali con RAG")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
 