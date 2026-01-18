
import threading
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from panelcontrol import PanelControl
from running import RunningScreen

from config.load_config import load_config_inicial
from config.configstate import ConfigState
from core.crono_thread import CronoThread
from web.server import run_web_server
from config.modalidades import MODALIDADES

class RootManager(ScreenManager):
    pass


class MainApp(App):
    def __init__(self, state, crono, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.crono = crono

    def build(self):
        # Cargar pantallas antes del ScreenManager
        Builder.load_file("panelcontrol.kv")
        Builder.load_file("running.kv")
        # El ScreenManager se define en main.kv
        #root = RootManager()
        root = Builder.load_file("main.kv")

        # Pasar state y crono a las pantallas
        root.get_screen("panelcontrol").init_backend(self.state, self.crono)
        root.get_screen("running").init_backend(self.state, self.crono)

        return root


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
    MainApp(state,crono).run()


if __name__ == "__main__":
    main()

 