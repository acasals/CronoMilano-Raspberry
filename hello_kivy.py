from kivy.app import App
from kivy.uix.label import Label
from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '680')
Config.set('graphics', 'height', '480')

class HelloApp(App):
    def build(self):
        return Label(text="Hello Kivy!", font_size=48)

HelloApp().run()