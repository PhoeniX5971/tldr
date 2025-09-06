from fastapi import FastAPI
from pydantic import BaseModel
from ai.ai_graph import summarize_text

# ----------------------------
# FastAPI setup
# ----------------------------
app = FastAPI(title="tldr", version="alpha")


class MessageRequest(BaseModel):
    text: str


@app.post("/summarize")
def summarize(req: MessageRequest):
    summary = summarize_text(req.text)
    return {"summary": summary}
