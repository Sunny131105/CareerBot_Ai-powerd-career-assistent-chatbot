"""Quick check that your Gemini key + model work: python test_api.py"""
import os

import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('GEMINI_API_KEY')
model = os.getenv('GEMINI_MODEL', 'gemini-3.8-flash')

if not key:
    raise SystemExit("GEMINI_API_KEY not set. Copy .env.example to .env and add your key.")

r = requests.post(
    f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
    json={'contents': [{'parts': [{'text': 'Reply with: API working!'}]}]},
    headers={'x-goog-api-key': key},
    timeout=30,
)
print("Status:", r.status_code)
print(r.json()['candidates'][0]['content']['parts'][0]['text'] if r.ok else r.text)
