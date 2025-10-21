from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os, json, requests

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCALAI_BASE_URL = os.getenv("LOCALAI_BASE_URL", "http://localhost:8080")
MODEL_PATH = os.getenv("MODEL_PATH", "./models")

app = FastAPI(title="Unified AI Backend")

class PromptRequest(BaseModel):
    input: str
    model: str = "deepseek-v2"

@app.get("/")
def home():
    return {"status": "Unified AI Backend Running"}

@app.get("/models")
def list_models():
    models_file = os.path.join(MODEL_PATH, "models.json")
    if os.path.exists(models_file):
        with open(models_file, "r") as f:
            return json.load(f)
    return {"installed": [], "available": []}

@app.post("/infer")
def infer(prompt_request: PromptRequest):
    model = prompt_request.model
    user_input = prompt_request.input

    if OPENAI_API_KEY:
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": user_input}]
                }
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    elif LOCALAI_BASE_URL:
        try:
            response = requests.post(
                f"{LOCALAI_BASE_URL}/v1/engines/{model}/completions",
                json={"prompt": user_input}
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"response": f"Mock response: {user_input}"}