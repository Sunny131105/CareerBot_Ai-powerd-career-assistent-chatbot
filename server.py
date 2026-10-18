import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from chatbot_core import get_reply

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

API_KEY = os.getenv('GEMINI_API_KEY', '')
MODEL = os.getenv('GEMINI_MODEL', 'gemini-3.8-flash')
FALLBACK_MODEL = os.getenv('GEMINI_FALLBACK_MODEL', '')


@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = (data.get('message') or '').strip()
    if not user_message:
        return jsonify({'reply': 'Please enter a message.'})
    try:
        reply = get_reply(
            user_message, data.get('history'), data.get('audience', 'both'), data.get('language', 'en'),
            data.get('temperature', 0.7), API_KEY, MODEL, FALLBACK_MODEL,
        )
        return jsonify({'reply': reply})
    except Exception:
        app.logger.exception('Unexpected error in /chat')
        return jsonify({'reply': 'An unexpected error occurred. Please try again.'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
