from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    prompt = (
        f"You are Krishna, a compassionate assistant trained to help users with antidepressant questions.\n"
        f"User: {user_message}\nKrishna:"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma3", "prompt": prompt, "stream": False}
        )
        if response.ok:
            reply = response.json()["response"].strip()
        else:
            reply = "Sorry, I couldn't generate a response."
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
