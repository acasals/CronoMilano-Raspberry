from config.load_config import load_config_inicial
from config.configstate import ConfigState
from core.crono_thread import CronoThread
from web.server import run_web_server
from config.modalidades import MODALIDADES
from panelcontrol import PanelControlApp

import threading
import time


def main():
    config = load_config_inicial()
    state = ConfigState(config)

    # --- HILO CRÍTICO: CRONÓMETRO ---
    crono = CronoThread(state)
    crono.daemon = True
    crono.start()

    # --- HILO SECUNDARIO: SERVIDOR WEB ---
    web_thread = threading.Thread(
        target=run_web_server,
        args=(state,crono),
        daemon=True
    )
    web_thread.start()

    # --- GUI ---
    PanelControlApp(state,crono).run()

 
if __name__ == "__main__":
    main()

 