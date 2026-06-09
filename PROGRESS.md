# 🧭 Project Progress — Multi-Agent Travel System

> **How to use this file:** When you reopen Claude Code, say:
> *"Read PROGRESS.md — let's continue from where we left off."*
> This file is my memory between sessions.

---

## 🎯 Project Description
An **AI travel assistant** that asks the user for their trip details (destination, duration,
budget, interests) and generates a complete **end-to-end itinerary**. Instead of one big AI,
the work is split across a **team of specialist AI agents** that collaborate — each handles
one part (hotels, food, attractions, transport), and a final planner combines everything into
a realistic **day-by-day plan**. As a bonus, one agent uses a **real-time tool** (live weather)
so the plan reacts to actual conditions instead of guessing.

**The point of the project:** learn how to build a *multi-agent* AI system — how agents are
defined, how they pass work to each other, how they call external tools/APIs, and how to take
real user input — by building one from scratch.

- **Framework:** CrewAI (multi-agent)
- **AI brain (LLM):** Google Gemini — model `gemini/gemini-2.5-flash`
- **Real-time tool:** OpenWeatherMap API (live weather)
- **Language:** Python (running inside `venv`)
- **Secrets:** `.env` holds `GEMINI_API_KEY` and `WEATHER_API_KEY` (never commit `.env`)

---

## 🧠 Concepts I've learned so far
| # | Concept | Got it? |
|---|---------|---------|
| 1 | `venv` = isolated library box per project | ✅ |
| 2 | `requirements.txt` = shopping list of libraries (`pip install` buys now; the list remembers) | ✅ |
| 3 | **Agent** = an AI worker (role / goal / backstory / llm) — the *reusable worker*, written generically | ✅ |
| 4 | **Task** = the job for an agent (description / expected_output / agent) — the *specific work order* | ✅ |
| 5 | **Crew** = manager that runs agents+tasks; `.kickoff()` starts it | ✅ |
| 6 | **Task → Agent** direction: a task points to its agent; agents don't hold tasks | ✅ |
| 7 | **`context=[...]`** = pass one task's *output* to another (the "baton") — holds tasks, not agents | ✅ |
| 8 | Only the **`tasks=[...]` order** controls run order (sequential); `agents=[...]` is just the roster | ✅ |
| 9 | **"Define before use"** — a task used in another task's context must be written above it | ✅ |
| 10 | **Tool** = a function an agent can CALL to get real data; `@tool` registers it, docstring tells the agent when to use it | ✅ |
| 11 | **`requests`** = Python "visits" a URL: `requests.get(url, params=...)` → `.status_code` → `.json()` | ✅ |
| 12 | **JSON navigation:** dict by name `data["main"]["temp"]`; list by position `data["weather"][0]` | ✅ |
| 13 | **`tools=[...]`** on an agent hands it a tool; the *agent decides when* to use it (nudge it via the task) | ✅ |
| 14 | **`input()`** asks the user, always returns text | ✅ |
| 15 | **`{placeholders}` + `kickoff(inputs={...})`** = fill task blanks with user values (key must match `{name}`) | ✅ |
| 16 | LLM control knobs (`temperature`, `top_p`, `max_tokens`) live on `LLM(...)` — optional tuning | ✅ |
| — | HTTP codes: 200 ok, 401/403 bad key, 404 not found, 429 quota, 503 server busy | ✅ |
| 17 | **Ambiguous input → ASK, don't guess** — bare "5000" had no currency; the LLM silently guessed USD. Fix: collect `currency`, pass `{currency}` through | ✅ |
| 18 | **Constrain the choices** — real apps use pickers/dropdowns for small fixed sets; free `input()` can't stop bad input (we deferred dropdown, just ask for now) | ✅ |
| 19 | **Rules-check (budget math)** — LLMs are bad at arithmetic AND sound confident; force the planner to show a cost breakdown + total + a "fits/over" line | ✅ |
| 20 | **Tool pattern, reused (web search)** — `@tool` + `requests.post` + key in `headers` + parse `data["organic"]`; `tools=[search_web]` on every agent | ✅ |
| 21 | **POST vs GET / header auth** — search APIs receive the query in the *body* (POST); the key goes in a **header**, not the URL (weather was GET + key in URL) | ✅ |
| 22 | **3 tiers of data**: ① generate=guess → ② web-search=grounded → ③ real API=authoritative (e.g. Amadeus). **We are now Tier 2.** | ✅ |

---

## ✅ What's built so far
**Five agents** running in `Process.sequential`, each with its own task:
1. **Accommodation Agent** — finds hotels within budget
2. **Cuisine Agent** — suggests local foods & beverages
3. **Attractions Agent** — recommends sights/landmarks/museums
4. **Transport Agent** — how to get around (passes, airport transfers)
5. **Itinerary Agent** — combines all of the above into a day-by-day plan
   - uses `context=[accommodation, cuisine, attractions, transport]` (the baton)
   - has the **Weather Tool** (`tools=[get_weather]`) and is told in its task to check live weather

**One real-time tool:** `get_weather(city)` in `tools.py` — calls OpenWeatherMap and returns a
readable weather sentence to the agent.

**User input:** `main.py` now asks the user for destination / duration / budget / interests via
`input()`, then passes them to `kickoff(inputs={...})`, which fills the `{placeholders}` in every
task. **Nothing is hardcoded anymore** (used to be Tokyo / 5 days / ₹80,000 / food + history).

Run order: `accommodation → cuisine → attractions → transport → itinerary`.

**Added on 2026-06-07 (Session 2):**
- **Currency input** — `main.py` now also asks "In what currency?" and passes `{currency}`; every task reads `{budget} {currency}` (e.g. "5000 INR"). Killed the bug where agents silently assumed USD.
- **Budget enforcement** — the itinerary task now makes the planner show a **cost breakdown table + total + a clear "fits/over budget" line**. It correctly flagged ₹5,000/5 days as OVER BUDGET.
- **Web search tool** — `search_web` (Serper API) added to `tools.py`; wired onto **all 5 agents** via `tools=[...]` + each task nudged to "search for real data, do not guess." Moved the whole project from **Tier 1 (guessing) → Tier 2 (grounded in real web data)**.

### Files
- `src/agents.py` — Gemini LLM + the 5 agents; imports `get_weather, search_web`; **every agent has `tools=[search_web]`**; itinerary has `tools=[get_weather, search_web]`
- `src/tasks.py`  — the 5 tasks; all use `{placeholders}` incl. `{currency}`; budget breakdown in itinerary; search nudges in the 4 specialist tasks; itinerary has the `context=[...]` baton
- `src/main.py`   — builds the Crew, asks 5 `input()` questions (incl. currency), runs `kickoff(inputs={...})`
- `src/tools.py`  — `get_weather` (OpenWeatherMap, GET) + `search_web` (Serper, POST + header key)
- `.env`          — now also holds `SERPER_API_KEY` (instant activation, free 2,500 searches)

### How to run
```bash
source venv/bin/activate     # activate the venv (see "(venv)" in prompt)
python -m src.main           # run from the project root; it will ask 4 questions
```

---

## ⚠️ Notes / gotchas learned
- Use `python -m src.main` (NOT `python src/main.py`) so the `from src...` imports work.
- We use **`gemini-2.5-flash`** (`2.0-flash` → 429, `1.5-flash` → 404).
- A **503** = Gemini server busy → just run again. (Hit this a lot lately while testing.)
- **New OpenWeatherMap keys take ~1–2 hours to activate.** A `401` on first runs likely = key not live yet.
- **Agent vs Task mix-up** (caught this twice!): `tasks=[...]` and `context=[...]` need the `_task` names,
  NOT the `_agent` names. Only `agents=[...]` and a task's own `agent=` use `_agent`.
- **Python syntax bugs I hit:** uneven **indentation** (every line in a block lines up); `os.getenv`
  uses a **dot** not a comma; every argument inside `Agent(...)` needs a **comma**; one opening quote, not two.

---

## 🗺️ Roadmap — where we are
```
1. Setup ........................ ✅ done
2. Build one agent .............. ✅ done
3. Give it a task ............... ✅ done
4. Run as a crew ................ ✅ done
5. Add more agents (5 total) .... ✅ done (cuisine, itinerary, attractions, transport)
6. Agents work together (context) ✅ done
7. Add a real-time TOOL (bonus) . ✅ done (weather tool, wired to itinerary agent)
8. Take USER INPUT in main.py ... ✅ done (input() + kickoff(inputs={...}))
9. VERIFY a full run end-to-end . ✅ DONE (2026-06-09) — see below 🎉
```

**🎉 Step 9 verified (2026-06-09):** Ran Hyderabad / 5 days / 7000 INR / history. All 5 agents
fired in order, `web_search_tool` pulled real data ~11×, and the **`weather_tool` fired live**
("28.46°C with light rain" → the OpenWeatherMap key is now ACTIVE). The planner factored the
rain into an indoor/outdoor day plan and printed a budget breakdown + "FITS BUDGET".
**The original project is COMPLETE.**

## ⚠️ What the successful run REVEALED (the Evaluation lesson, live)
The planner **fudged the budget to force "FITS"**:
- Transport agent researched **~3,000 INR**; planner quietly used **1,200**.
- Food = **300 INR for 5 days** = **₹60/day** — impossible. It claimed this was "more realistic"; it's the opposite.
- The LLM worked **backwards from the 7,000 target** ("motivated math") instead of adding honest numbers.

→ Concept #19 (force a breakdown table) was step 1, but the table can still hold made-up numbers.
**The numbers need a *code* check, not just an LLM check.**

## 🚀 Going to production — Phase 1, Step 1 (current focus)
The build works, but it can't be *trusted* (it fudged the budget). Taking it to production = TRUST first.
We are doing **ONE step at a time**. Right now, only this:

**STEP 1: Structured Output (JSON, not free-text markdown).**
- **Problem (what we have):** `itinerary_task.expected_output` asks for a markdown table + prose.
  Free text is for *humans to read*, not for *code to check*. Python can't reliably pull "food = 300"
  out of a sentence, so it can't catch the fudged numbers.
- **Goal:** make the planner emit a fixed **JSON shape** (days[], cost_breakdown{accommodation, transport,
  food, entry_fees}, total, sources[]). Predictable keys = code can read every number.
- **Why first:** every later production step (rules-check, tests, an API, a web UI) needs machine-readable
  output. You can't validate or build on free text. JSON is the foundation.
- **NOT doing yet (deliberately):** the rules-check, eval harness, FastAPI, Docker, parallel agents.
  Those come after Step 1 works.

## 💡 Concepts to revisit LATER (deliberately deferred, not forgotten)
Build first, THEN learn to watch & trust the agents. Two pillars of real agent engineering:
- **Observability** = how to track what each agent is doing. Ladder: logs → `verbose=True` →
  full **tracing** (the "Tracing is disabled" box at the end of every run is CrewAI offering this).
- **Evaluation** = how to know an answer is *correct*. LLMs always sound confident even when wrong
  (hotel prices are guessed, not real). Splits into: rules-check (code), fact-check (real tools/APIs —
  that's why the weather tool matters), quality-check (human or an AI judge).
- **Input validation** = the same "is it correct?" question at the front door (`input()` accepts anything).
