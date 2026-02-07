from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen

from config.modalidades import MODALIDADES, MODALIDADES_VISIBLES, MODALIDADES_TODOS, CONCURSO_TODOS
from gui.numeric_keyboard import NumericInput, KeyboardManager

class PanelControl(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = None
        self.crono = None
        self.modalidades = MODALIDADES
        self.modalidad = None
        self.cfg = {}
        self.inputs = {}
        
        self.keyboard_manager = KeyboardManager(self)

    def init_backend(self, state, crono):
        self.state = state
        self.crono = crono
        
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
        self.inputs = self.cargar_campos(self.ids.campos_modalidad, visibles)
        comunes = CONCURSO_TODOS
        self.inputs.update(self.cargar_campos(self.ids.campos_comunes,comunes))
        self.keyboard_manager.rebind()


    def cargar_campos(self, layout, campos_dict):
        layout.clear_widgets()
        layout.add_widget(Widget(size_hint_y=1))
        inputs = {}
        
        for campo, label in campos_dict.items():
            fila = BoxLayout(size_hint_y= None, height= 40)
            fila.add_widget(Widget(size_hint_x=1))
            columnas=BoxLayout(size_hint_x=None, width=250)
            
            # Columna 1: Label alineado a la derecha
            lbl = Label(text=label, halign="right", valign="middle")
            
            # Columna 2: NumericInput 
            inp = NumericInput(
                text=str(self.cfg[campo]),
                size_hint_x=None,
                width=60,
                input_filter='int'
            )
            inputs[campo] = inp
            
            columnas.add_widget(lbl)
            columnas.add_widget(inp)
            
            fila.add_widget(columnas)
            fila.add_widget(Widget(size_hint_x=1))

            layout.add_widget(fila)
            layout.add_widget(Widget(size_hint_x=1))
            
        layout.add_widget(Widget(size_hint_y=1))
        return inputs

    def crono_start(self):
        cfg = self.state.get_dict()
        for campo, widget in self.inputs.items():
            cfg[campo] = int(widget.text)
            
        self.state.update(cfg)
        self.state.start()
 
    def ir_a_ajustes(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'ajustes'
        

