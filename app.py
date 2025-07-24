import os
from flask import Flask, request, render_template
from openai import OpenAI

# ✅ Get API key from environment variable (safer for deployment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def chat_with_gpt(user_message):
    """
    Send the user's message to OpenAI GPT model and return the response.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # You can also use "gpt-4o"
        messages=[
            {"role": "system", "content": "You are a friendly chatbot on a website."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST", "HEAD"])
def index():
    """
    Main route for chatbot:
    - HEAD request → used by Render for health check, returns 200 OK
    - GET → loads the chat page
    - POST → user submits a message, bot replies
    """
    # ✅ Fix for Render HEAD health check
    if request.method == "HEAD":
        return "", 200  

    bot_response = ""
    if request.method == "POST":
        user_message = request.form["message"]
        bot_response = chat_with_gpt(user_message)

    return render_template("chat.html", bot_response=bot_response)

# ✅ Optional global handler for HEAD requests
@app.before_request
def handle_head_requests():
    if request.method == "HEAD":
        return "", 200

if __name__ == "__main__":
    # ✅ Use 0.0.0.0 for Render deployment
    app.run(host="0.0.0.0", port=5000, debug=True)
