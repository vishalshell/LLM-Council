# LLM Council Vetting Harness 🧪 ( **Development Preview – Expect Bugs!** )

> ⚠️ **Heads-up!**  
> This repository is an early-stage proof-of-concept. APIs, file names, and scoring logic will change often, and some pieces may simply break. **Use at your own risk** and never rely on the verdicts for production decisions yet.

## What problem does it solve?

When you fine-tune or build your own local language-model, it's hard to know **how far it drifts** from well-known, best-in-class models.  
The **LLM Council Vetting Harness** helps by:

1. **Asking three public "anchor" models** – OpenAI GPT-4o, Google Gemini 1.5 Pro, and Anthropic Claude 3 Haiku – the very same prompt you feed your **local LLM**.  
2. **Finding a majority consensus** among those anchors.  
3. **Comparing** your local model's answer to that consensus with a quick Levenshtein similarity score.  
4. Returning a JSON **report** that tells you whether your model "passes" (looks similar) or "fails" (sounds off).

Think of it as a lightweight *sanity-check harness* before you push a new model checkpoint into QA or prod.

## ✨ Key features

| Feature | Notes |
|---------|-------|
| **Parallel generation** | Local + 3 anchors queried concurrently. |
| **Council logic** | Any answer that ≥ 2 / 3 anchors share becomes the "majority." |
| **Text similarity score** | 0-100 (RapidFuzz Levenshtein). |
| **Single REST endpoint** | `POST /vet` → returns a ready-to-log JSON blob. |
| **Container-first** | `docker compose up --build` runs the lot on port 8000. |
| **Easy to extend** | Add or remove anchor clients in one place (`backend/clients`). |

## 🖼 Architecture (ASCII)

```
User
│  POST /vet
▼
+------------------+        spawn N coroutines
|  FastAPI Server  |  ──────────────┬─────────────────────┐
|  app/main.py     |                │                     │
+---------+--------+                │                     │
          │                         │                     │
          │                         ▼                     ▼
          │                +--------------+      +--------------+
          │                |  Local  LLM  |      |  Anchor LLMs |
          │                +--------------+      | (GPT-4o etc) |
          ▼                        |             +--------------+
+-----------------------+          |                     │
| Council / Orchestrator | <───────┘                     │
| backend/orchestrator.py|                               │
+-----------+-----------+                                │
          │                                              │
          ▼                                              ▼
JSON Report  ─────────────────────────────────────────▶  Client
```

## ⚙️ Quick start

```bash
git clone https://github.com/your-org/llm_council_project.git
cd llm_council_project

# 1. Add secrets
cp .env.example .env
#    - OPENAI_API_KEY
#    - GEMINI_API_KEY
#    - ANTHROPIC_API_KEY
#    - LOCAL_MODEL_PATH (folder or GGUF / GGML file)

# 2. Build & run
docker compose up --build
# or:  python -m venv .venv && source .venv/bin/activate
#      pip install -r requirements.txt
#      uvicorn app.main:app --reload

# 3. Test it
curl -X POST http://localhost:8000/vet \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Who is the prime minister of Malaysia?"}'
```

Sample response:

```jsonc
{
  "prompt": "Who is the prime minister of Malaysia?",
  "local_answer": "Dato' Sri Anwar Ibrahim.",
  "anchors": {
    "openai":  "Datuk Seri Anwar Ibrahim is the current PM.",
    "gemini":  "Malaysia's current prime minister is Anwar Ibrahim.",
    "claude":  "Anwar Ibrahim."
  },
  "majority_answer": "anwar ibrahim.",
  "consistency_score": 92,
  "verdict": "pass"
}
```

## 🔧 Configuration reference

| Variable            | Description                                   |
| ------------------- | --------------------------------------------- |
| `OPENAI_API_KEY`    | Access to GPT-4o.                             |
| `GEMINI_API_KEY`    | Access to Gemini 1.5 Pro.                     |
| `ANTHROPIC_API_KEY` | Access to Claude 3 Haiku.                     |
| `LOCAL_MODEL_PATH`  | Location of your local HF model or GGML file. |

## 📈 How the verdict is decided

1. **Majority step**
   *Lower-cased, stripped answers* → if 2 or more anchors match exactly, that text is the majority.
   If no outright majority, the first anchor's answer becomes the tie-breaker (🤷 until we add better logic).

2. **Similarity step**

   ```
   score = 100 - LevenshteinDistance(local, majority) × 100 / len(local)
   ```

3. **Threshold** – default pass mark = **85 %**.
   Change it in `backend/orchestrator.py` if you need stricter or looser checks.

## 🛠 Extending / hacking

* **Swap anchors** – comment out or add new client classes in `backend/clients/`.
* **Better majority logic** – replace `_majority()` with semantic clustering (e.g. `rapidfuzz.process.extract`, semantic-search, etc.).
* **Alternative similarity** – drop in cosine similarity, BLEU, BERTScore… your call.

## 🧪 Tests

```bash
pytest -q
```

A stub test demonstrates monkey-patching all clients with dummy answers to keep CI fast.

## ❗ Caveats & TODOs

* Uses simple string equality for majority – fails on near-identical wording.
* No streaming / chunked responses yet.
* No memory or DB; everything lives in RAM.
* Error handling around the cloud APIs is bare-bones.
* You *must* download / mount a local model yourself – repo doesn't include weights.

## License

MIT © 2025 – contribute freely!
