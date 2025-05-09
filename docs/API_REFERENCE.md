# API Reference

## POST /vet

### Request

```json
{ "prompt": "<string>" }
```

### Response

```json
{
  "prompt":"…",
  "local_answer":"…",
  "anchors": { "openai":"…", "gemini":"…", "claude":"…" },
  "majority_answer":"…",
  "consistency_score":97,
  "verdict":"pass"
}
```