import os
from flask import Flask, request, jsonify, render_template_string

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
    <script>
        function atualizarMensagens() {
            fetch('/mensagens')
                .then(response => response.json())
                .then(data => {
                    let mensagensDiv = document.getElementById('mensagens');
                    mensagensDiv.innerHTML = '';
                    if (data.length > 0) {
                        data.forEach(msg => {
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
        setInterval(atualizarMensagens, 100); // Atualiza a cada 0.1 segundo
    </script>
</head>
<body>
    <div class="container">
        <h2>Mensagens Recebidas</h2>
        <div id="mensagens">
            <p>Nenhuma mensagem recebida ainda.</p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/mensagem", methods=["GET"])
def receber_mensagem():
    mensagem = request.args.get("msg")
    if mensagem:
        mensagens.append(mensagem)
        print(f"Mensagem recebida: {mensagem}")
    return "Mensagem recebida"

@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    return jsonify(mensagens)

@app.route("/", methods=["GET"])
def pagina_inicial():
    return render_template_string(HTML_TEMPLATE)

PORT = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=PORT)