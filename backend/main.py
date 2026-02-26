from fastapi import FastAPI, Form
import requests

app = FastAPI()

def call_llm(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",  # or "mistral"
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

@app.post("/analyze/")
def analyze_legal(text: str = Form(...)):
    prompts = {
        "summary": (
            "Summarize the following legal document in clear language:\n\n"
            f"{text}"
        ),
        "clauses": (
            "Extract key clauses such as Termination, Liability, "
            "Jurisdiction, Payment, and Confidentiality:\n\n"
            f"{text}"
        ),
        "entities": (
            "Extract all named entities such as parties, dates, locations, "
            "laws, and monetary amounts:\n\n"
            f"{text}"
        )
    }
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"  # or "mistral"

class AnalyzeRequest(BaseModel):
    text: str

def call_llm(prompt: str) -> str:
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=120,
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Ollama not reachable: {e}")

    # If Ollama returns non-200, show its message
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Ollama error {r.status_code}: {r.text}")

    # If response isn't valid JSON, fail clearly
    try:
        data = r.json()
    except ValueError:
        raise HTTPException(status_code=502, detail=f"Ollama returned non-JSON: {r.text[:500]}")

    if "response" not in data:
        raise HTTPException(status_code=502, detail=f"Unexpected Ollama payload: {data}")

    return data["response"].strip()

@app.post("/analyze/")
def analyze_legal(req: AnalyzeRequest):
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")

    prompts = {
        "summary": (
            "Summarize the following legal document in clear language:\n\n"
            f"{text}"
        ),
        "clauses": (
            "Extract key clauses (Termination, Liability, Jurisdiction, Payment, Confidentiality). "
            "Return as bullet points with clause name + extracted text.\n\n"
            f"{text}"
        ),
        "entities": (
            "Extract named entities: parties, dates, locations, laws, monetary amounts. "
            "Return as JSON-like lists per category.\n\n"
            f"{text}"
        ),
    }

    results = {}
    for key, prompt in prompts.items():
        results[key] = call_llm(prompt)

    return results
    results = {key: call_llm(prompt) for key, prompt in prompts.items()}
    return results
