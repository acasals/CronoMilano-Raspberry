from config.modalidades import MODALIDADES
from config.settings import Settings

def load_config_inicial():
    base = MODALIDADES["F5J_10"].copy()

    # Añadir parámetros propios del concurso
    base["num_grupos"] = 2
    base["num_mangas"] = 6
    base["empezar_manga"] = 1
    base["empezar_grupo"] = 1
    base["manga"] = 1
    base["grupo"] = 1
    base["vuelo_actual"] = 1
    base["acortar"] = False
    base["alargar"] = False
        
    settings = Settings()
    base["brillo_display"] = settings.get("brillo_display")
    base["volumen"] = settings.get("volumen")
    base["brillo_digitos"] = settings.get("brillo_digitos")
    
    return base