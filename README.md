# 🧠 **RAG SharePoint Chatbot**

Un sistema di Retrieval-Augmented Generation che indicizza documenti da SharePoint e consente di interrogarli tramite modelli LLM (OpenAI o Gemini), con API FastAPI e interfaccia in Streamlit.

## 🚀 **Funzionalità principali**

- 📂 **Estrazione documenti da SharePoint** (PDF, DOCX)
- 🧩 **Indicizzazione** con embedding OpenAI + Milvus
- 💬 **Query semantiche** con OpenAI (gpt-4o-mini) o Gemini (gemini-2.5-flash)
- 🔧 **FastAPI** per le API
- 🖥️ **Interfaccia utente in Streamlit**

## ⚙️ **Esecuzione**

### 🔁 1. Clona il progetto
```bash
git clone https://github.com/tuo-username/progetto-pubblico.git
cd progetto-pubblico
```

### 🐳 2. Esecucuzione con Docker
```bash
docker compose up --build
```

### ⚡ 3. Avvio rapido
```bash
uvicorn app.main:app --reload
```

### 💻 4. Interfaccia utente
```bash
uvicorn app.main:app --reload
```

## ✨ **Credits**
Realizzato come progetto di tesi universitaria. Powered by:
- OpenAI
- Gemini (Google)
- Milvus
- FastAPI
- Streamlit
- Microsoft Graph API

## 📜 **Licenza**
Questo progetto è rilasciato per fini dimostrativi e accademici. Nessun dato sensibile è incluso nella versione pubblica.
