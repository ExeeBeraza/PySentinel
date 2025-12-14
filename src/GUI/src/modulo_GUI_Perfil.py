"""
PySentinel - Pantalla de Perfil
Gestión del perfil de usuario
"""

import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk
from PIL import Image, ImageTk
from pathlib import Path

import theme


class Perfil:
    """Pantalla de perfil de usuario"""

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.load_resources()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Mi Perfil")

    def load_resources(self):
        """Carga imágenes y recursos"""
        base_dir = Path(__file__).resolve().parent
        resource_dir = base_dir.parent / "resource"

        # Cargar imagen de perfil
        self.photo_perfil = None
        ruta_perfil = resource_dir / "perfil.png"

        if ruta_perfil.exists():
            img = Image.open(ruta_perfil)
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            self.photo_perfil = ImageTk.PhotoImage(img)

    def create_widgets(self):
        """Crea todos los widgets"""
        self.create_header()
        self.create_main_content()

    def create_header(self):
        """Crea el header con botón de volver"""
        header = tk.Frame(self.root, bg=theme.SECONDARY, height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Botón volver
        btn_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_BUTTON)
        btn_volver = tk.Button(
            header,
            text="← Volver",
            font=btn_font,
            command=self.volver,
            **theme.get_button_style()
        )
        btn_volver.pack(side="left", padx=20, pady=15, ipadx=15, ipady=8)

        # Título
        title_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=20, weight="bold")
        title = tk.Label(
            header,
            text="👤 Mi Perfil",
            font=title_font,
            bg=theme.SECONDARY,
            fg=theme.TEXT_PRIMARY
        )
        title.pack(side="left", padx=20, pady=15)

    def create_main_content(self):
        """Crea el contenido principal"""
        main_frame = tk.Frame(self.root, bg=theme.PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # Contenedor de dos columnas
        content = tk.Frame(main_frame, bg=theme.PRIMARY)
        content.pack(fill="both", expand=True)

        # Columna izquierda - Foto de perfil
        left_col = tk.Frame(content, bg=theme.PRIMARY, width=200)
        left_col.pack(side="left", fill="y", padx=(0, 40))

        # Card de foto
        photo_card = tk.Frame(left_col, bg=theme.BG_CARD, padx=30, pady=30)
        photo_card.pack(pady=20)

        if self.photo_perfil:
            photo_label = tk.Label(photo_card, image=self.photo_perfil, bg=theme.BG_CARD)
        else:
            photo_font = tkFont.Font(size=60)
            photo_label = tk.Label(
                photo_card,
                text="👤",
                font=photo_font,
                bg=theme.BG_CARD,
                fg=theme.TEXT_SECONDARY
            )
        photo_label.pack(pady=10)

        # Botón cambiar foto
        btn_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
        btn_foto = tk.Button(
            photo_card,
            text="📷 Cambiar foto",
            font=btn_font,
            **theme.get_button_style()
        )
        btn_foto.pack(pady=(15, 0), ipadx=10, ipady=5)

        # Columna derecha - Formulario
        right_col = tk.Frame(content, bg=theme.PRIMARY)
        right_col.pack(side="left", fill="both", expand=True)

        # Título de sección
        section_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=theme.FONT_SIZE_SUBTITLE)
        section_title = tk.Label(
            right_col,
            text="Información Personal",
            font=section_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_PRIMARY
        )
        section_title.pack(anchor="w", pady=(0, 20))

        # Campos del formulario
        fields = [
            ("Nombre de usuario", "usuario_ejemplo"),
            ("Nombre completo", ""),
            ("Correo electrónico", ""),
            ("Contraseña", "••••••••"),
        ]

        self.entries = {}
        label_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
        entry_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_NORMAL)

        for label_text, placeholder in fields:
            # Frame del campo
            field_frame = tk.Frame(right_col, bg=theme.PRIMARY)
            field_frame.pack(fill="x", pady=8)

            # Label
            label = tk.Label(
                field_frame,
                text=label_text,
                font=label_font,
                bg=theme.PRIMARY,
                fg=theme.TEXT_SECONDARY
            )
            label.pack(anchor="w")

            # Entry
            is_password = "Contraseña" in label_text
            entry = tk.Entry(
                field_frame,
                font=entry_font,
                show="•" if is_password else "",
                **theme.get_entry_style()
            )
            entry.pack(fill="x", pady=(5, 0), ipady=10)

            if placeholder:
                entry.insert(0, placeholder)

            self.entries[label_text] = entry

        # Botones de acción
        btn_frame = tk.Frame(right_col, bg=theme.PRIMARY)
        btn_frame.pack(fill="x", pady=(30, 0))

        btn_action_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_BUTTON, weight="bold")

        # Botón guardar
        btn_guardar = tk.Button(
            btn_frame,
            text="💾  Guardar Cambios",
            font=btn_action_font,
            command=self.guardar,
            **theme.get_accent_button_style()
        )
        btn_guardar.pack(side="left", ipadx=20, ipady=10)

        # Botón cerrar sesión
        btn_logout = tk.Button(
            btn_frame,
            text="🚪  Cerrar Sesión",
            font=btn_action_font,
            command=self.cerrar_sesion,
            **theme.get_button_style()
        )
        btn_logout.pack(side="left", padx=(15, 0), ipadx=20, ipady=10)

    # =========================================================================
    # ACCIONES
    # =========================================================================

    def volver(self):
        """Vuelve a la pantalla principal"""
        from modulo_GUI_main import Principal
        Principal(self.root)

    def guardar(self):
        """Guarda los cambios del perfil"""
        print("💾 Guardando cambios...")

    def cerrar_sesion(self):
        """Cierra la sesión del usuario"""
        from tkinter import messagebox

        # Confirmar cierre de sesión
        confirmar = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?"
        )

        if confirmar:
            print("🚪 Cerrando sesión...")
            from modulo_GUI_Inicio import Inicio
            Inicio(self.root)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = Tk()
    app = Perfil(root)
    root.mainloop()
