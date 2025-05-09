# Detailed Architecture

ASCII diagram (same as README) and component descriptions.

```
User --> FastAPI (app/main.py)
            |-- local client
            |-- openai client
            |-- gemini client
            |-- claude client
            `-- council verdict
```

### Components

| Module | Responsibility |
|--------|----------------|
| `backend/clients/*` | Thin async wrappers for each model API |
| `backend/orchestrator.py` | Runs all models, computes majority & similarity |
| `app/main.py` | FastAPI entry point |