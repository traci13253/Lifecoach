from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str


class ChatSession(BaseModel):
    """A record of a user prompt and the AI response."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    prompt: str
    response: str


class ChatResponse(BaseModel):
    id: str
    response: str


class ChatHistory(BaseModel):
    sessions: List[ChatSession] = Field(default_factory=list)
