import json
import os

class Settings:
    def __init__(self, path="config/settings.json"):
        self.path = path
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "version": "0.1",
                "autor": "Alex",
                "brillo_display": 50,
                "volumen": 50,
                "brillo_digitos": 50
                }  # valores por defecto

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value