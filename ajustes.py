from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class AjustesScreen(Screen):

    def init_backend(self, state, crono):
        self.state = state
        self.crono = crono
        # Registrar callback
        self.state.add_callback(self.on_state_update)
        
        # Cargar campos iniciales
        self.cfg = self.state.get_dict()
        
        # Sliders: cargar valores
        self.ids.slider_brillo_display.value = self.cfg["brillo_display"]
        self.ids.slider_volumen.value = self.cfg["volumen"]
        self.ids.slider_brillo_digitos.value = self.cfg["brillo_digitos"]
        # Vincular eventos
        self.ids.slider_brillo_display.bind(value=self.on_slider_change)
        self.ids.slider_volumen.bind(value=self.on_slider_change)
        self.ids.slider_brillo_digitos.bind(value=self.on_slider_change)
                
    def on_state_update(self, new_state):
        Clock.schedule_once(lambda dt: self.update_gui(new_state))
        
    def update_gui(self, state):
        if state["cronoenmarcha"]:
            self.manager.current = "running"
          
    def on_slider_change(self, slider, value):
        brillo_display = self.cfg["brillo_display"]
        volumen = self.cfg["volumen"]
        brillo_digitos = self.cfg["brillo_digitos"]
        match slider.slider_name:
            case "slider_brillo_display":
                brillo_display = value
            case "slider_volumen":
                volumen = value
            case "slider_brillo_digitos":
                brillo_digitos = value
        self.state.set_brillo_volumen_digitos(brillo_display, volumen, brillo_digitos)
        
    def volver(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'panelcontrol'