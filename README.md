# 🎯 CareerBot — AI-Powered Career Guidance Chatbot

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini%20API-4285F4?logo=google&logoColor=white)

CareerBot is an AI chatbot that gives **students** and **organizations** practical answers to career-related questions: career roadmaps, skills to learn, resume and interview tips, hiring, and employee upskilling. It is built on the Google Gemini API with a career-focused system prompt, conversation memory, and a resilient API layer.

> Developed during the Data Science & Analytics Internship at **Zidio Development** under the guidance of **Mr. Chandan Mishra**.

---

## 📌 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack) 
- [Project Structure](#-project-structure) 
- [Getting Started](#-getting-started) 
- [Configuration](#-configuration) 
- [Deployment](#-deployment-streamlit-community-cloud) 
- [Testing](#-testing) 
- [Security](#-security) 
- [Limitations](#-limitations) 
- [Future Improvements](#-future-improvements) 
- [Author](#-author) 

---

## ✨ Features

- **Career-focused answers**: a system prompt keeps replies practical, step-by-step and on topic.
- **Two audiences**: choose *Student / Fresher* or *Organization / HR*, and the answers adapt to each.
- **Conversation memory**: recent messages are sent with every request, so follow-up questions work.
- **Multilingual replies**: English, Hindi and Hinglish.
- **Adjustable creativity**: control the model's temperature from the sidebar.
- **Suggestion buttons**: one-tap starter questions such as *Data science roadmap* or *Resume tips*.
- **Reliable API handling**: automatic retries on temporary overload, an optional backup model, and friendly error messages.
- **Two interfaces**: a Streamlit app (recommended for deployment) and a Flask + HTML/JS app with dark mode, analytics dashboard and chat export.

### Example questions

| For | Example |
|---|---|
| Students | *Give me a roadmap to become a data scientist from scratch* |
| Students | *How should I prepare for a technical interview in 2 weeks?* |
| Students | *What are the best career options after 12th with science (PCM)?* |
| Organizations | *Write a job description for a junior data analyst* |
| Organizations | *How can my company run an effective employee upskilling program?* |

---

## ⚙️ How It Works

<img width="1280" height="579" alt="image" src="https://github.com/user-attachments/assets/92358e18-6429-4a7f-8b5b-8a4526851e1c" />


1. The user picks a profile and language, then asks a question.
2. `chatbot_core.py` builds the system prompt: **base career instructions + audience instruction + language instruction**.
3. The last 20 chat messages and the new question are converted to the Gemini format.
4. The request is sent to the Gemini API. On a temporary overload (HTTP 429 / 500 / 503) it is retried up to three times, then sent to the backup model if one is configured.
5. The reply is shown in the chat and added to the history for the next turn.

All prompt, memory and API logic lives in one shared module, so both interfaces behave the same way.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language model | Google Gemini API |
| Core logic | Python, `requests` |
| Web interface (deployment) | Streamlit |
| Web interface (local) | Flask, HTML, CSS, JavaScript |
| Configuration | `python-dotenv`, Streamlit secrets |

---

## 📁 Project Structure

```
career-chatbot/
├── chatbot_core.py            # shared prompts, history handling, Gemini API call
├── streamlit_app.py           # Streamlit interface (used for deployment)
├── server.py                  # Flask backend for the HTML interface
├── run.py                     # launches the Flask app locally
├── test_api.py                # checks that your API key and model work
├── static/                    # HTML, CSS and JavaScript of the Flask interface
├── .streamlit/
│   └── secrets.toml.example   # template for Streamlit secrets
├── .env.example               # template for local environment variables
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or newer
- A Google Gemini API key. Create one at [Google AI Studio](https://aistudio.google.com/apikey).

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# 2. (Optional) create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 3. Install dependencies
python -m pip install -r requirements.txt
```

### Add your API key

Copy `.env.example` to `.env` and edit it:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Check that the key and model work:

```bash
python test_api.py
```

### Run the app

**Streamlit interface (recommended):**

```bash
python -m streamlit run streamlit_app.py
```

Then open <http://localhost:8501>.

**Flask + HTML interface (local demo):**

```bash
python run.py
```

Then open <http://127.0.0.1:5000>.

> Run only one interface at a time, and don't launch `run.py` from inside Streamlit.

---

## 🔧 Configuration

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Your Gemini API key |
| `GEMINI_MODEL` | No | Model name (default: `gemini-3.8-flash`). Change it if Google retires or renames the model. |
| `GEMINI_FALLBACK_MODEL` | No | Backup model tried if the main model stays overloaded |

Settings are read from Streamlit secrets first, then from environment variables or `.env`.

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push this repository to GitHub. The `.env` file is excluded by `.gitignore`.
2. Go to [share.streamlit.io](https://share.streamlit.io) and choose **New app**.
3. Select your repository and set the main file path to `streamlit_app.py`.
4. Open **App settings → Secrets** and add:

   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   GEMINI_MODEL = "gemini-3.8-flash"
   ```

5. Click **Deploy**.

---

## 🧪 Testing

The core logic was tested with a mocked Gemini API, covering:

- prompt assembly for each audience and language
- conversation history conversion (user / model turns)
- retry on temporary overload (503) and the friendly message after repeated failures
- missing API key handling
- Flask routes (home page and `/chat`)

`python test_api.py` verifies live connectivity with your own key.

---

## 🔒 Security

- The API key is **never stored in the source code**. It is read from `.env` or Streamlit secrets.
- `.gitignore` excludes `.env` and `.streamlit/secrets.toml`.
- Before pushing, check that no key is committed: `git grep -n "AIza"`.
- If a key is ever exposed, revoke it in Google AI Studio and create a new one. Deleting it in a later commit is not enough, because it stays in the Git history.

---

## ⚠️ Limitations

- Answers come from a language model and can be inaccurate or out of date. Always verify salaries, exam dates and job-market demand from official sources.
- CareerBot offers guidance, not guarantees, and does not replace a professional career counsellor.
- Chat history lives only in the browser session. There is no login or permanent storage.
- The app depends on an external API, so availability and speed depend on the provider.

---

## 🔮 Future Improvements

- Resume upload and analysis with skill-gap feedback
- Retrieval-augmented generation (RAG) over a curated roles, skills and courses dataset
- User accounts and saved chat history
- Evaluation on a test set of real student and HR questions
- Streaming responses
- Integration with job and course platforms

---

## 👤 Author

**Sunny**
Data Science & Analytics Intern, Zidio Development
Mentor: Mr. Chandan Mishra

---

If you find this project useful, consider giving it a ⭐ on GitHub.
