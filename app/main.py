from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import run_agent


app = FastAPI(
    title="Calendar AI Agent",
    description="AI-powered Google Calendar agent",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Calendar AI Agent is running",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = run_agent(request.message)

    return {
        "response": response
    }