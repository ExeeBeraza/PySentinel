"""
PySentinel - Pantalla de Login
Inicio de sesión de usuarios
"""

import sys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, messagebox
from pathlib import Path

# Agregar el directorio src al path para imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import theme
from db.connector import login_usuario


# Variable global para almacenar el usuario logueado
usuario_actual = None


class Login:
    """Pantalla de inicio de sesión"""

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Iniciar Sesión")

    def create_widgets(self):
        """Crea todos los widgets"""
        # Contenedor principal centrado
        main_frame = tk.Frame(self.root, bg=theme.PRIMARY)
        main_frame.pack(fill="both", expand=True)

        # Card de login centrada
        card_frame = tk.Frame(main_frame, bg=theme.BG_CARD, padx=50, pady=40)
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Header del card
        header = tk.Frame(card_frame, bg=theme.BG_CARD)
        header.pack(fill="x", pady=(0, 30))

        # Icono
        icon_font = tkFont.Font(size=50)
        icon = tk.Label(
            header,
            text="🔐",
            font=icon_font,
            bg=theme.BG_CARD
        )
        icon.pack()

        # Título
        title_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=28, weight="bold")
        title = tk.Label(
            header,
            text="Iniciar Sesión",
            font=title_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY
        )
        title.pack(pady=(10, 5))

        # Subtítulo
        subtitle_font = tkFont.Font(family=theme.FONT_FAMILY, size=12)
        subtitle = tk.Label(
            header,
            text="Ingresa tus credenciales para continuar",
            font=subtitle_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        subtitle.pack()

        # Formulario
        form_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        form_frame.pack(fill="x", pady=10)

        label_font = tkFont.Font(family=theme.FONT_FAMILY, size=11)
        entry_font = tkFont.Font(family=theme.FONT_FAMILY, size=12)

        # Campo Usuario
        user_frame = tk.Frame(form_frame, bg=theme.BG_CARD)
        user_frame.pack(fill="x", pady=10)

        user_label = tk.Label(
            user_frame,
            text="👤  Nombre de usuario",
            font=label_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        user_label.pack(anchor="w")

        self.entry_username = tk.Entry(
            user_frame,
            font=entry_font,
            width=35,
            **theme.get_entry_style()
        )
        self.entry_username.pack(fill="x", pady=(5, 0), ipady=12)

        # Campo Contraseña
        pass_frame = tk.Frame(form_frame, bg=theme.BG_CARD)
        pass_frame.pack(fill="x", pady=10)

        pass_label = tk.Label(
            pass_frame,
            text="🔒  Contraseña",
            font=label_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        pass_label.pack(anchor="w")

        self.entry_password = tk.Entry(
            pass_frame,
            font=entry_font,
            width=35,
            show="•",
            **theme.get_entry_style()
        )
        self.entry_password.pack(fill="x", pady=(5, 0), ipady=12)

        # Bind Enter key para login
        self.entry_password.bind("<Return>", lambda e: self.iniciar_sesion())

        # Botón de login
        btn_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        btn_frame.pack(fill="x", pady=(25, 15))

        btn_font = tkFont.Font(family=theme.FONT_FAMILY, size=14, weight="bold")
        btn_login = tk.Button(
            btn_frame,
            text="Iniciar Sesión",
            font=btn_font,
            command=self.iniciar_sesion,
            **theme.get_accent_button_style()
        )
        btn_login.pack(fill="x", ipady=12)

        # Separador
        separator_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        separator_frame.pack(fill="x", pady=15)

        forgot_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)

        sep_line1 = tk.Frame(separator_frame, bg=theme.BORDER_COLOR, height=1)
        sep_line1.pack(side="left", fill="x", expand=True)

        sep_text = tk.Label(
            separator_frame,
            text="  o  ",
            font=forgot_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED
        )
        sep_text.pack(side="left")

        sep_line2 = tk.Frame(separator_frame, bg=theme.BORDER_COLOR, height=1)
        sep_line2.pack(side="left", fill="x", expand=True)

        # Link de registro
        register_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        register_frame.pack(pady=10)

        register_text = tk.Label(
            register_frame,
            text="¿No tienes cuenta?",
            font=label_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        register_text.pack(side="left")

        register_link = tk.Label(
            register_frame,
            text=" Regístrate",
            font=label_font,
            bg=theme.BG_CARD,
            fg=theme.ACCENT,
            cursor="hand2"
        )
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: self.ir_registro())

        # Botón volver
        btn_volver_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        btn_volver_frame.pack(pady=(20, 0))

        btn_volver_font = tkFont.Font(family=theme.FONT_FAMILY, size=11)
        btn_volver = tk.Button(
            btn_volver_frame,
            text="← Volver al inicio",
            font=btn_volver_font,
            command=self.volver,
            **theme.get_button_style()
        )
        btn_volver.pack(ipadx=15, ipady=8)

    # =========================================================================
    # ACCIONES
    # =========================================================================

    def iniciar_sesion(self):
        """Procesa el inicio de sesión"""
        global usuario_actual

        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Campos vacíos",
                "Por favor ingresa tu usuario y contraseña"
            )
            return

        # Mostrar pantalla de carga
        from loading import LoadingScreen
        loading = LoadingScreen(self.root, "Iniciando sesión...", "Verificando credenciales")
        loading.mostrar()

        def validar():
            global usuario_actual

            # Validar credenciales con la BD
            resultado = login_usuario(username, password)

            loading.ocultar()

            if resultado['exito']:
                # Guardar datos del usuario logueado
                usuario_actual = {
                    'id': resultado['id_usuario'],
                    'username': username,
                    'nombre': resultado['nombre'],
                    'rol': resultado['rol']
                }

                print(f"✅ Sesión iniciada: {resultado['nombre']} (ID: {resultado['id_usuario']})")
                messagebox.showinfo(
                    "Bienvenido",
                    f"¡Hola {resultado['nombre']}!\nHas iniciado sesión correctamente."
                )
                self.ir_principal()
            else:
                print(f"❌ Error de login: {resultado['mensaje']}")
                messagebox.showerror(
                    "Error de autenticación",
                    resultado['mensaje']
                )

        # Ejecutar validación después de mostrar loading
        self.root.after(100, validar)

    def ir_principal(self):
        """Navega a la pantalla principal"""
        from modulo_GUI_main import Principal
        Principal(self.root)

    def ir_registro(self):
        """Navega a la pantalla de registro"""
        from modulo_GUI_singin import Registro
        Registro(self.root)

    def volver(self):
        """Vuelve a la pantalla de inicio"""
        from modulo_GUI_Inicio import Inicio
        Inicio(self.root)


def get_usuario_actual():
    """Retorna el usuario actualmente logueado"""
    return usuario_actual


def cerrar_sesion():
    """Cierra la sesión del usuario actual"""
    global usuario_actual
    usuario_actual = None
    print("🚪 Sesión cerrada")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
