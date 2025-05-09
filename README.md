# LLM Council Vetting Harness

Vets your **local LLM** answer against a three‑model council (GPT‑4o, Gemini 1.5 Pro, Claude 3 Haiku) and tells you whether your model’s response matches the majority.

```
User ──► FastAPI ──► { local , openai , gemini , claude }
                        │
                        ▼
                  Council logic
```
