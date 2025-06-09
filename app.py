from flask import Flask, render_template, request
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    ideias = []
    if request.method == "POST":
        nicho = request.form["nicho"]
        prompt = f"Gere 3 ideias criativas para vídeos curtos no nicho '{nicho}', com gancho e mini-roteiro."
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        ideias = resposta.choices[0].message["content"].split("\n\n")
    return render_template("index.html", ideias=ideias)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
