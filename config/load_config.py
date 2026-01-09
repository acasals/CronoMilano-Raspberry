from config.modalidades import MODALIDADES


def load_config_inicial():
    modalidad_inicial = "F5J_10"
    base = MODALIDADES[modalidad_inicial].copy()

    # Añadir parámetros propios del concurso
    base["modalidad_inicial"] = modalidad_inicial
    base["num_grupos"] = 2
    base["num_mangas"] = 6
    base["empezar_manga"] = 1
    base["empezar_grupo"] = 1

    return base