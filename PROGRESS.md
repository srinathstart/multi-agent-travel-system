# 🧭 Project Progress — Multi-Agent Travel System

> **How to use this file:** When you reopen Claude Code, say:
> *"Read PROGRESS.md — let's continue from where we left off."*
> This file is my memory between sessions.

---

## 🎯 The Project
An AI travel assistant that takes user input (destination, duration, budget, interests)
and generates an **end-to-end itinerary**: travel options, accommodation, attractions,
and local cuisine/beverages. **Bonus:** integrate real-time data / external APIs.

- **Framework:** CrewAI (multi-agent)
- **AI brain (LLM):** Google Gemini — model `gemini/gemini-2.5-flash`
- **Language:** Python (running inside `venv`)
- **API key:** stored in `.env` as `GEMINI_API_KEY` (never commit this file)

---

## 🧠 Concepts I've learned so far
| # | Concept | Got it? |
|---|---------|---------|
| 1 | `venv` = isolated library box per project | ✅ |
| 2 | `requirements.txt` = shopping list of libraries; `-r` = read from file | ✅ |
| 3 | **Agent** = an AI worker (role / goal / backstory / llm) | ✅ |
| 4 | **Task** = the job for an agent (description / expected_output / agent) | ✅ |
| 5 | **Crew** = manager that runs agents+tasks; `.kickoff()` starts it | ✅ |
| 6 | Adding more agents = same pattern (define → task → register in crew) | ✅ |
| 7 | **`context=[...]`** = pass one task's result to another (the "baton") | ✅ |
| — | HTTP status codes: 200 ok, 401/403 bad key, 404 not found, 429 quota, 503 server busy | ✅ |

---

## ✅ What's built so far
Three agents working together in `Process.sequential`:
1. **Accommodation Agent** — finds hotels within budget
2. **Cuisine Agent** — suggests local foods & beverages
3. **Itinerary Agent** — combines the above into a day-by-day plan
   (uses `context=[accommodation_task, cuisine_task]`)

Currently the trip details are **hardcoded** (Tokyo, 5 days, ₹80,000, food + history).

### Files
- `src/agents.py` — the 3 agents + Gemini LLM setup
- `src/tasks.py`  — the 3 tasks
- `src/main.py`   — builds the Crew and runs `.kickoff()`
- `src/tools.py`  — still EMPTY (for the real-time API bonus, coming later)

### How to run
```bash
source venv/bin/activate     # activate the venv (see "(venv)" in prompt)
python -m src.main           # run from the project root
```

---

## ⚠️ Notes / gotchas learned
- Use `python -m src.main` (NOT `python src/main.py`) so the `from src...` imports work.
- `gemini-2.0-flash` gave a 429 (limit 0) and `gemini-1.5-flash` gave 404 → we use **`gemini-2.5-flash`**.
- A **503** error = Gemini server busy → just run again. With 3 agents this happens occasionally.

---

## 🗺️ Roadmap — where we are
```
1. Setup ........................ ✅ done
2. Build one agent .............. ✅ done
3. Give it a task ............... ✅ done
4. Run as a crew ................ ✅ done
5. Add more agents .............. ✅ done (cuisine + itinerary)
6. Agents work together (context) ✅ done
7. Add a real-time TOOL (bonus) . ⬅️ NEXT
8. Take USER INPUT in main.py ... ⬜ todo
   -- also still to add: Transport Agent + Attractions Agent
```

## 👉 NEXT TIME, start here
1. Re-run `python -m src.main` to confirm the 3-agent itinerary works (the 503 was just server-busy).
2. Then: add an **Attractions Agent** and a **Transport Agent** (same pattern as before).
3. Then: build the first **Tool** in `tools.py` (e.g. real-time weather or web search) — the bonus points.
4. Finally: make `main.py` ask the user for destination/budget/etc. instead of hardcoding.
