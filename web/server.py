from flask import Flask, render_template, request, jsonify,current_app
from config.modalidades import MODALIDADES, MODALIDADES_VISIBLES, MODALIDADES_TODOS
import os

# Estas dos variables las inyectará app.py
state = None
crono = None

app = Flask(__name__)

def run_web_server(shared_state, shared_crono):
    app.config["STATE"] = shared_state
    app.config["CRONO"] = shared_crono
    
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

# ---------------------------------------------------------
# PÁGINA PRINCIPAL: muestra parámetros actuales
# ---------------------------------------------------------
@app.route("/")
def index():
    state = current_app.config["STATE"]
    cfg = state.get_dict()
    modalidad_actual =cfg["modalidad"]
    visibles = MODALIDADES_VISIBLES.get(modalidad_actual, {})
    modalidades_todos=MODALIDADES_TODOS
    
    return render_template(
        "index.html",
        modalidades=MODALIDADES,
        modalidad_actual=cfg["modalidad"],
        estado=cfg,
        modalidades_todos = modalidades_todos,
        visibles= visibles
    )

# ---------------------------------------------------------
# AJAX: cargar valores de una modalidad
# ---------------------------------------------------------
@app.post("/ajax_modalidad")
def ajax_modalidad():
    modalidad = request.json["modalidad"]

    valores = MODALIDADES[modalidad]

    visibles = MODALIDADES_VISIBLES[modalidad]  # dict {campo: label}

    return jsonify({
        "valores": valores,
        "visibles": visibles
    })
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
