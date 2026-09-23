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

    # user_command:
    # The user is directly talking to the calendar agent.
    #
    # incoming_message:
    # Someone else sent a message to the user.
    source: str = "user_command"

    # Only needed when source == incoming_message
    sender: str | None = None


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Calendar AI Agent is running",
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    response = run_agent(
        user_message=request.message,
        source=request.source,
        sender=request.sender,
    )

    return {
        "response": response
    }