from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging

from common.ollama_client import generate

logger = logging.getLogger("backend")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = 512


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate_text(req: GenRequest):
    try:
        out = generate(req.prompt, model=req.model, host=None)
        return {"output": out}
    except Exception as e:
        logger.exception("Generation failed")
        return {"error": str(e)}
