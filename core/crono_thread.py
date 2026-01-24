import threading
import time

class CronoThread(threading.Thread):
    def __init__(self, state, audio):
        super().__init__()
        self.daemon = False
        self.state = state
        self.audio = audio
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
            vuelo_actual = 1
            
            while self.state.cronoenmarcha and not self._stop_flag:

                # --- PREPARACIÓN ---
                prep = self.prep2 if self.repetido else self.prep1
                if prep > 0 and not self._stop_flag:
                    self.state.set_fase("Preparación")
                    self.say_preparados()
                    self.countdown(prep * 60, locucion=True, lanzamiento=True,
                                   acortable=True, alargable=True)

                # --- VUELO ---
                if self.state.cronoenmarcha:
                    self.state.set_fase("Vuelo")
                    self.bocina()
                    if self.vuelo > 0 and not self._stop_flag:
                        self.countdown(self.vuelo * 60, locucion=True, lanzamiento=False,
                                    acortable=True, alargable=False)

                # --- ATERRIZAJE ---
                if self.state.cronoenmarcha:
                    self.state.set_fase("Aterrizaje")
                    self.bocina()
                    if self.aterrizaje > 0:
                        self.countdown(self.aterrizaje, locucion=False, lanzamiento=False,
                                    acortable=False, alargable=False)

                # --- ESPERA ---
                if self.state.cronoenmarcha:
                    self.state.set_fase("Espera")
                    self.final()
                    if self.espera > 0:
                        self.countdown(self.espera * 60, locucion=False, lanzamiento=False,
                                    acortable=True, alargable=True)
                    else:
                        time.sleep(3)

                # Siguiente vuelo
                if self.state.cronoenmarcha:
                    self.repetido = True
                    cuenta_vuelos -= 1
                    vuelo_actual +=1

                    if cuenta_vuelos <= 0:
                        self.grupo += 1
                        self.repetido = False

                        if self.grupo > self.num_grupos:
                            self.grupo = 1
                            self.manga += 1

                        cuenta_vuelos = self.num_vuelos
                        vuelo_actual = 1

                # Actualizar estado dinámico
                self.state.set_manga_grupo_vuelo(self.manga, self.grupo, vuelo_actual)


    # ---------------------------------------------------------
    # COUNTDOWN
    # ---------------------------------------------------------
    def countdown(self, tiempo, locucion, lanzamiento, acortable, alargable):

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
            rm = int(time_end - now)

            if acortable and ac and rm > 90:
                time_end -= 60

            if alargable and al:
                time_end += 60

            if rm < remtime:
                self.show_time(rm, locucion, lanzamiento)
                self.state.set_tiempo(rm)

            remtime = rm
            time.sleep(0.01)

    def show_time(self,tiempo,locucion,lanzamiento):
            tiempo = int(tiempo)
            minutos=tiempo//60
            segundos=tiempo % 60
            if locucion:
                self.say_tiempo(minutos, segundos, lanzamiento)
            print(minutos,segundos)
            
    # ---------------------------------------------------------
    # PARADA LIMPIA
    # ---------------------------------------------------------
    def stop_thread(self):
        self._stop_flag = True
        self.state.stop()
        
    # ---------------------------------------------------------
    # AUDIO
    # ---------------------------------------------------------
    def say_preparados(self):
        self.audio.play("preparados")
        #display7x4.scroll('preparados pilotos',300)
        if self.manga<=20:
            self.audio.play("manga")
            self.audio.play(str(self.manga))
        if self.grupo<= 20:
            self.audio.play("grupo")
            self.audio.play(str(self.grupo))
        #display7x4.scroll('round ' + str(self.manga)+ '  group ' + str(self.grupo),500)
        
    def bocina(self):
        self.audio.play("bocina")
        
    def final(self):
        self.audio.play("final")
        
    def say_tiempo(self,minutos, segundos, lanzamiento = False):
        if segundos == 0:
            if minutos == 10:
                self.audio.play("10minutos")
            if minutos == 8:
                self.audio.play("8minutos")
            if minutos == 5:
                self.audio.play("5minutos")
            if minutos == 4:
                self.audio.play("4minutos")
            if minutos == 3:
                self.audio.play("3minutos")
            if minutos == 2:
                self.audio.play("2minutos")
            if minutos == 1:
                self.audio.play("1minuto")
                
        if minutos == 0:
            if segundos==50:
                self.audio.play("50segundos")
            if segundos==40:
                self.audio.play("40segundos")
            if segundos==30:
                if lanzamiento:
                    self.audio.play("30seglanz")
                else:
                    self.audio.play("30segundos")
            if segundos==20:
                self.audio.play("20segundos")
            if segundos<=10:
                self.audio.play(str(segundos))
        
    