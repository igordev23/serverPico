import os
import threading
import serial
from flask import Flask, request, jsonify, render_template
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)

mensagens = []
gps_data = {"latitude": 0.0, "longitude": 0.0}

# Leitura da porta serial em thread separada
def read_serial():
    global gps_data
    try:
        with serial.Serial('COM4', 9600, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("GPS:"):
                    try:
                        parts = line.replace("GPS:", "").split(",")
                        gps_data["latitude"] = float(parts[0])
                        gps_data["longitude"] = float(parts[1])
                        print(f"GPS Atualizado: {gps_data}")
                    except Exception as e:
                        print("Erro ao processar GPS:", e)
    except Exception as e:
        print(f"Erro ao abrir porta serial: {e}")

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

@app.route("/reset", methods=["POST"])
def resetar_mensagens():
    global mensagens
    mensagens = []
    print("Mensagens resetadas.")
    return "Mensagens resetadas"

@app.route("/gps", methods=["GET"])
def get_gps():
    return jsonify(gps_data)

@app.route("/ver-mapa", methods=["GET"])
def ver_mapa():
    return render_template("gps_mapa.html")

@app.route("/", methods=["GET"])
def pagina_inicial():
    return render_template("index.html")

if __name__ == '__main__':
    t = threading.Thread(target=read_serial)
    t.daemon = True
    t.start()

    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
