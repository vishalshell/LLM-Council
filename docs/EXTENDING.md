# Extending LLM Council

## Add a new anchor

1. Create `backend/clients/myanchor.py` implementing `generate(prompt)`.
2. Import and append an instance to `_anchors` in `backend/orchestrator.py`.

## Change similarity metric

Replace the Levenshtein line with your preferred metric (e.g., BERTScore).