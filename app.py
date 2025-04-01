import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

mensagens = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mensagens Recebidas</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .container { padding: 20px; border: 1px solid #ddd; display: inline-block; }
        .mensagem { background: #f4f4f4; padding: 10px; margin: 5px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Mensagens Recebidas</h2>
        {% if mensagens %}
            {% for msg in mensagens %}
                <div class="mensagem">{{ msg }}</div>
            {% endfor %}
        {% else %}
            <p>Nenhuma mensagem recebida ainda.</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/mensagem", methods=["GET"])
def receber_mensagem():
    mensagem = request.args.get("msg")
    if mensagem:  # Apenas adiciona se houver uma mensagem
        mensagens.append(mensagem)
        print(f"Mensagem recebida: {mensagem}")
    return render_template_string(HTML_TEMPLATE, mensagens=mensagens)

@app.route("/", methods=["GET"])
def pagina_inicial():
    return "<h1>Servidor está rodando!</h1>"

PORT = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=PORT)
