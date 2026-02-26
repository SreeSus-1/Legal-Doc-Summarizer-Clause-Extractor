# Legal-Doc-Summarizer-Clause-Extractor
Using LLaMA 2 / Mistral (via Ollama), FastAPI &amp; Streamlit

AI-powered assistant for summarizing legal documents, extracting key clauses,
and identifying named entities.

## Features
- Summarize complex legal documents
- Extract clauses (Termination, Liability, Jurisdiction, etc.)
- Identify parties, dates, locations, and laws
- FastAPI backend with Streamlit frontend

## How to Run
1. Pull model:
   ollama pull llama2
2. Start backend:
   uvicorn backend.main:app --reload
3. Start frontend:
   streamlit run frontend/app.py
