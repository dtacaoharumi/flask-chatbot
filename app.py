from flask import Flask, request, render_template
from openai import OpenAI
import os

# ✅ Get API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
...


def chat_with_gpt(user_message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # You can also use "gpt-4o"
        messages=[
            {"role": "system", "content": "You are a friendly chatbot on a website."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    bot_response = ""
    if request.method == "POST":
        user_message = request.form["message"]
        bot_response = chat_with_gpt(user_message)
    return render_template("chat.html", bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
