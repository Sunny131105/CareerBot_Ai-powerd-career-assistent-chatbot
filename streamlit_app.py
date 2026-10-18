"""CareerBot - Streamlit version.  Run locally: streamlit run streamlit_app.py"""
import os

import streamlit as st
from dotenv import load_dotenv

from chatbot_core import get_reply

load_dotenv()


def get_setting(name, default=''):
    """Read from Streamlit secrets (cloud) first, then environment/.env (local)."""
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.getenv(name, default)


API_KEY = get_setting('GEMINI_API_KEY')
MODEL = get_setting('GEMINI_MODEL', 'gemini-3.8-flash')
FALLBACK_MODEL = get_setting('GEMINI_FALLBACK_MODEL')

st.set_page_config(page_title='CareerBot - AI Career Assistant', page_icon='🎯', layout='centered')

WELCOME = ("Hello! I'm CareerBot, your AI career guide. I help students with career paths, skills, "
           "resumes, interviews and internships, and help organizations with hiring, upskilling and "
           "employee growth. Ask me anything about careers.")

SUGGESTIONS = {
    '📊 Data science roadmap': 'Give me a roadmap to become a data scientist from scratch',
    '🎓 Options after 12th': 'What are the best career options after 12th with science (PCM)?',
    '📄 Resume tips': 'How can I make my resume ATS-friendly? Give me a checklist',
    '🎯 Interview prep': 'How should I prepare for a technical interview in 2 weeks?',
    '🏢 Employee upskilling': 'How can my company run an effective employee upskilling program?',
    '📝 Job description': 'Write a job description for a junior data analyst',
}

AUDIENCES = {'Student or Organization': 'both', 'Student / Fresher': 'student', 'Organization / HR': 'organization'}
LANGUAGES = {'English': 'en', 'Hindi': 'hi', 'Hinglish': 'hinglish'}

# ---- sidebar settings ----
with st.sidebar:
    st.header('Settings')
    audience = AUDIENCES[st.selectbox('I am a', list(AUDIENCES))]
    language = LANGUAGES[st.selectbox('Language', list(LANGUAGES))]
    temperature = st.slider('Creativity', 0.0, 1.0, 0.7, 0.1)
    if st.button('🗑️ Clear chat'):
        st.session_state.messages = []
        st.rerun()

st.title('🎯 CareerBot')
st.caption('Career guidance for students & organizations')

if not API_KEY:
    st.error('GEMINI_API_KEY is not set. Add it in .env (local) or in Streamlit Cloud → App settings → Secrets.')
    st.stop()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# ---- chat history ----
with st.chat_message('assistant'):
    st.write(WELCOME)
for m in st.session_state.messages:
    with st.chat_message(m['role']):
        st.markdown(m['text'])

# ---- suggestion buttons (only before the first message) ----
clicked = None
if not st.session_state.messages:
    cols = st.columns(2)
    for i, (label, text) in enumerate(SUGGESTIONS.items()):
        if cols[i % 2].button(label, use_container_width=True):
            clicked = text

prompt = st.chat_input('Ask a career question...') or clicked

if prompt:
    history = list(st.session_state.messages)
    st.session_state.messages.append({'role': 'user', 'text': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
            reply = get_reply(prompt, history, audience, language, temperature, API_KEY, MODEL, FALLBACK_MODEL)
        st.markdown(reply)
    st.session_state.messages.append({'role': 'model', 'text': reply})
