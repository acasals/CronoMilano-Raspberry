import threading
import time

class CronoThread(threading.Thread):
    def __init__(self, state):
        super().__init__()
        self.daemon = False
        self.state = state
        self._stop_flag = False

        # Lock interno solo para variables del hilo
        self._lock = threading.Lock()

        # Variables internas congeladas al hacer START
        self.prep1 = 0
        self.prep2 = 0
        self.vuelo = 0
        self.aterrizaje = 0
        self.espera = 0
        self.num_vuelos = 0
        self.num_grupos = 0

        self.repetido = False

    # ---------------------------------------------------------
    # Congelar parámetros al iniciar concurso
    # ---------------------------------------------------------
    def _load_parameters_from_state(self):
        with self.state._lock:
            self.prep1 = self.state.prep1
            self.prep2 = self.state.prep2
            self.vuelo = self.state.vuelo
            self.aterrizaje = self.state.aterrizaje
            self.espera = self.state.espera
            self.num_vuelos = self.state.num_vuelos
            self.num_grupos = self.state.num_grupos

            # Estado inicial
            self.manga = self.state.empezar_manga
            self.grupo = self.state.empezar_grupo
            self.vuelo_actual = 1

        self.repetido = False

    # ---------------------------------------------------------
    # HILO PRINCIPAL
    # ---------------------------------------------------------
    def run(self):
        while not self._stop_flag:
            time.sleep(0.01)

            if not self.state.cronoenmarcha:
                continue

            # Congelar parámetros al inicio
            self._load_parameters_from_state()

            cuenta_vuelos = self.num_vuelos

            while self.state.cronoenmarcha and not self._stop_flag:

                # --- PREPARACIÓN ---
                prep = self.prep2 if self.repetido else self.prep1
                if prep > 0:
                    self.state.set_fase("Preparación")
                    self.say_preparados()
                    self.countdown(prep * 60, audio=True, lanzamiento=True,
                                   acortable=True, alargable=True)

                # --- VUELO ---
                self.state.set_fase("Vuelo")
                self.bocina()
                if self.vuelo > 0:
                    self.countdown(self.vuelo * 60, audio=True, lanzamiento=False,
                                   acortable=True, alargable=False)

                # --- ATERRIZAJE ---
                self.state.set_fase("Aterrizaje")
                self.bocina()
                if self.aterrizaje > 0:
                    self.countdown(self.aterrizaje, audio=False, lanzamiento=False,
                                   acortable=False, alargable=False)

                # --- ESPERA ---
                self.state.set_fase("Espera")
                self.final()
                if self.espera > 0:
                    self.countdown(self.espera * 60, audio=False, lanzamiento=False,
                                   acortable=True, alargable=True)
                else:
                    time.sleep(3)

                # Siguiente vuelo
                self.repetido = True
                cuenta_vuelos -= 1

                if cuenta_vuelos <= 0:
                    self.grupo += 1
                    self.repetido = False

                    if self.grupo > self.num_grupos:
                        self.grupo = 1
                        self.manga += 1

                    cuenta_vuelos = self.num_vuelos

                # Actualizar estado dinámico
                self.state.set_manga_grupo_vuelo(self.manga, self.grupo, self.vuelo_actual)

        print("CronoThread detenido")

    # ---------------------------------------------------------
    # COUNTDOWN
    # ---------------------------------------------------------
    def countdown(self, tiempo, audio, lanzamiento, acortable, alargable):

        time_end = time.monotonic() + tiempo
        remtime = tiempo

        while remtime > 0:

            if not self.state.cronoenmarcha or self._stop_flag:
                break

            # Leer flags desde state
            with self.state._lock:
                ac = self.state.acortar
                al = self.state.alargar
                self.state.acortar = False
                self.state.alargar = False

            now = time.monotonic()
            rm = time_end - now

            if acortable and ac and rm > 90:
                time_end -= 60

            if alargable and al:
                time_end += 60

            if rm < remtime:
                self.show_time(rm, audio, lanzamiento)
                self.state.set_tiempo(rm)

            remtime = rm
            time.sleep(0.01)

    # ---------------------------------------------------------
    # PARADA LIMPIA
    # ---------------------------------------------------------
    def stop_thread(self):
        self._stop_flag = True
        self.state.stop()
        
    def say_preparados(self):
        print("Preparados")
        
    def bocina(self):
        print("Bocina")
        
    def final(self):
        print("Final")
        
    def show_time(self,tiempo,audio,lanzamiento):
        minutos=tiempo//60
        segundos=tiempo % 60
        print(minutos,segundos)