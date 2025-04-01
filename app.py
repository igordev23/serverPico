import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mensagem Recebida</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .container { padding: 20px; border: 1px solid #ddd; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Mensagem Recebida</h2>
        <p>{{ mensagem }}</p>
    </div>
</body>
</html>
"""

@app.route("/mensagem", methods=["GET"])
def receber_mensagem():
    mensagem = request.args.get("msg", "Nenhuma mensagem recebida")
    print(f"Mensagem recebida: {mensagem}")
    return render_template_string(HTML_TEMPLATE, mensagem=mensagem)
@app.route("/", methods=["GET"])
def pagina_inicial():
    return "<h1>Servidor está rodando!</h1><p>Acesse <a href='/mensagem?msg=Hello'>/mensagem?msg=Hello</a> para testar.</p>"


PORT = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=PORT)
