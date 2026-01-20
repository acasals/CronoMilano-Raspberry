from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from config.modalidades import MODALIDADES, MODALIDADES_VISIBLES, MODALIDADES_TODOS, CONCURSO_TODOS

class PanelControl(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = None
        self.crono = None
        self.modalidades = MODALIDADES
        self.modalidad = None
        self.cfg = {}
        self.inputs = {}
        
    def init_backend(self, state, crono):
        self.state = state
        self.crono = crono
        self.state.add_callback(self.on_state_update)

        # --- AQUÍ van los valores iniciales ---
        self.modalidades = MODALIDADES
        self.modalidad = state.modalidad

        # Spinner: cargar valores
        self.ids.spinner_modalidad.values = [v["nombre"] for v in self.modalidades.values()]
        self.ids.spinner_modalidad.text = self.modalidades[self.modalidad]["nombre"]

        # Vincular evento
        self.ids.spinner_modalidad.bind(text=self.on_modalidad_change)

        # Cargar campos iniciales
        self.cfg = self.state.get_dict()
        self.actualizar_campos()

    def on_state_update(self, new_state):
        Clock.schedule_once(lambda dt: self.update_gui(new_state))

    def update_gui(self, state):
      if state["cronoenmarcha"]:
          self.manager.current = "running"


    def on_modalidad_change(self, spinner, value):
        for clave, mod in self.modalidades.items():
            if mod["nombre"] == value:
                self.modalidad = mod["modalidad"]
                for clave, valor in mod.items():
                    self.cfg[clave] = valor
                self.actualizar_campos()
                break
        
    
    def actualizar_campos(self):
        visibles = MODALIDADES_VISIBLES[self.modalidad]
        self.cargar_campos(self.ids.campos_modalidad, visibles)
        comunes = CONCURSO_TODOS
        self.cargar_campos(self.ids.campos_comunes,comunes)
      
    def cargar_campos(self, layout, campos_dict):
        layout.clear_widgets()
        layout.add_widget(Widget(size_hint_y=1))
        self.inputs = {}
        for campo, label in campos_dict.items():
            fila = BoxLayout(size_hint_y= None, height= 40)
            fila.add_widget(Widget(size_hint_x=1))
            columnas=BoxLayout(size_hint_x=None, width=250)
            # Columna 1: Label alineado a la derecha
            lbl = Label(text=label, halign="right", valign="middle")
            # Columna 2: IntInput alineado a la izquierda
            inp = IntInput(text=str(self.cfg[campo]), size_hint_x=None, width=40)
            self.inputs[campo] = inp
            columnas.add_widget(lbl)
            columnas.add_widget(inp)
            fila.add_widget(columnas)
            fila.add_widget(Widget(size_hint_x=1))

            layout.add_widget(fila)
            layout.add_widget(Widget(size_hint_x=1))
        layout.add_widget(Widget(size_hint_y=1))

    def crono_start(self):
        for campo, widget in self.inputs.items():
            self.cfg[campo] = int(widget.text)
        self.state.update(self.cfg)
        self.state.start()
 
    def ir_a_ajustes(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'ajustes'
        
class IntInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Acepta solo dígitos
        s = ''.join(c for c in substring if c.isdigit())
        if not s:
            return

        new = self.text + s

        # Valida que el número resultante sea >= 0
        try:
            if int(new) < 0:
                return
        except:
            return

        super().insert_text(s, from_undo)
        

