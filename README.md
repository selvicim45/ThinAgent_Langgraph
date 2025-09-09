# ThinAgent (LangGraph) — Calculator Agent

A beginner-friendly **thin agent** built with **LangGraph + LangChain**.  
It reads a natural-language math request (e.g., "multiply 6 by 7 then add 4"), decides which **tool** to call (`add`/`sub`/`mul`/`div`), and can optionally **reflect** (review its own answer) up to 2 times for quality.

---

## ✨ What this Calculator Agent does

- Parses plain-English math prompts.
- Uses an LLM to decide which tool(s) to call:
  - `add(num1, num2)`, `sub(...)`, `mul(...)`, `div(...)`
- Orchestrates the flow with **LangGraph**:
  - Nodes: **LLM → Tools → (optional) Reflection → Final Answer**
  - Conditional edges choose whether to run tools again, reflect, or finish.

---

## 🧱 Suggested project structure
<pre>
ThinAgent_Langgraph/
├─ calculator_agent.py      # Main agent (LangGraph) + tools + demo run
├─ requirements.txt         # Python deps
├─ test_project.py          # Integration–style tests for the agent
├─ .env.example             # Template for env vars (no secrets)
├─ .gitignore               # Ignore .env, caches, etc.
└─ README.md
</pre>

---

## ✅ Prerequisites

- Python **3.10+**  
- An **OpenAI API key** (or compatible provider)  
- Git

---
## 🚀 Setup (step-by-step)

## 1) Clone the repo
```bash
git clone https://github.com/selvicim45/ThinAgent_Langgraph.git
cd ThinAgent_Langgraph
```
## 2) Create & activate a virtual environment
 macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Windows (PowerShell)
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```
## 3) Install dependencies
Create requirements.txt (if not present) with:
```bash
python-dotenv
langchain
langchain-openai
langgraph
openai
pytest
```
## Install:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
## Testing
Run all tests:
```bash
pytest -q
```


