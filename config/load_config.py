from config.modalidades import MODALIDADES


def load_config_inicial():
    base = MODALIDADES["F5J_10"].copy()

    # Añadir parámetros propios del concurso
    base["num_grupos"] = 2
    base["num_mangas"] = 6
    base["empezar_manga"] = 1
    base["empezar_grupo"] = 1
    base["vuelo_actual"] = 1

    return base