from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from config.modalidades import MODALIDADES

class PanelControl(BoxLayout):
    def __init__(self, state, crono, **kwargs):
        super().__init__(**kwargs)

        self.state = state
        self.crono = crono

        # --- AQUÍ van los valores iniciales -
        ESTO ESTÁ MAL, CORREGIRLO OTRO DIA. iMPORTAR MODALIADES
        self.modalidades = state.modalidades
        self.modalidad_actual = state.modalidad

        # Spinner: cargar valores
        self.ids.spinner_modalidad.values = list(self.modalidades.keys())
        self.ids.spinner_modalidad.text = self.modalidad_actual

        # Vincular evento
        self.ids.spinner_modalidad.bind(text=self.on_modalidad_change)

        # Cargar campos iniciales
        self.actualizar_campos_modalidad()
        self.cargar_campos(self.ids.campos_comunes, state.concurso_todos)

    def on_modalidad_change(self, spinner, value):
        self.modalidad_actual = value
        self.actualizar_campos_modalidad()

    def actualizar_campos_modalidad(self):
        campos = self.modalidades[self.modalidad_actual]["campos"]
        campos_dict = {c: self.state.modalidades_todos[c] for c in campos}
        self.cargar_campos(self.ids.campos_modalidad, campos_dict)

    def cargar_campos(self, layout, campos_dict):
        layout.clear_widgets()
        for campo, label in campos_dict.items():
            fila = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
            fila.add_widget(Label(text=label, halign="right", valign="middle"))
            fila.add_widget(NumberInput(text=str(self.state.get(campo, 0))))
            layout.add_widget(fila)

class PanelControlApp(App):
    def __init__(self, state, crono, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.crono = crono

    def build(self):
        Window.size = (680, 480)
        return PanelControl(self.state, self.crono)

