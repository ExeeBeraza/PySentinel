"""
PySentinel - Pantalla de Perfil
Gestión del perfil de usuario
"""

import sys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, messagebox
from PIL import Image, ImageTk
from pathlib import Path

# Agregar el directorio src al path para imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import theme
from db.connector import obtener_perfil, actualizar_perfil
from modulo_GUI_login import get_usuario_actual, cerrar_sesion


class Perfil:
    """Pantalla de perfil de usuario"""

    def __init__(self, root):
        self.root = root
        self.usuario = None
        self.setup_window()
        self.load_resources()
        self.cargar_datos_usuario()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Mi Perfil")

    def load_resources(self):
        """Carga imágenes y recursos"""
        base_dir = Path(__file__).resolve().parent
        resource_dir = base_dir.parent / "resources"

        # Cargar imagen de perfil
        self.photo_perfil = None
        ruta_perfil = resource_dir / "perfil.png"

        if ruta_perfil.exists():
            img = Image.open(ruta_perfil)
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            self.photo_perfil = ImageTk.PhotoImage(img)

    def cargar_datos_usuario(self):
        """Carga los datos del usuario desde la BD"""
        usuario_actual = get_usuario_actual()

        if usuario_actual and usuario_actual.get('id'):
            resultado = obtener_perfil(usuario_actual['id'])
            if resultado.get('exito'):
                self.usuario = resultado
            else:
                self.usuario = usuario_actual
        else:
            self.usuario = {
                'username': 'Sin sesión',
                'nombre': '',
                'correo': '',
                'rol': '',
                'fecha_registro': None,
                'total_analisis': 0
            }

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

        # Columna izquierda - Foto de perfil y estadísticas
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

        # Nombre de usuario debajo de la foto
        username_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=14, weight="bold")
        username_label = tk.Label(
            photo_card,
            text=f"@{self.usuario.get('username', '')}",
            font=username_font,
            bg=theme.BG_CARD,
            fg=theme.ACCENT
        )
        username_label.pack(pady=(10, 5))

        # Rol del usuario
        rol_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)
        rol_label = tk.Label(
            photo_card,
            text=f"🏷️ {self.usuario.get('rol', 'usuario').capitalize()}",
            font=rol_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED
        )
        rol_label.pack()

        # Card de estadísticas
        stats_card = tk.Frame(left_col, bg=theme.BG_CARD, padx=25, pady=20)
        stats_card.pack(pady=10, fill="x")

        stats_title_font = tkFont.Font(family=theme.FONT_FAMILY, size=11, weight="bold")
        stats_title = tk.Label(
            stats_card,
            text="📊 Estadísticas",
            font=stats_title_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY
        )
        stats_title.pack(anchor="w", pady=(0, 10))

        # Total de análisis
        stats_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)
        total_analisis = self.usuario.get('total_analisis', 0)
        stats_analisis = tk.Label(
            stats_card,
            text=f"🔍 Análisis realizados: {total_analisis}",
            font=stats_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        stats_analisis.pack(anchor="w", pady=2)

        # Fecha de registro
        fecha_registro = self.usuario.get('fecha_registro')
        if fecha_registro:
            fecha_str = fecha_registro.strftime("%d/%m/%Y") if hasattr(fecha_registro, 'strftime') else str(fecha_registro)[:10]
        else:
            fecha_str = "N/A"

        stats_fecha = tk.Label(
            stats_card,
            text=f"📅 Miembro desde: {fecha_str}",
            font=stats_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        stats_fecha.pack(anchor="w", pady=2)

        # Columna derecha - Información del usuario
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

        # Campos del formulario con datos del usuario
        fields = [
            ("👤 Nombre de usuario", self.usuario.get('username', '')),
            ("📛 Nombre completo", self.usuario.get('nombre', '')),
            ("📧 Correo electrónico", self.usuario.get('correo', '')),
        ]

        self.entries = {}
        label_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
        entry_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_NORMAL)

        for label_text, value in fields:
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

            # Entry (solo lectura para mostrar datos)
            entry = tk.Entry(
                field_frame,
                font=entry_font,
                **theme.get_entry_style()
            )
            entry.pack(fill="x", pady=(5, 0), ipady=10)

            if value:
                entry.insert(0, value)

            # Hacer el campo de solo lectura para username y correo
            if "usuario" in label_text.lower():
                entry.config(state="readonly")

            self.entries[label_text] = entry

        # Botones de acción
        btn_frame = tk.Frame(right_col, bg=theme.PRIMARY)
        btn_frame.pack(fill="x", pady=(30, 0))

        btn_action_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_BUTTON, weight="bold")

        # Botón guardar (deshabilitado por ahora)
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
            command=self.cerrar_sesion_action,
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
        # Obtener valores de los campos editables
        nombre = self.entries.get("📛 Nombre completo")
        correo = self.entries.get("📧 Correo electrónico")

        if not nombre or not correo:
            messagebox.showwarning(
                "Campos incompletos",
                "Por favor completa todos los campos"
            )
            return

        nuevo_nombre = nombre.get().strip()
        nuevo_correo = correo.get().strip()

        if not nuevo_nombre or not nuevo_correo:
            messagebox.showwarning(
                "Campos vacíos",
                "El nombre y correo no pueden estar vacíos"
            )
            return

        # Obtener ID del usuario actual
        usuario_actual = get_usuario_actual()
        if not usuario_actual or not usuario_actual.get('id'):
            messagebox.showerror(
                "Error",
                "No hay sesión activa"
            )
            return

        # Mostrar pantalla de carga
        from loading import LoadingScreen
        loading = LoadingScreen(self.root, "Guardando...", "Actualizando información del perfil")
        loading.mostrar()

        def procesar_guardado():
            resultado = actualizar_perfil(
                id_usuario=usuario_actual['id'],
                nombre=nuevo_nombre,
                correo=nuevo_correo
            )

            loading.ocultar()

            if resultado['exito']:
                print(f"✅ Perfil actualizado: {nuevo_nombre}")
                messagebox.showinfo(
                    "Éxito",
                    "Tu perfil ha sido actualizado correctamente"
                )
                # Recargar la pantalla para mostrar los cambios
                self.cargar_datos_usuario()
            else:
                print(f"❌ Error actualizando perfil: {resultado['mensaje']}")
                messagebox.showerror(
                    "Error",
                    resultado['mensaje']
                )

        self.root.after(100, procesar_guardado)

    def cerrar_sesion_action(self):
        """Cierra la sesión del usuario"""
        # Confirmar cierre de sesión
        confirmar = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?"
        )

        if confirmar:
            cerrar_sesion()  # Limpiar sesión
            print("🚪 Sesión cerrada")
            from modulo_GUI_Inicio import Inicio
            Inicio(self.root)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = Tk()
    app = Perfil(root)
    root.mainloop()
