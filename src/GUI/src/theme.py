"""
PySentinel - Tema y estilos de la aplicación
Define colores, fuentes y estilos consistentes para toda la GUI
"""

# =============================================================================
# PALETA DE COLORES
# =============================================================================

# Colores principales
PRIMARY = "#1a1a2e"          # Azul oscuro (fondo principal)
SECONDARY = "#16213e"        # Azul medio (fondo secundario)
ACCENT = "#e94560"           # Rojo/rosa (acento principal)
ACCENT_HOVER = "#ff6b6b"     # Rojo claro (hover)

# Colores de texto
TEXT_PRIMARY = "#ffffff"     # Blanco (texto principal)
TEXT_SECONDARY = "#a0a0a0"   # Gris claro (texto secundario)
TEXT_MUTED = "#6c6c6c"       # Gris oscuro (texto deshabilitado)

# Colores de fondo
BG_DARK = "#0f0f1a"          # Fondo muy oscuro
BG_CARD = "#1f1f3a"          # Fondo de tarjetas
BG_INPUT = "#2a2a4a"         # Fondo de inputs
BG_BUTTON = "#2d2d5a"        # Fondo de botones

# Colores de estado
SUCCESS = "#00d26a"          # Verde (éxito)
WARNING = "#ffc107"          # Amarillo (advertencia)
ERROR = "#ff4757"            # Rojo (error)
INFO = "#3498db"             # Azul (información)

# Bordes
BORDER_COLOR = "#3d3d6b"     # Color de bordes
BORDER_LIGHT = "#4a4a7a"     # Borde claro

# =============================================================================
# FUENTES
# =============================================================================

FONT_FAMILY = "Helvetica"
FONT_FAMILY_TITLE = "Helvetica"

FONT_SIZE_TITLE = 28
FONT_SIZE_SUBTITLE = 18
FONT_SIZE_NORMAL = 12
FONT_SIZE_SMALL = 10
FONT_SIZE_BUTTON = 11

# =============================================================================
# DIMENSIONES
# =============================================================================

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750

BUTTON_HEIGHT = 40
BUTTON_RADIUS = 8

PADDING_SMALL = 10
PADDING_MEDIUM = 20
PADDING_LARGE = 30

# =============================================================================
# ESTILOS DE COMPONENTES
# =============================================================================

def get_button_style():
    """Retorna el estilo base para botones"""
    return {
        "bg": BG_BUTTON,
        "fg": TEXT_PRIMARY,
        "activebackground": ACCENT,
        "activeforeground": TEXT_PRIMARY,
        "relief": "flat",
        "cursor": "hand2",
        "borderwidth": 0,
    }

def get_accent_button_style():
    """Retorna el estilo para botones de acento"""
    return {
        "bg": ACCENT,
        "fg": TEXT_PRIMARY,
        "activebackground": ACCENT_HOVER,
        "activeforeground": TEXT_PRIMARY,
        "relief": "flat",
        "cursor": "hand2",
        "borderwidth": 0,
    }

def get_entry_style():
    """Retorna el estilo base para campos de entrada"""
    return {
        "bg": BG_INPUT,
        "fg": TEXT_PRIMARY,
        "insertbackground": TEXT_PRIMARY,
        "relief": "flat",
        "borderwidth": 0,
        "highlightthickness": 1,
        "highlightbackground": BORDER_COLOR,
        "highlightcolor": ACCENT,
    }

def get_label_style():
    """Retorna el estilo base para etiquetas"""
    return {
        "bg": PRIMARY,
        "fg": TEXT_PRIMARY,
    }

def center_window(root, width, height):
    """Centra la ventana en la pantalla"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def configure_window(root, title="PySentinel", width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
    """Configura la ventana principal con estilos base"""
    root.title(title)
    root.configure(bg=PRIMARY)
    root.resizable(False, False)
    center_window(root, width, height)

