import threading

class ConfigState:
    def __init__(self, config_dict):
        self._lock = threading.Lock()
        self._apply_dict(config_dict)

        # Estado dinámico del concurso
        self.cronoenmarcha = False
        self.fase = "Detenido"          # Fase inicial
        self.tiempo_restante = 0

    # ---------------------------------------------------------
    # MÉTODO INTERNO: aplica un diccionario completo
    # ---------------------------------------------------------
    def _apply_dict(self, d):
        # Parámetros de modalidad
        self.modalidad = d.get("modalidad")
        self.nombre = d.get("nombre")
        self.prep1 = d.get("prep1")
        self.prep2 = d.get("prep2")
        self.vuelo = d.get("vuelo")
        self.aterrizaje = d.get("aterrizaje")
        self.espera = d.get("espera")
        self.num_vuelos = d.get("num_vuelos")

        # Parámetros del concurso
        self.num_grupos = d.get("num_grupos")
        self.num_mangas = d.get("num_mangas")
        self.empezar_manga = d.get("empezar_manga")
        self.empezar_grupo = d.get("empezar_grupo")

        # Estado de manga/grupo/vuelo (se reinician en START)
        self.manga = d.get("manga")
        self.grupo = d.get("grupo")
        self.vuelo_actual = d.get("vuelo_actual")

        # Flags de control
        self.acortar = d.get("acortar")
        self.alargar = d.get("alargar")

    # ---------------------------------------------------------
    # MÉTODO PÚBLICO: update completo
    # ---------------------------------------------------------
    def update(self, config_dict):
        """
        Actualiza TODOS los valores del estado a partir de un diccionario.
        Se usa cuando la GUI o Flask envían un config completo.
        """
        with self._lock:
            self._apply_dict(config_dict)

    # ---------------------------------------------------------
    # CONTROL DEL CRONO
    # ---------------------------------------------------------
    def start(self):
        """
        La GUI/Flask solo ponen el sistema en marcha.
        La fase real la controla el CronoThread.
        """
        with self._lock:
            self.cronoenmarcha = True
            self.fase = "Preparación"   # Primera fase real del concurso
            self.manga = self.empezar_manga
            self.grupo = self.empezar_grupo
            self.vuelo_actual = 1

    def stop(self):
        """
        STOP siempre devuelve a 'Detenido'.
        """
        with self._lock:
            self.cronoenmarcha = False
            self.fase = "Detenido"

    # ---------------------------------------------------------
    # CONTROL DE FASES (solo para CronoThread)
    # ---------------------------------------------------------
    def set_fase(self, fase):
        """
        El CronoThread es el único que debe llamar a esto.
        Fases válidas:
        - Detenido
        - Preparación
        - Vuelo
        - Aterrizaje
        - Espera
        """
        with self._lock:
            self.fase = fase

    # ---------------------------------------------------------
    # ESTADO DINÁMICO
    # ---------------------------------------------------------
    def set_tiempo(self, t):
        with self._lock:
            self.tiempo_restante = int(t)

    def set_manga_grupo_vuelo(self, manga, grupo, vuelo):
        with self._lock:
            self.manga = manga
            self.grupo = grupo
            self.vuelo_actual = vuelo

    # ---------------------------------------------------------
    # FLAGS DE ACORTAR / ALARGAR
    # ---------------------------------------------------------
    def pedir_acortar(self):
        with self._lock:
            self.acortar = True

    def pedir_alargar(self):
        with self._lock:
            self.alargar = True

    # ---------------------------------------------------------
    # SERIALIZACIÓN
    # ---------------------------------------------------------
    def get_dict(self):
        with self._lock:
            return {
                "modalidad": self.modalidad,
                "nombre": self.nombre,
                "prep1": self.prep1,
                "prep2": self.prep2,
                "vuelo": self.vuelo,
                "aterrizaje": self.aterrizaje,
                "espera": self.espera,
                "num_vuelos": self.num_vuelos,
                "num_grupos": self.num_grupos,
                "num_mangas": self.num_mangas,
                "empezar_manga": self.empezar_manga,
                "empezar_grupo": self.empezar_grupo,
                "cronoenmarcha": self.cronoenmarcha,
                "fase": self.fase,
                "tiempo_restante": self.tiempo_restante,
                "manga": self.manga,
                "grupo": self.grupo,
                "vuelo_actual": self.vuelo_actual
            }