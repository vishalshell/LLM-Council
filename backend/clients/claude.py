import os, httpx
from backend.clients.base import BaseClient
class ClaudeClient(BaseClient):
    def __init__(self):
        self.name="claude"
        self.key=os.getenv("ANTHROPIC_API_KEY")
        self.url="https://api.anthropic.com/v1/messages"
        self.headers={"x-api-key":self.key,"anthropic-version":"2023-06-01"}
    async def generate(self,prompt:str)->str:
        data={"model":"claude-3-haiku-20240307","max_tokens":256,"messages":[{"role":"user","content":prompt}]}
        async with httpx.AsyncClient(timeout=30) as c:
            r=await c.post(self.url,headers=self.headers,json=data); r.raise_for_status()
            return r.json()["content"][0]["text"]
