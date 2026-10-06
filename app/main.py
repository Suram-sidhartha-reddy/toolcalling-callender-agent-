from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import run_agent
#from app.watsapp.webhook import router as whatsapp_router


app = FastAPI(
    title="Calendar AI Agent",
    description="AI-powered Google Calendar agent",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str
    source: str = "user_command"
    sender: str | None = None


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
    response = run_agent(
        user_message=request.message,
        source=request.source,
        sender=request.sender,
    )

    return {
        "response": response
    }


#app.include_router(whatsapp_router)