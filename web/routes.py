import time
import sys
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
            "panelcontrol.html",
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
        valores = state.get_dict()

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
        cfg = state.get_dict()
        if not cfg["cronoenmarcha"]:
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
            last_sent = None
            while True:
                current = state.get_dict()
                # Solo enviar si hay cambios reales
                if current != last_sent:
                    yield f"data: {json.dumps(current)}\n\n"
                    sys.stdout.flush()
                    last_sent = current

                time.sleep(0.3)

        return Response(
            stream(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
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
    # AJUSTES
    # ---------------------------------------------------------
    @app.route("/ajustes")
    def ajustes():
        cfg = state.get_dict()
        if  cfg["cronoenmarcha"]:
            return render_template("running.html")
        
        return render_template(
                "ajustes.html",
                volumen = cfg["volumen"],
                brillo_digitos = cfg["brillo_digitos"]
                )
                
    @app.post("/set_ajustes")
    def set_ajustes():
        cfg = state.get_dict()
        data = request.json
        brillo_display = cfg["brillo_display"]
        volumen = data["volumen"]
        print("volumen:", volumen)
        brillo_digitos = data["brillo_digitos"]

        state.set_brillo_volumen_digitos(brillo_display, volumen, brillo_digitos)
        return "OK"
    
    