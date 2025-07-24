import os
from flask import Flask, request, render_template
from openai import OpenAI
from datetime import datetime

# ✅ Get API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# ✅ Path for log file
LOG_FILE = "chat_logs.txt"

def save_chat_log(user_message, bot_response):
    """
    Save the conversation to a text file (chat_logs.txt)
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] USER: {user_message}\n")
        f.write(f"[{datetime.now()}] BOT: {bot_response}\n\n")

def chat_with_gpt(user_message):
    """
    Send the user's message to OpenAI GPT model and return the response.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a friendly chatbot on a website."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST", "HEAD"])
def index():
    try:
        # ✅ Render health check
        if request.method == "HEAD":
            return "", 200

        bot_response = ""
        if request.method == "POST":
            user_message = request.form["message"]
            bot_response = chat_with_gpt(user_message)

            # ✅ Log to Render console
            print(f"📩 USER: {user_message}")
            print(f"🤖 BOT: {bot_response}")

            # ✅ Log to local text file
            save_chat_log(user_message, bot_response)

        return render_template("chat.html", bot_response=bot_response)

    except Exception as e:
        print("❌ ERROR:", e)  # Show exact error in Render logs
        return f"An error occurred: {e}", 500

# ✅ Optional: handle HEAD globally
@app.before_request
def handle_head_requests():
    if request.method == "HEAD":
        return "", 200

if __name__ == "__main__":
    # ✅ Use 0.0.0.0 for Render deployment
    app.run(host="0.0.0.0", port=5000, debug=True)
