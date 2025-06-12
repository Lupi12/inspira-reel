import os
from flask import Flask, render_template, request, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
from whitenoise import WhiteNoise

load_dotenv()

# Configuração do App e do WhiteNoise
app = Flask(__name__)
# Informa ao WhiteNoise onde encontrar os arquivos estáticos
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

# Rota para servir o manifest.json
@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("Chave da API da OpenAI não encontrada.")
except Exception as e:
    print(f"Erro ao inicializar o cliente OpenAI: {e}")
    client = None

@app.route("/", methods=["GET", "POST"])
def home():
    ideias_formatadas = []
    error_message = None

    if not client:
        error_message = "O serviço de IA não está configurado corretamente. Contate o suporte."
        return render_template("index.html", error=error_message)

    if request.method == "POST":
        nicho = request.form.get("nicho", "").strip()

        if nicho:
            prompt = (
                f"Gere 3 ideias criativas para vídeos curtos no nicho '{nicho}', "
                f"com gancho inicial forte, benefício claro e CTA no final. "
                f"Separe cada ideia com '---'."
            )

            try:
                resposta = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.7
                )
                
                ideias_texto = resposta.choices[0].message.content
                ideias_formatadas = [ideia.strip() for ideia in ideias_texto.split('---') if ideia.strip()]

            except Exception as e:
                print(f"Ocorreu um erro na API da OpenAI: {e}")
                error_message = "Desculpe, não consegui gerar as ideias. Verifique se a chave da API está correta ou tente novamente mais tarde."

        else:
            error_message = "Por favor, digite um nicho para gerar as ideias."

    return render_template("index.html", ideias=ideias_formatadas, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)