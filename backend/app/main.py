from fastapi import FastAPI

from .models.chat import ChatRequest, ChatResponse, ChatSession, ChatHistory
from .services import ai

app = FastAPI()
_history = ChatHistory()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Handle a chat prompt and return the AI response."""
    response_text = ai.generate_response(request.prompt)
    session = ChatSession(prompt=request.prompt, response=response_text)
    _history.sessions.append(session)
    return ChatResponse(id=session.id, response=session.response)


@app.get("/chat/history", response_model=ChatHistory)
def history() -> ChatHistory:
    """Return the history of chat sessions."""
    return _history
