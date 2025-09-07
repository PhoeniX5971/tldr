from fastapi import FastAPI
from pydantic import BaseModel
from ai.ai_graph import invoke_graph

# ----------------------------
# FastAPI setup
# ----------------------------
app = FastAPI(title="tldr", version="alpha")


class MessageRequest(BaseModel):
    text: str


@app.post("/summarize")
def summarize(req: MessageRequest):
    summary = invoke_graph(req.text, node="summarizer")
    return {"summary": summary}


@app.post("/web_search")
def web_search(req: MessageRequest):
    web_search = invoke_graph(req.text, node="searcher")
    return {"web_search": web_search}
