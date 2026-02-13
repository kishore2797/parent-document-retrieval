from __future__ import annotations

import httpx

from app.settings import settings


class LLMClient:
    def __init__(self) -> None:
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.base_url = settings.openai_base_url.rstrip("/")

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            return (
                "[Mock answer] OPENAI_API_KEY not configured. "
                "Set it in .env to get real LLM responses."
            )

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.2,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]


llm_client = LLMClient()

