import os, asyncio
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from backend.clients.base import BaseClient
class LocalClient(BaseClient):
    def __init__(self):
        self.name="local"
        path=os.getenv("LOCAL_MODEL_PATH")
        self.pipe=pipeline("text-generation",
                           model=AutoModelForCausalLM.from_pretrained(path),
                           tokenizer=AutoTokenizer.from_pretrained(path),
                           device="cpu")
    async def generate(self,prompt:str)->str:
        loop=asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda:self.pipe(prompt,max_new_tokens=256)[0]["generated_text"])
