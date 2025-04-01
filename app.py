from flask import Flask, request

app = Flask(__name__)

@app.route("/mensagem", methods=["GET"])
def receber_mensagem():
    mensagem = request.args.get("msg", "Nenhuma mensagem recebida")
    print(f"Mensagem recebida: {mensagem}")
    return "Mensagem recebida", 200

app.run(host="0.0.0.0", port=5000)
