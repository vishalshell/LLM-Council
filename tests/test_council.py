import pytest, asyncio
from backend import orchestrator
@pytest.mark.asyncio
async def test_stub(monkeypatch):
    async def stub(prompt): return "same"
    orchestrator._local.generate=stub
    for c in orchestrator._anchors:
        c.generate=stub
    out=await orchestrator.vet_prompt("hi")
    assert out["verdict"]=="pass"
