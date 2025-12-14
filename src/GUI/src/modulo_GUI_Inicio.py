"""
PySentinel - Pantalla de Inicio (Welcome)
Primera pantalla que ve el usuario al abrir la aplicación
"""

import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk
from PIL import Image, ImageTk
from pathlib import Path

import theme


class Inicio:
    """Pantalla de bienvenida de la aplicación"""

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.load_resources()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Bienvenido")

    def load_resources(self):
        """Carga imágenes y recursos"""
        base_dir = Path(__file__).resolve().parent
        resource_dir = base_dir.parent / "resource"

        # Intentar cargar imagen de fondo
        self.bg_image = None
        bg_path = resource_dir / "_85001311-a3ad-476c-ae4c-db32a1115050.jpg"

        if bg_path.exists():
            img = Image.open(bg_path)
            # Redimensionar manteniendo aspecto
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)

    def create_widgets(self):
        """Crea todos los widgets"""
        # Contenedor principal
        main_frame = tk.Frame(self.root, bg=theme.PRIMARY)
        main_frame.pack(fill="both", expand=True)

        # Sección superior - Logo y título
        header_section = tk.Frame(main_frame, bg=theme.PRIMARY)
        header_section.pack(fill="x", pady=(40, 20))

        # Logo/Icono grande
        logo_font = tkFont.Font(size=50)
        logo = tk.Label(
            header_section,
            text="🔫",
            font=logo_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_PRIMARY
        )
        logo.pack()

        # Título principal
        title_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=36, weight="bold")
        title = tk.Label(
            header_section,
            text="PySentinel",
            font=title_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_PRIMARY
        )
        title.pack(pady=(10, 5))

        # Subtítulo
        subtitle_font = tkFont.Font(family=theme.FONT_FAMILY, size=16)
        subtitle = tk.Label(
            header_section,
            text="Sistema de Detección de Armas con IA",
            font=subtitle_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_SECONDARY
        )
        subtitle.pack()

        # Sección de características
        features_frame = tk.Frame(main_frame, bg=theme.PRIMARY)
        features_frame.pack(pady=20)

        features = [
            ("🎯", "Detección precisa", "Powered by YOLOv5"),
            ("⚡", "Análisis rápido", "Resultados en segundos"),
            ("🔒", "Seguro", "Procesamiento local"),
        ]

        for icon, title_text, desc in features:
            feature_card = tk.Frame(features_frame, bg=theme.BG_CARD, padx=25, pady=20)
            feature_card.pack(side="left", padx=10)

            # Icono
            icon_font = tkFont.Font(size=28)
            icon_label = tk.Label(
                feature_card,
                text=icon,
                font=icon_font,
                bg=theme.BG_CARD
            )
            icon_label.pack()

            # Título de característica
            feat_title_font = tkFont.Font(family=theme.FONT_FAMILY, size=12, weight="bold")
            feat_title = tk.Label(
                feature_card,
                text=title_text,
                font=feat_title_font,
                bg=theme.BG_CARD,
                fg=theme.TEXT_PRIMARY
            )
            feat_title.pack(pady=(8, 2))

            # Descripción
            feat_desc_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)
            feat_desc = tk.Label(
                feature_card,
                text=desc,
                font=feat_desc_font,
                bg=theme.BG_CARD,
                fg=theme.TEXT_MUTED
            )
            feat_desc.pack()

        # Sección de botones
        btn_section = tk.Frame(main_frame, bg=theme.PRIMARY)
        btn_section.pack(pady=30)

        btn_font = tkFont.Font(family=theme.FONT_FAMILY, size=14, weight="bold")

        # Contenedor de botones lado a lado
        btn_container = tk.Frame(btn_section, bg=theme.PRIMARY)
        btn_container.pack()

        # Botón Iniciar Sesión
        btn_login = tk.Button(
            btn_container,
            text="🔐  Iniciar Sesión",
            font=btn_font,
            command=self.ir_login,
            **theme.get_accent_button_style()
        )
        btn_login.pack(side="left", padx=10, ipadx=30, ipady=15)

        # Botón Registrarse
        btn_registro = tk.Button(
            btn_container,
            text="📝  Crear Cuenta",
            font=btn_font,
            command=self.ir_registro,
            **theme.get_button_style()
        )
        btn_registro.pack(side="left", padx=10, ipadx=30, ipady=15)

        # Texto informativo
        info_font = tkFont.Font(family=theme.FONT_FAMILY, size=11)
        info_text = tk.Label(
            btn_section,
            text="Inicia sesión o crea una cuenta para comenzar a usar PySentinel",
            font=info_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_MUTED
        )
        info_text.pack(pady=(20, 0))

        # Footer
        footer = tk.Frame(main_frame, bg=theme.PRIMARY)
        footer.pack(side="bottom", fill="x", pady=20)

        footer_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)
        footer_text = tk.Label(
            footer,
            text="© 2024 PySentinel | Detección inteligente de armas",
            font=footer_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_MUTED
        )
        footer_text.pack()

    # =========================================================================
    # ACCIONES
    # =========================================================================

    def ir_login(self):
        """Navega a la pantalla de login"""
        from modulo_GUI_login import Login
        Login(self.root)

    def ir_registro(self):
        """Navega a la pantalla de registro"""
        from modulo_GUI_singin import Registro
        Registro(self.root)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = Tk()
    app = Inicio(root)
    root.mainloop()
