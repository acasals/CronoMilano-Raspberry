from flask import Flask, render_template, request, jsonify
from config.modalidades import MODALIDADES
import os

# Estas dos variables las inyectará app.py
state = None
crono = None

app = Flask(__name__)

def run_web_server(shared_state, shared_crono):
    global state, crono
    state = shared_state
    crono = shared_crono
    
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

# ---------------------------------------------------------
# PÁGINA PRINCIPAL: muestra parámetros actuales
# ---------------------------------------------------------
@app.route("/")
def index():
    cfg = state.get_dict()
    return render_template(
        "index.html",
        modalidades=MODALIDADES,
        modalidad_actual=cfg["modalidad_inicial"],
        campos=cfg
    )

# ---------------------------------------------------------
# AJAX: cargar valores de una modalidad
# ---------------------------------------------------------
@app.route("/ajax_modalidad", methods=["POST"])
def ajax_modalidad():
    modalidad = request.json["modalidad"]
    campos = MODALIDADES[modalidad]
    return jsonify(campos)

# ---------------------------------------------------------
# START: recibe parámetros editados y arranca el concurso
# ---------------------------------------------------------
@app.route("/start", methods=["POST"])
def start():
    # 1. Recoger modalidad seleccionada
    modalidad = request.form["modalidad"]

    # 2. Construir diccionario completo con valores editados
    valores = {}

    # Valores base de la modalidad
    for campo, valor_original in MODALIDADES[modalidad].items():
        if campo == "modalidad":
            valores[campo] = valor_original
        else:
            valores[campo] = int(request.form[campo])

    # 3. Añadir parámetros propios del concurso
    valores["modalidad_inicial"] = modalidad
    valores["num_grupos"] = int(request.form["num_grupos"])
    valores["num_mangas"] = int(request.form["num_mangas"])
    valores["empezar_manga"] = int(request.form["empezar_manga"])
    valores["empezar_grupo"] = int(request.form["empezar_grupo"])

    # 4. Actualizar estado
    state.update(valores)

    # 5. Arrancar concurso
    state.start()

    print("Arrancando concurso con:", valores)
    return "OK"


# ---------------------------------------------------------
# CONCURSO EN MARCHA
# ---------------------------------------------------------
@app.route("/concurso")
def concurso():
    return render_template("concurso.html")

# ---------------------------------------------------------
# AJAX: devuelve el estado actual del concurso
# ---------------------------------------------------------
@app.route("/estado")
def estado():
    return jsonify(state.get_dict())

# ---------------------------------------------------------
# ACORTAR Y ALARGAR
# ---------------------------------------------------------
@app.post("/acortar")
def acortar():
    state.pedir_acortar()
    return "OK"

@app.post("/alargar")
def alargar():
    state.pedir_alargar()
    return "OK"


# ---------------------------------------------------------
# STOP
# ---------------------------------------------------------
@app.route("/stop", methods=["POST"])
def stop():
    state.stop()
    return "OK"


# ---------------------------------------------------------
# APAGAR SISTEMA
# ---------------------------------------------------------
@app.post("/apagar")
def apagar():
    os.system("sudo shutdown -h now")
    return "Apagando..."
