# Navega por rutas tipo 'ips.boton_x' dentro de root.ids.
def resolve_id_path(root, path):
    parts = path.split(".")
    widget = root
    for p in parts:
        widget = widget.ids[p]
    return widget

# Oculta widget
def hide_by_path(root, path):
    w = resolve_id_path(root, path)
    w.size_hint_y = None
    w.height = 0
    w.opacity = 0
    w.disabled = True

# Muestra widget
def show_by_path(root, path, height=40):
    w = resolve_id_path(root, path)
    w.size_hint_y = 1
    w.height = height
    w.opacity = 1
    w.disabled = False
    
def formato_mmss(segundos):
    m = segundos // 60
    s = segundos % 60
    return f"{m:02d}:{s:02d}"