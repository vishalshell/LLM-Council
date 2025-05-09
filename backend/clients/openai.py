import os, httpx
from backend.clients.base import BaseClient
class OpenAIClient(BaseClient):
    def __init__(self):
        self.name="openai"
        self.key=os.getenv("OPENAI_API_KEY")
        self.url="https://api.openai.com/v1/chat/completions"
        self.headers={"Authorization":f"Bearer {self.key}"}
    async def generate(self,prompt:str)->str:
        data={"model":"gpt-4o-mini","messages":[{"role":"user","content":prompt}],"max_tokens":256}
        async with httpx.AsyncClient(timeout=30) as c:
            r=await c.post(self.url,headers=self.headers,json=data); r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
