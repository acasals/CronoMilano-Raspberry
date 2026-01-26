from flask import Flask
from web.routes import register_routes

app = Flask(__name__)

def run_web_server(shared_state, shared_crono):

    # Registrar rutas con dependencias
    register_routes(app, shared_state,shared_crono)
    
    # Arrancar servidor
    app.run(host="0.0.0.0", port=5000, threaded=True,debug=False, use_reloader=False)


