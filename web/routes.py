import time
import json
from flask import Response, request, jsonify, render_template
from os import system
from config.modalidades import MODALIDADES, MODALIDADES_VISIBLES, MODALIDADES_TODOS, CONCURSO_TODOS

def register_routes(app, state,crono):


    # ---------------------------------------------------------
    # PÁGINA PRINCIPAL: muestra parámetros actuales
    # ---------------------------------------------------------
    @app.route("/")
    def index():
        cfg = state.get_dict()
        if cfg["cronoenmarcha"]:
            return render_template("running.html")
        modalidad = cfg["modalidad"]
        visibles = MODALIDADES_VISIBLES.get(modalidad, {})
        modalidades_todos = MODALIDADES_TODOS
        concurso_todos = CONCURSO_TODOS
        
        return render_template(
            "index.html",
            modalidades=MODALIDADES,
            modalidad=modalidad,
            estado=cfg,
            modalidades_todos = modalidades_todos,
            concurso_todos = concurso_todos,
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
        nombre = MODALIDADES[modalidad]["nombre"]

        # 2. Construir diccionario completo con valores editados
        valores = {}

        # Valores de la modalidad
        valores["modalidad"] = modalidad
        valores["nombre"] = nombre
        for campo in MODALIDADES[modalidad]:
            if campo in ("nombre", "modalidad"):
                continue
            valores[campo] = int(request.form[campo])

        # 3. Añadir parámetros propios del concurso
        valores["num_grupos"] = int(request.form["num_grupos"])
        valores["num_mangas"] = int(request.form["num_mangas"])
        valores["empezar_manga"] = int(request.form["empezar_manga"])
        valores["empezar_grupo"] = int(request.form["empezar_grupo"])

        # 4. Actualizar estado
        state.update(valores)

        # 5. Arrancar concurso
        state.start()
    
        return render_template("running.html")
        

    # ---------------------------------------------------------
    # CONCURSO EN MARCHA
    # ---------------------------------------------------------
    @app.route("/running")
    def running():
        return render_template("running.html")

    # ---------------------------------------------------------
    # AJAX: devuelve el estado actual del concurso
    # ---------------------------------------------------------
    @app.route("/status")
    def status():
        return jsonify(state.get_dict())
    
    
    @app.route("/events")
    def events():
        def stream():
            while True:
                estado = state.get_dict()
                yield f"data: {json.dumps(estado)}\n\n"
                time.sleep(0.2)  # envía un evento cada 200 milisegundos

        return Response(
            stream(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

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
        system("sudo shutdown -h now")
        return "Apagando..."