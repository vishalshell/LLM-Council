from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.orchestrator import vet_prompt

class Req(BaseModel):
    prompt:str

app = FastAPI()

@app.post("/vet")
async def vet(r:Req):
    try:
        return await vet_prompt(r.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
