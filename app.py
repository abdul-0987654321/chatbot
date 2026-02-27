import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Wix se requests allow karne ke liye zaroori hai

# 🔐 Groq API Configuration
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Memory (Context)
chat_history = [
    {"role": "system", "content": "You are a professional AI assistant. Use markdown for tables, lists, and code."}
]

@app.route('/')
def home():
    return "AI Server is Live!"

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"reply": "Empty message"}), 400

        chat_history.append({"role": "user", "content": user_message})

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": chat_history[-10:], # Last 10 messages for context
            "max_tokens": 1000
        }
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
            chat_history.append({"role": "assistant", "content": bot_reply})
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"reply": "API Error"}), response.status_code

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Render port setting
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
