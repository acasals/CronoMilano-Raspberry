
import threading
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock

from panelcontrol import PanelControl
from running import RunningScreen
from ajustes import AjustesScreen

from config.load_config import load_config_inicial
from config.configstate import ConfigState
from core.crono_thread import CronoThread
from web.server import run_web_server
from config.modalidades import MODALIDADES

from kivy.factory import Factory
from coloroverlay import ColorOverlay
Factory.register('ColorOverlay', cls=ColorOverlay)

from hardware.brillo import BrilloController
        
class RootManager(ScreenManager):
    def init_backend(self, state, crono):
        self.state = state
        self.crono = crono

        # Registrar un único callback global
        self.state.add_callback(self.on_state_update)

    def on_state_update(self, new_state):
        # Ejecutar en el hilo principal de Kivy
        Clock.schedule_once(lambda dt: self.update_all_screens(new_state))

    def update_all_screens(self, new_state):
        
        # Llama a update_gui(new_state) en cada pantalla que exista.
        
        # Running
        if "running" in self.screen_names:
            screen = self.get_screen("running")
            if hasattr(screen, "update_gui"):
                screen.update_gui(new_state)

        # Panel de control
        if "panelcontrol" in self.screen_names:
            screen = self.get_screen("panelcontrol")
            if hasattr(screen, "update_gui"):
                screen.update_gui(new_state)

        # Ajustes
        if "ajustes" in self.screen_names:
            screen = self.get_screen("ajustes")
            if hasattr(screen, "update_gui"):
                screen.update_gui(new_state)




class MainApp(App):
    def __init__(self, state, crono, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.crono = crono

    def build(self):
        Builder.load_file("panelcontrol.kv")
        Builder.load_file("running.kv")
        Builder.load_file("ajustes.kv")
        
        root = Builder.load_file("main.kv")

        sm = root.ids.root_manager
        sm.init_backend(self.state, self.crono)

        sm.get_screen("panelcontrol").init_backend(self.state, self.crono)
        sm.get_screen("running").init_backend(self.state, self.crono)
        sm.get_screen("ajustes").init_backend(self.state, self.crono)
                 
        return root
    
    def on_start(self):
        
        # --- BRILLO DE LA PANTALLA KIVY ---
        from kivy.app import App
        def set_kivy_brightness(value):
            overlay = self.root.ids.brightness_overlay
            opacity = 1 - (value / 255.0)
            overlay.opacity = opacity

        # Asignar callback
        self.state.on_brillo_display_change = set_kivy_brightness

        # Aplicar brillo inicial
        set_kivy_brightness(self.state.brillo_display)
        
        # --- BRILLO DE LOS DÍGITOS (PWM HARDWARE) ---
        self.brillo_hw = BrilloController()
        
        def set_display_digitos_brightness(value):
            # value es 0–255
            self.brillo_hw.set_brillo(value)
           
        # Asignar callback
        self.state.on_brillo_digitos_change = set_display_digitos_brightness
        
        # Aplicar brillo inicial
        set_display_digitos_brightness(self.state.brillo_digitos)



    def on_stop(self):
        # Apagar PWM hardware
        self.brillo_hw.apagar()

    
def main():
    config = load_config_inicial()
    state = ConfigState(config)
    
    # --- AUDIO SOLO PARA EL CRONÓMETRO ---
    import os
    os.environ["SDL_AUDIODRIVER"] = "alsa"
    os.environ["AUDIODEV"] = "hw:Pro,0"
     
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()
    
    from sonidos.audio_manager import AudioManager
    audio = AudioManager()
    audio.start()
    audio.load_all()
    audio.set_volume(state.volumen)
    state.on_volume_change = lambda v: audio.set_volume(v)
    
    # --- HILO CRÍTICO: CRONÓMETRO ---
    crono = CronoThread(state, audio)
    crono.daemon = True
    crono.start()

    # # --- HILO SECUNDARIO: SERVIDOR WEB ---
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

 