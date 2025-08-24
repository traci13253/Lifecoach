import asyncio
from typing import Dict


async def generate_response(message: str) -> str:
    """Mock async function to generate a response."""
    await asyncio.sleep(0)
    return message[::-1]


async def health_check() -> Dict[str, str]:
    """Return the application's health status."""
    return {"status": "ok"}


async def chat(message: str) -> Dict[str, str]:
    """Handle chat messages asynchronously."""
    response = await generate_response(message)
    return {"response": response}
