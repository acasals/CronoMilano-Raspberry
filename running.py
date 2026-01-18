from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from config.modalidades import MOSTRAR_NUM_VUELOS, MODALIDADES
from helpers import resolve_id_path, hide_by_path, show_by_path, formato_mmss

class RunningScreen(Screen):

    def init_backend(self, state, crono):
        self.state = state
        self.crono = crono
        self.mostrarAcortar = {"Preparación", "Vuelo", "Espera"}
        self.mostrarAlargar = {"Preparación", "Espera"}

        # Registrar callback
        self.state.add_callback(self.on_state_update)
        
    def on_state_update(self, new_state):
        Clock.schedule_once(lambda dt: self.update_gui(new_state))

    def update_gui(self, state):
        # Actualizar cronómetro
        if "tiempo_restante" in state:
            self.ids.lbl_crono.text = formato_mmss(state["tiempo_restante"])

        # Actualizar textos opcionales
        if "fase" in state:
            fase = state["fase"]
            self.ids.lbl_fase.text = fase
            if fase in self.mostrarAcortar:
                show_by_path(self, "boton_acortar")
            else:
                hide_by_path(self, "boton_acortar")
            
            if fase in self.mostrarAlargar:
                show_by_path(self, "boton_alargar")
            else:
                hide_by_path(self, "boton_alargar")

        if "manga" in state:
            self.ids.lbl_manga.text = "Manga: " + str(state["manga"])
            
        if "grupo" in state:
            self.ids.lbl_grupo.text = "Grupo: " + str(state["grupo"])

        if "vuelo_actual" in state:
            for mod in MOSTRAR_NUM_VUELOS:
                if mod == state["modalidad"]:
                    self.ids.lbl_vuelo.text = "Vuelo: " + str(state["vuelo_actual"])
                    break

        # Cambiar de pantalla si se detiene
        if not state.get("cronoenmarcha", False):
            self.manager.current = "panelcontrol"

    def crono_stop(self):
        self.state.stop()
        
    def crono_acortar(self):
        self.state.pedir_acortar()
       
    def crono_alargar(self):
        self.state.pedir_alargar()
    


