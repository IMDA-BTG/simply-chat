# app.py
import os
from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from az_openai import message_azure_openai_model

app = Flask(__name__)

# Retrieve rate limit values from environment variables or set default values
default_limit = os.getenv('DEFAULT_RATE_LIMIT', '500/day, 10/minute')
chat_limit = os.getenv('CHAT_RATELIMIT', '10/minute')

# Rate limiting (simple implementation)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[default_limit]
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/chat', methods=['POST'])
@limiter.limit(chat_limit)
def chat():
    user_input = request.json.get('message')
    print(f"Received message: {user_input}")
    if not user_input:
        return jsonify({"error": "Invalid input"}), 400

    try:
        response_text = message_azure_openai_model(user_input)
        print(f"Response: {response_text}")
        return jsonify({"answer": response_text})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
