from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

# ---------------------------------------------------------
# 1) NumericInput: tu clase base para todos los campos
# ---------------------------------------------------------
class NumericInput(TextInput):
    pass


# ---------------------------------------------------------
# 2) Teclado numérico con OK y Cancelar
# ---------------------------------------------------------
class NumericKeyboard(BoxLayout):
    def __init__(self, target, popup, **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.popup = popup
        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 5
       
        fila_altura = 60
        fila_altura_acciones = 80

        # --- Números 1-9 ---
        grid = BoxLayout(orientation='vertical', spacing=5)
        for row in (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "9")):
            r = BoxLayout(spacing=5, size_hint_y=None, height=fila_altura)
            for n in row:
                r.add_widget(Button(text=n, on_release=self.press))
            grid.add_widget(r)
        self.add_widget(grid)

        # --- Fila 0 y borrar ---
        bottom = BoxLayout(spacing=5, size_hint_y=None, height=fila_altura)
        bottom.add_widget(Button(text="0", on_release=self.press))
        bottom.add_widget(Button(text="⌫", on_release=self.backspace))
        self.add_widget(bottom)

        # --- OK y Cancelar ---
        actions =  BoxLayout(spacing=5, size_hint_y=None, height=fila_altura_acciones)
        actions.add_widget(Button(text="Cancelar",
                                  background_color=(1, 0.3, 0.3, 1),
                                  on_release=self.cancel))
        actions.add_widget(Button(text="OK",
                                  background_color=(0.3, 1, 0.3, 1),
                                  on_release=self.ok))
        self.add_widget(actions)
        
        # Ajustar altura total del teclado
        self.bind(minimum_height=self.setter('height'))
        self.size_hint_y = None

    def press(self, instance):
        self.target.text += instance.text

    def backspace(self, instance):
        self.target.text = self.target.text[:-1]

    def ok(self, instance):
        self.popup.dismiss()

    def cancel(self, instance):
        self.target.text = self.target._old_value
        self.popup.dismiss()


# ---------------------------------------------------------
# 3) KeyboardManager: un único bind global
# ---------------------------------------------------------
class KeyboardManager:
    def __init__(self, root_widget):
        self.root = root_widget
        
    def rebind(self):
        # Enlaza SOLO los NumericInput existentes
        for child in self.root.walk():
            if isinstance(child, NumericInput):
                # Evita doble bind
                child.unbind(focus=self._open_keyboard)
                child.bind(focus=self._open_keyboard)

    def _open_keyboard(self, instance, value):
        if not value:
            return
        instance._old_value = instance.text
        popup = Popup(
            title="",
            title_size=0,
            separator_height=0,
            size_hint=(1, 1),
            background_color = (0, 0, 0, 0),
            background="",
            auto_dismiss=False
        )
            # Contenedor flotante para posicionar el teclado
        root = FloatLayout()
        popup.content = root

        kb = NumericKeyboard(target=instance, popup=popup)
        # Tamaño del teclado
        kb_width = Window.width * 0.35
        kb_height = kb.height
        kb.size_hint = (None, None)
        kb.size = (kb_width, kb_height)
        # Posición del input en pantalla
        x, y = instance.to_window(instance.x, instance.y)
        # Decidir lado
        if x < Window.width / 2:
            # Input a la izquierda → teclado a la derecha
            kb_x = Window.width - kb_width - 60
        else:
            # Input a la derecha → teclado a la izquierda
            kb_x = 60
        kb_y = 60
        kb.pos = (kb_x, kb_y)

        root.add_widget(kb)
        popup.open()

