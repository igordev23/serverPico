import os
from flask import Flask, request, jsonify, render_template_string
from urllib.parse import unquote

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
        .mensagem { background: #f4f4f4; padding: 10px; margin: 5px; border-radius: 5px; font-size: 18px; }
        .botao { margin-top: 10px; padding: 10px; background: red; color: white; border: none; cursor: pointer; border-radius: 5px; font-size: 16px; }
    </style>
    <script>
        function atualizarMensagens() {
            fetch('/mensagens')
                .then(response => response.json())
                .then(data => {
                    let mensagensDiv = document.getElementById('mensagens');
                    mensagensDiv.innerHTML = '';
                    if (data.length > 0) {
                        data.reverse().forEach(msg => {
                            let div = document.createElement('div');
                            div.className = 'mensagem';
                            div.textContent = msg;
                            mensagensDiv.appendChild(div);
                        });
                    } else {
                        mensagensDiv.innerHTML = '<p>Nenhuma mensagem recebida ainda.</p>';
                    }
                });
        }
        function resetarMensagens() {
            fetch('/reset', { method: 'POST' })
                .then(() => atualizarMensagens());
        }
        setInterval(atualizarMensagens, 2000);
    </script>
</head>
<body>
    <div class="container">
        <h2>Mensagens Recebidas</h2>
        <div id="mensagens">
            <p>Nenhuma mensagem recebida ainda.</p>
        </div>
        <button class="botao" onclick="resetarMensagens()">Resetar Mensagens</button>
    </div>
</body>
</html>
"""

@app.route("/mensagem", methods=["GET"])
def receber_mensagem():
    mensagem = request.args.get("msg")
    if mensagem:
        mensagem = unquote(mensagem)  # Decodifica caracteres especiais na URL
        if len(mensagens) == 0 or mensagens[-1] != mensagem:  # Evita duplicatas consecutivas
            mensagens.append(mensagem)
            print(f"Mensagem recebida: {mensagem}")
    return "Mensagem recebida"

@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    return jsonify(mensagens)

@app.route("/reset", methods=["POST"])
def resetar_mensagens():
    global mensagens
    mensagens = []
    print("Mensagens resetadas.")
    return "Mensagens resetadas"

@app.route("/", methods=["GET"])
def pagina_inicial():
    return render_template_string(HTML_TEMPLATE)

PORT = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=PORT)
