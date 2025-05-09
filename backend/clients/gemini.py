import os, httpx
from backend.clients.base import BaseClient
class GeminiClient(BaseClient):
    def __init__(self):
        self.name="gemini"
        self.key=os.getenv("GEMINI_API_KEY")
        self.url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.key}"
    async def generate(self,prompt:str)->str:
        data={"contents":[{"parts":[{"text":prompt}]}]}
        async with httpx.AsyncClient(timeout=30) as c:
            r=await c.post(self.url,json=data); r.raise_for_status()
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
