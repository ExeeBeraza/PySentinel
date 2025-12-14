"""
PySentinel - Pantalla Principal
Interfaz principal para detección de armas
"""

import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog
from tkinter import Tk
from PIL import Image, ImageTk
from pathlib import Path
import sys

# Agregar el directorio src al path para poder importar módulos
src_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(src_dir))

# Importar tema y módulos
import theme
from modulo_GUI_Perfil import Perfil
from modulo_GUI_historial import Historial
from detectores.detect import detectar_pistola


class Principal:
    """Pantalla principal de la aplicación PySentinel"""

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.load_resources()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana principal"""
        # Limpiar widgets existentes
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Detector de Armas")

    def load_resources(self):
        """Carga imágenes y recursos"""
        base_dir = Path(__file__).resolve().parent
        resource_dir = base_dir.parent / "resources"

        # Cargar iconos
        self.icons = {}
        icon_files = {
            "perfil": "perfil.png",
            "historial": "reloj.png",
        }

        for name, filename in icon_files.items():
            path = resource_dir / filename
            if path.exists():
                img = Image.open(path)
                img = img.resize((24, 24), Image.Resampling.LANCZOS)
                self.icons[name] = ImageTk.PhotoImage(img)
            else:
                self.icons[name] = None

    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crea el header con navegación"""
        # Frame del header
        header = tk.Frame(self.root, bg=theme.SECONDARY, height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Logo/Título
        title_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=20, weight="bold")
        title = tk.Label(
            header,
            text="🔫 PySentinel",
            font=title_font,
            bg=theme.SECONDARY,
            fg=theme.TEXT_PRIMARY
        )
        title.pack(side="left", padx=20, pady=15)

        # Botones de navegación (derecha)
        nav_frame = tk.Frame(header, bg=theme.SECONDARY)
        nav_frame.pack(side="right", padx=20)

        # Botón Historial
        btn_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_BUTTON)

        self.btn_historial = tk.Button(
            nav_frame,
            text="  Historial" if self.icons.get("historial") else "📋 Historial",
            image=self.icons.get("historial"),
            compound="left",
            font=btn_font,
            command=self.ir_historial,
            **theme.get_button_style()
        )
        self.btn_historial.pack(side="right", padx=5, pady=15, ipadx=15, ipady=8)

        # Botón Perfil
        self.btn_perfil = tk.Button(
            nav_frame,
            text="  Perfil" if self.icons.get("perfil") else "👤 Perfil",
            image=self.icons.get("perfil"),
            compound="left",
            font=btn_font,
            command=self.ir_perfil,
            **theme.get_button_style()
        )
        self.btn_perfil.pack(side="right", padx=5, pady=15, ipadx=15, ipady=8)

    def create_main_content(self):
        """Crea el contenido principal"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=theme.PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Título de sección
        section_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=theme.FONT_SIZE_SUBTITLE)
        section_title = tk.Label(
            main_frame,
            text="Detector de Armas con IA",
            font=section_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_PRIMARY
        )
        section_title.pack(pady=(10, 5))

        # Subtítulo
        subtitle_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_NORMAL)
        subtitle = tk.Label(
            main_frame,
            text="Selecciona una imagen para analizar y detectar armas",
            font=subtitle_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_SECONDARY
        )
        subtitle.pack(pady=(0, 20))

        # Área de drop/selección de imagen
        self.drop_frame = tk.Frame(
            main_frame,
            bg=theme.BG_CARD,
            highlightbackground=theme.BORDER_COLOR,
            highlightthickness=2
        )
        self.drop_frame.pack(fill="both", expand=True, pady=10)

        # Contenido del área de drop
        drop_content = tk.Frame(self.drop_frame, bg=theme.BG_CARD)
        drop_content.place(relx=0.5, rely=0.5, anchor="center")

        # Icono grande
        icon_font = tkFont.Font(size=60)
        icon_label = tk.Label(
            drop_content,
            text="📷",
            font=icon_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        icon_label.pack(pady=(0, 15))

        # Texto principal
        drop_text_font = tkFont.Font(family=theme.FONT_FAMILY, size=16, weight="bold")
        drop_text = tk.Label(
            drop_content,
            text="Haz clic para seleccionar una imagen",
            font=drop_text_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY
        )
        drop_text.pack(pady=(0, 10))

        # Texto secundario
        drop_hint_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
        drop_hint = tk.Label(
            drop_content,
            text="Formatos soportados: PNG, JPG, JPEG",
            font=drop_hint_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED
        )
        drop_hint.pack()

        # Hacer clickeable toda el área
        for widget in [self.drop_frame, drop_content, icon_label, drop_text, drop_hint]:
            widget.bind("<Button-1>", lambda e: self.seleccionar_imagen())
            widget.configure(cursor="hand2")

        # Efecto hover
        def on_enter(e):
            self.drop_frame.configure(highlightbackground=theme.ACCENT)

        def on_leave(e):
            self.drop_frame.configure(highlightbackground=theme.BORDER_COLOR)

        self.drop_frame.bind("<Enter>", on_enter)
        self.drop_frame.bind("<Leave>", on_leave)

        # Botón de acción
        btn_frame = tk.Frame(main_frame, bg=theme.PRIMARY)
        btn_frame.pack(pady=20)

        btn_font = tkFont.Font(family=theme.FONT_FAMILY, size=14, weight="bold")
        self.btn_analizar = tk.Button(
            btn_frame,
            text="🔍  Seleccionar y Analizar Imagen",
            font=btn_font,
            command=self.seleccionar_imagen,
            **theme.get_accent_button_style()
        )
        self.btn_analizar.pack(ipadx=30, ipady=12)

    def create_footer(self):
        """Crea el footer con información"""
        footer = tk.Frame(self.root, bg=theme.SECONDARY, height=40)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        footer_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
        footer_text = tk.Label(
            footer,
            text="PySentinel v1.0 | Powered by YOLOv5",
            font=footer_font,
            bg=theme.SECONDARY,
            fg=theme.TEXT_MUTED
        )
        footer_text.pack(pady=10)

    # =========================================================================
    # ACCIONES
    # =========================================================================

    def seleccionar_imagen(self):
        """Abre el diálogo para seleccionar una imagen"""
        image_path = tkinter.filedialog.askopenfilename(
            title="Seleccionar imagen para analizar",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )

        if image_path:
            print(f"Analizando imagen: {image_path}")
            detectar_pistola(image_path)
            print("✅ Detección completada")

    def ir_perfil(self):
        """Navega a la pantalla de perfil"""
        Perfil(self.root)

    def ir_historial(self):
        """Navega a la pantalla de historial"""
        Historial(self.root)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = Tk()
    app = Principal(root)
    root.mainloop()
