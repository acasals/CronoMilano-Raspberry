import threading
import queue
import pygame
import os
import time


class AudioManager:
    def __init__(self, sound_folder=None):
        # Carpeta donde están los WAV
        self.sound_folder = sound_folder or os.path.dirname(os.path.abspath(__file__))
        self.queue = queue.Queue()
        self.sounds = {}
        self.thread = threading.Thread(target=self._audio_loop, daemon=True)
         # Canal único para reproducción secuencial
        self.channel = pygame.mixer.Channel(0)
        self.volume = 0.5
        self.channel.set_volume(self.volume/100)
        
    def start(self):
        self.thread.start()
        
    def set_volume(self, v):
        self.volume = max(0.0, min(100.0, v))
        self.channel.set_volume(self.volume/100)

    def load_all(self):
        """Carga todos los .wav del directorio en memoria."""
        for filename in os.listdir(self.sound_folder):
            if filename.lower().endswith(".wav"):
                name = os.path.splitext(filename)[0]
                path = os.path.join(self.sound_folder, filename)
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    print(f"[AudioManager] Cargado: {name}")
                except Exception as e:
                    print(f"[AudioManager] ERROR cargando {filename}: {e}")

    def play(self, name):
        """El hilo crítico solo hace esto: latencia cero."""
        self.queue.put(name)

    def _audio_loop(self):
        print("[AudioManager] Hilo de audio listo")

        while True:
            name = self.queue.get()
            sound = self.sounds.get(name)

            if not sound:
                print(f"[AudioManager] Sonido '{name}' no encontrado")
                continue

            print(f"[AudioManager] Reproduciendo: {name}")
            self.channel.play(sound)

            # Esperar a que termine ANTES de pasar al siguiente
            while self.channel.get_busy():
                time.sleep(0.01)

