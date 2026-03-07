from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from llm import chat

load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()
    history = data.get('history', [])
    if not user_message:
        return jsonify(error="No message provided"), 400
    try:
        reply = chat(history, user_message)
        return jsonify(reply=reply)
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    import os
    base_port = int(os.getenv('PORT', 5003))
    for offset in range(10):
        port = base_port + offset
        try:
            print(f"Starting server on port {port}…")
            app.run(host='0.0.0.0', port=port, debug=True)
            break
        except OSError as exc:
            if "Address already in use" in str(exc):
                print(f"Port {port} busy, trying next…")
            else:
                raise
    else:
        app.run(host='0.0.0.0', port=0, debug=True)
