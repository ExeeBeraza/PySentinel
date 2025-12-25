"""
PySentinel - Pantalla de Registro
Registro de nuevos usuarios
"""

import sys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, messagebox
from pathlib import Path

# Agregar el directorio src al path para imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import theme
from db.connector import registrar_usuario


class Registro:
    """Pantalla de registro de usuarios"""

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Crear Cuenta")

    def create_widgets(self):
        """Crea todos los widgets"""
        # Contenedor principal centrado
        main_frame = tk.Frame(self.root, bg=theme.PRIMARY)
        main_frame.pack(fill="both", expand=True)

        # Card de registro centrada
        card_frame = tk.Frame(main_frame, bg=theme.BG_CARD, padx=50, pady=35)
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Header del card
        header = tk.Frame(card_frame, bg=theme.BG_CARD)
        header.pack(fill="x", pady=(0, 20))

        # Icono
        icon_font = tkFont.Font(size=45)
        icon = tk.Label(
            header,
            text="📝",
            font=icon_font,
            bg=theme.BG_CARD
        )
        icon.pack()

        # Título
        title_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=26, weight="bold")
        title = tk.Label(
            header,
            text="Crear Cuenta",
            font=title_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY
        )
        title.pack(pady=(8, 3))

        # Subtítulo
        subtitle_font = tkFont.Font(family=theme.FONT_FAMILY, size=11)
        subtitle = tk.Label(
            header,
            text="Completa los datos para registrarte",
            font=subtitle_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        subtitle.pack()

        # Formulario
        form_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        form_frame.pack(fill="x", pady=5)

        label_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)
        entry_font = tkFont.Font(family=theme.FONT_FAMILY, size=11)

        # Campos del formulario
        fields = [
            ("👤", "Nombre de usuario", False, "username"),
            ("📛", "Nombre completo", False, "nombre"),
            ("📧", "Correo electrónico", False, "email"),
            ("🔒", "Contraseña", True, "password"),
            ("🔒", "Confirmar contraseña", True, "password_confirm"),
        ]

        self.entries = {}

        for icon, label_text, is_password, field_id in fields:
            field_frame = tk.Frame(form_frame, bg=theme.BG_CARD)
            field_frame.pack(fill="x", pady=6)

            label = tk.Label(
                field_frame,
                text=f"{icon}  {label_text}",
                font=label_font,
                bg=theme.BG_CARD,
                fg=theme.TEXT_SECONDARY
            )
            label.pack(anchor="w")

            entry = tk.Entry(
                field_frame,
                font=entry_font,
                width=35,
                show="•" if is_password else "",
                **theme.get_entry_style()
            )
            entry.pack(fill="x", pady=(3, 0), ipady=10)

            self.entries[field_id] = entry

        # Botón de registro
        btn_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        btn_frame.pack(fill="x", pady=(20, 10))

        btn_font = tkFont.Font(family=theme.FONT_FAMILY, size=13, weight="bold")
        btn_registro = tk.Button(
            btn_frame,
            text="Crear Cuenta",
            font=btn_font,
            command=self.registrar,
            **theme.get_accent_button_style()
        )
        btn_registro.pack(fill="x", ipady=10)

        # Link de login
        login_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        login_frame.pack(pady=10)

        login_text = tk.Label(
            login_frame,
            text="¿Ya tienes cuenta?",
            font=label_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        login_text.pack(side="left")

        login_link = tk.Label(
            login_frame,
            text=" Inicia sesión",
            font=label_font,
            bg=theme.BG_CARD,
            fg=theme.ACCENT,
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.ir_login())

        # Botón volver
        btn_volver_frame = tk.Frame(card_frame, bg=theme.BG_CARD)
        btn_volver_frame.pack(pady=(10, 0))

        btn_volver_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)
        btn_volver = tk.Button(
            btn_volver_frame,
            text="← Volver al inicio",
            font=btn_volver_font,
            command=self.volver,
            **theme.get_button_style()
        )
        btn_volver.pack(ipadx=12, ipady=6)

    # =========================================================================
    # ACCIONES
    # =========================================================================

    def registrar(self):
        """Procesa el registro del usuario"""
        # Obtener valores
        username = self.entries["username"].get().strip()
        nombre = self.entries["nombre"].get().strip()
        email = self.entries["email"].get().strip()
        password = self.entries["password"].get()
        password_confirm = self.entries["password_confirm"].get()

        # Validaciones básicas
        if not all([username, nombre, email, password, password_confirm]):
            messagebox.showwarning(
                "Campos incompletos",
                "Por favor completa todos los campos"
            )
            return

        if password != password_confirm:
            messagebox.showerror(
                "Error",
                "Las contraseñas no coinciden"
            )
            return

        if len(password) < 6:
            messagebox.showwarning(
                "Contraseña débil",
                "La contraseña debe tener al menos 6 caracteres"
            )
            return

        # Mostrar pantalla de carga
        from loading import LoadingScreen
        loading = LoadingScreen(self.root, "Creando cuenta...", "Registrando usuario en la base de datos")
        loading.mostrar()

        def procesar_registro():
            # Registrar usuario en la BD
            resultado = registrar_usuario(
                username=username,
                nombre=nombre,
                correo=email,
                contraseña=password
            )

            loading.ocultar()

            if resultado['exito']:
                print(f"✅ Usuario registrado: {username} (ID: {resultado['id_usuario']})")
                messagebox.showinfo(
                    "Registro exitoso",
                    f"¡Bienvenido {nombre}!\nTu cuenta ha sido creada exitosamente."
                )
                # Ir a la pantalla de login para que inicie sesión
                self.ir_login()
            else:
                print(f"❌ Error en registro: {resultado['mensaje']}")
                messagebox.showerror(
                    "Error de registro",
                    resultado['mensaje']
                )

        # Ejecutar registro después de mostrar loading
        self.root.after(100, procesar_registro)

    def ir_principal(self):
        """Navega a la pantalla principal"""
        from modulo_GUI_main import Principal
        Principal(self.root)

    def ir_login(self):
        """Navega a la pantalla de login"""
        from modulo_GUI_login import Login
        Login(self.root)

    def volver(self):
        """Vuelve a la pantalla de inicio"""
        from modulo_GUI_Inicio import Inicio
        Inicio(self.root)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = Tk()
    app = Registro(root)
    root.mainloop()
