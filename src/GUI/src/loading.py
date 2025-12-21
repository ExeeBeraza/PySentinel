"""
PySentinel - Componente de Pantalla de Carga
Muestra animaciones de carga durante operaciones largas
"""

import tkinter as tk
import tkinter.font as tkFont
import theme


class LoadingScreen:
    """Pantalla de carga con animación"""

    def __init__(self, root, mensaje="Cargando...", submensaje="Por favor espera"):
        self.root = root
        self.mensaje = mensaje
        self.submensaje = submensaje
        self.frame = None
        self.animation_id = None
        self.dot_count = 0
        self.spinner_index = 0
        self.spinner_chars = ["◐", "◓", "◑", "◒"]

    def mostrar(self):
        """Muestra la pantalla de carga"""
        # Crear frame overlay
        self.frame = tk.Frame(
            self.root,
            bg=theme.PRIMARY,
            width=theme.WINDOW_WIDTH,
            height=theme.WINDOW_HEIGHT
        )
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Contenedor central
        center_frame = tk.Frame(self.frame, bg=theme.PRIMARY)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Spinner animado
        self.spinner_label = tk.Label(
            center_frame,
            text=self.spinner_chars[0],
            font=tkFont.Font(size=60),
            bg=theme.PRIMARY,
            fg=theme.ACCENT
        )
        self.spinner_label.pack(pady=(0, 20))

        # Mensaje principal
        self.msg_label = tk.Label(
            center_frame,
            text=self.mensaje,
            font=tkFont.Font(family=theme.FONT_FAMILY, size=20, weight="bold"),
            bg=theme.PRIMARY,
            fg=theme.TEXT_PRIMARY
        )
        self.msg_label.pack(pady=(0, 10))

        # Submensaje con puntos animados
        self.submsg_label = tk.Label(
            center_frame,
            text=self.submensaje,
            font=tkFont.Font(family=theme.FONT_FAMILY, size=12),
            bg=theme.PRIMARY,
            fg=theme.TEXT_SECONDARY
        )
        self.submsg_label.pack()

        # Barra de progreso simple
        progress_frame = tk.Frame(center_frame, bg=theme.BORDER_COLOR, height=4, width=200)
        progress_frame.pack(pady=(30, 0))
        progress_frame.pack_propagate(False)

        self.progress_bar = tk.Frame(progress_frame, bg=theme.ACCENT, height=4, width=0)
        self.progress_bar.place(x=0, y=0, height=4)

        # Iniciar animación
        self._animar()
        self._animar_barra()

        # Forzar actualización
        self.root.update()

    def _animar(self):
        """Anima el spinner"""
        if self.frame and self.frame.winfo_exists():
            # Rotar spinner
            self.spinner_index = (self.spinner_index + 1) % len(self.spinner_chars)
            self.spinner_label.config(text=self.spinner_chars[self.spinner_index])

            # Animar puntos
            self.dot_count = (self.dot_count + 1) % 4
            dots = "." * self.dot_count
            self.submsg_label.config(text=f"{self.submensaje}{dots}")

            # Continuar animación
            self.animation_id = self.root.after(200, self._animar)

    def _animar_barra(self):
        """Anima la barra de progreso"""
        if self.frame and self.frame.winfo_exists():
            current_width = self.progress_bar.winfo_width()
            if current_width >= 200:
                self.progress_bar.place(x=0, y=0, width=0, height=4)
                current_width = 0

            new_width = current_width + 10
            self.progress_bar.place(x=0, y=0, width=new_width, height=4)

            self.root.after(100, self._animar_barra)

    def actualizar_mensaje(self, mensaje, submensaje=None):
        """Actualiza el mensaje de la pantalla de carga"""
        if self.frame and self.frame.winfo_exists():
            self.mensaje = mensaje
            self.msg_label.config(text=mensaje)
            if submensaje:
                self.submensaje = submensaje
            self.root.update()

    def ocultar(self):
        """Oculta la pantalla de carga"""
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        if self.frame:
            self.frame.destroy()
            self.frame = None


def mostrar_carga(root, mensaje="Cargando...", submensaje="Por favor espera"):
    """Función helper para mostrar pantalla de carga"""
    loading = LoadingScreen(root, mensaje, submensaje)
    loading.mostrar()
    return loading


def ejecutar_con_carga(root, funcion, mensaje="Procesando...", submensaje="Por favor espera", callback=None):
    """
    Ejecuta una función mostrando pantalla de carga.

    Args:
        root: Ventana principal de Tkinter
        funcion: Función a ejecutar
        mensaje: Mensaje a mostrar
        submensaje: Submensaje a mostrar
        callback: Función a llamar cuando termine (recibe el resultado)
    """
    loading = LoadingScreen(root, mensaje, submensaje)
    loading.mostrar()

    def ejecutar():
        try:
            resultado = funcion()
            loading.ocultar()
            if callback:
                callback(resultado)
        except Exception as e:
            loading.ocultar()
            print(f"Error: {e}")
            if callback:
                callback(None)

    # Ejecutar después de un pequeño delay para que se muestre la pantalla
    root.after(100, ejecutar)

    return loading

