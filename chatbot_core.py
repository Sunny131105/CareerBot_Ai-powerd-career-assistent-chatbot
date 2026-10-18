"""Shared CareerBot logic (prompts + Gemini call), used by both the Flask app and the Streamlit app."""
import time

import requests

MAX_HISTORY_TURNS = 20  # last N messages sent for context

BASE_PROMPT = """You are CareerBot, an AI career guidance assistant.
You help students and organizations with career-related questions only:
- Career paths and roadmaps (e.g. data science, web development, core engineering, government exams, MBA)
- Skills to learn, courses, certifications, projects and portfolio building
- Resume/CV, LinkedIn, cover letters, interview preparation, internships and job search
- Choosing streams/courses/colleges, switching careers, salary and growth outlook (give general ranges, say they vary)
- For organizations: hiring plans, job descriptions, employee upskilling, onboarding, retention and career-growth programs

Rules:
- Give practical, specific, step-by-step answers. Use short headings or bullet points, and keep answers focused.
- Ask one short clarifying question if key details (education, interests, experience level) are missing, but still give a useful first answer.
- Be honest: never promise jobs or guaranteed outcomes, and say when information may change (salaries, demand, exam dates).
- If the question is unrelated to careers, education or workplace skills, politely say you focus on career guidance and steer back.
- Be encouraging and respectful; the user may be anxious about their future."""

AUDIENCE_PROMPTS = {
    'student': "The user is a student or fresher. Focus on learning roadmaps, skills, projects, internships, resumes and first-job strategy. Keep language simple.",
    'organization': "The user represents an organization/HR/team lead. Focus on hiring, job descriptions, workforce upskilling, training plans, career ladders and retention.",
    'both': "The user may be a student or an organization. Infer which from their question.",
}

LANGUAGE_PROMPTS = {
    'en': "Reply in English.",
    'hi': "Reply in Hindi (Devanagari script).",
    'hinglish': "Reply in Hinglish (Hindi written in Roman/English letters, mixed with English words).",
}


def build_system_prompt(audience, language):
    return "\n\n".join([
        BASE_PROMPT,
        AUDIENCE_PROMPTS.get(audience, AUDIENCE_PROMPTS['both']),
        LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS['en']),
    ])


def build_contents(history, user_message):
    """history: list of {'role': 'user'|'model'|'assistant', 'text': str}"""
    contents = []
    for item in (history or [])[-MAX_HISTORY_TURNS:]:
        text = (item.get('text') or '').strip()
        if not text:
            continue
        role = 'user' if item.get('role') == 'user' else 'model'
        contents.append({'role': role, 'parts': [{'text': text}]})
    contents.append({'role': 'user', 'parts': [{'text': user_message}]})
    return contents


def api_url(model):
    return f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'


def call_gemini(payload, api_key, model, fallback_model=''):
    """Call Gemini; retry on temporary overload (429/500/503), then try the backup model."""
    models = [model] + ([fallback_model] if fallback_model else [])
    response = None
    for m in models:
        for attempt in range(3):
            response = requests.post(
                api_url(m),
                json=payload,
                headers={'Content-Type': 'application/json', 'x-goog-api-key': api_key},
                timeout=30,
            )
            if response.status_code not in (429, 500, 503):
                return response
            time.sleep(1.5 * (attempt + 1))
    return response


def get_reply(user_message, history, audience, language, temperature, api_key, model, fallback_model=''):
    """Return the reply text (or a friendly error message) for one user message."""
    if not api_key:
        return 'Missing GEMINI_API_KEY. Add it to your secrets/.env and restart.'
    try:
        temperature = min(max(float(temperature), 0.0), 1.0)
    except (TypeError, ValueError):
        temperature = 0.7

    payload = {
        'system_instruction': {'parts': [{'text': build_system_prompt(audience, language)}]},
        'contents': build_contents(history, user_message),
        'generationConfig': {'temperature': temperature, 'topK': 40, 'topP': 0.95, 'maxOutputTokens': 1500},
    }
    try:
        response = call_gemini(payload, api_key, model, fallback_model)
    except requests.exceptions.Timeout:
        return 'Request timed out. Please try again.'
    except requests.exceptions.RequestException:
        return 'Network error occurred. Please check your connection.'

    if response.status_code == 200:
        candidates = response.json().get('candidates') or []
        parts = (candidates[0].get('content') or {}).get('parts') if candidates else None
        if parts:
            return parts[0].get('text', '')
        return 'Sorry, I received an empty response. Please try rephrasing.'
    if response.status_code in (429, 503):
        return 'The AI service is busy right now. Please try again in a minute.'
    return f'API Error: {response.status_code}. Check your API key/model name and try again.'
