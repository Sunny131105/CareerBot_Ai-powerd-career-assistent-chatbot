# CareerBot - AI Career Guidance Chatbot

A Flask + vanilla JavaScript web chatbot (Google Gemini API) that answers career questions for **students** and **organizations**.

## What it does
- Students: career roadmaps, skills, courses, projects, resume/LinkedIn, interview prep, internships, course/stream choice
- Organizations: hiring plans, job descriptions, employee upskilling, career ladders, retention
- Remembers the conversation (follow-up questions work)
- Profile selector (Student / Organization), languages: English, Hindi, Hinglish
- Quick-suggestion buttons, light/dark theme, analytics dashboard, chat export

## Two ways to run
- **Streamlit (recommended for deployment):** `streamlit run streamlit_app.py`
- **Flask + HTML UI (local):** `python run.py`

Don't run `run.py` inside Streamlit; they are separate apps sharing `chatbot_core.py`.

## Setup
1. `pip install -r requirements.txt`
2. Create a **new** key at https://aistudio.google.com/apikey
3. Copy `.env.example` to `.env` and set `GEMINI_API_KEY` (change `GEMINI_MODEL` if Google renames it)
4. Optional check: `python test_api.py`
5. `python run.py` then open http://127.0.0.1:5000

## How it works
- `server.py` builds a career-focused system prompt (+ audience + language), adds recent chat history, calls Gemini, returns the reply
- `static/app.js` sends message, history, audience, language and creativity setting to `/chat`
- API key lives only in `.env` (never commit it)

## Ideas to extend
Resume upload and analysis, a curated roles/skills knowledge base (RAG), user login with saved chats, deployment (Render/Railway).

## Deploy on Streamlit Community Cloud
1. Push the repo to GitHub (`.env` is git-ignored)
2. share.streamlit.io -> New app -> main file: `streamlit_app.py`
3. App settings -> Secrets -> paste `GEMINI_API_KEY = "..."` and `GEMINI_MODEL = "gemini-3.8-flash"`
