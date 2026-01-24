from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from config.settings import Settings

class AjustesScreen(Screen):

    def init_backend(self, state, crono):
        self.state = state
        self.crono = crono
        # Registrar callback
        self.state.add_callback(self.on_state_update)
        
        # Cargar campos iniciales
        self.cfg = self.state.get_dict()
        self.brillo_display = self.cfg["brillo_display"]
        self.volumen = self.cfg["volumen"]
        self.brillo_digitos = self.cfg["brillo_digitos"]
                
        # Sliders: cargar valores
        self.ids.slider_brillo_display.value = self.brillo_display
        self.ids.slider_volumen.value = self.volumen
        self.ids.slider_brillo_digitos.value = self.brillo_digitos
        # Vincular eventos
        self.ids.slider_brillo_display.bind(value=self.on_slider_change,
    on_touch_up=self.on_slider_release)
        self.ids.slider_volumen.bind(value=self.on_slider_change,
    on_touch_up=self.on_slider_release)
        self.ids.slider_brillo_digitos.bind(value=self.on_slider_change,
    on_touch_up=self.on_slider_release)
        
    def on_state_update(self, new_state):
        Clock.schedule_once(lambda dt: self.update_gui(new_state))
        
    def update_gui(self, state):
        if state["cronoenmarcha"]:
            self.manager.current = "running"
          
    def on_slider_change(self, slider, value):
        match slider.slider_name:
            case "slider_brillo_display":
                self.brillo_display = value
            case "slider_volumen":
                self.volumen = value
            case "slider_brillo_digitos":
                self.brillo_digitos = value
       
    def on_slider_release(self, slider, touch):
    # Solo actuar si el touch pertenece al slider
        if slider.collide_point(*touch.pos):
            self.state.set_brillo_volumen_digitos(
                self.brillo_display,
                self.volumen,
                self.brillo_digitos
            )
       
    def volver(self):
        settings = Settings()
        settings.set("brillo_display", self.brillo_display)
        settings.set("volumen", self.volumen)
        settings.set("brillo_digitos", self.brillo_digitos)
        settings.save()
        self.manager.transition.direction = 'left'
        self.manager.current = 'panelcontrol'