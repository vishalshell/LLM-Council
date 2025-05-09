import asyncio
from rapidfuzz.distance import Levenshtein
from backend.clients.local import LocalClient
from backend.clients.openai import OpenAIClient
from backend.clients.gemini import GeminiClient
from backend.clients.claude import ClaudeClient

_local=LocalClient()
_anchors=[OpenAIClient(),GeminiClient(),ClaudeClient()]

def _majority(lst):
    counts={}
    for x in lst:
        key=x.strip().lower()
        counts[key]=counts.get(key,0)+1
    for ans,count in counts.items():
        if count>=2:
            return ans
    return None

async def vet_prompt(prompt:str):
    results=await asyncio.gather(_local.generate(prompt),* [c.generate(prompt) for c in _anchors])
    local_answer=results[0]
    anchor_answers=results[1:]
    anchor_map={c.name:a for c,a in zip(_anchors,anchor_answers)}
    maj=_majority(anchor_answers) or anchor_answers[0]
    sim=100-Levenshtein.distance(local_answer.lower(), maj.lower())*100/max(len(local_answer),1)
    verdict="pass" if sim>=85 else "fail"
    return {"prompt":prompt,"local_answer":local_answer,"anchors":anchor_map,"majority_answer":maj,"consistency_score":int(sim),"verdict":verdict}
