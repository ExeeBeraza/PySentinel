"""
PySentinel - Pantalla de Historial
Muestra el historial de detecciones realizadas
"""

import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk
from datetime import datetime

import theme


class Historial:
    """Pantalla de historial de detecciones"""

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Historial")

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
            text="📋 Historial de Detecciones",
            font=title_font,
            bg=theme.SECONDARY,
            fg=theme.TEXT_PRIMARY
        )
        title.pack(side="left", padx=20, pady=15)

        # Botón limpiar historial
        btn_limpiar = tk.Button(
            header,
            text="🗑️ Limpiar",
            font=btn_font,
            command=self.limpiar_historial,
            **theme.get_button_style()
        )
        btn_limpiar.pack(side="right", padx=20, pady=15, ipadx=15, ipady=8)

    def create_main_content(self):
        """Crea el contenido principal"""
        main_frame = tk.Frame(self.root, bg=theme.PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Estadísticas rápidas
        stats_frame = tk.Frame(main_frame, bg=theme.PRIMARY)
        stats_frame.pack(fill="x", pady=(0, 20))

        stats = [
            ("📊", "Total Análisis", "0"),
            ("🔫", "Armas Detectadas", "0"),
            ("✅", "Imágenes Seguras", "0"),
            ("📅", "Último Análisis", "N/A"),
        ]

        for icon, label, value in stats:
            stat_card = tk.Frame(stats_frame, bg=theme.BG_CARD, padx=20, pady=15)
            stat_card.pack(side="left", fill="x", expand=True, padx=5)

            # Icono y valor
            value_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=24, weight="bold")
            value_label = tk.Label(
                stat_card,
                text=f"{icon} {value}",
                font=value_font,
                bg=theme.BG_CARD,
                fg=theme.TEXT_PRIMARY
            )
            value_label.pack()

            # Etiqueta
            label_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
            label_widget = tk.Label(
                stat_card,
                text=label,
                font=label_font,
                bg=theme.BG_CARD,
                fg=theme.TEXT_SECONDARY
            )
            label_widget.pack()

        # Título de la lista
        list_header = tk.Frame(main_frame, bg=theme.PRIMARY)
        list_header.pack(fill="x", pady=(10, 10))

        section_font = tkFont.Font(family=theme.FONT_FAMILY_TITLE, size=theme.FONT_SIZE_SUBTITLE)
        section_title = tk.Label(
            list_header,
            text="Detecciones Recientes",
            font=section_font,
            bg=theme.PRIMARY,
            fg=theme.TEXT_PRIMARY
        )
        section_title.pack(side="left")

        # Lista de historial con scroll
        list_container = tk.Frame(main_frame, bg=theme.BG_CARD)
        list_container.pack(fill="both", expand=True)

        # Canvas para scroll
        canvas = tk.Canvas(list_container, bg=theme.BG_CARD, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=theme.BG_CARD)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mostrar historial (datos de ejemplo)
        self.mostrar_historial_vacio()

    def mostrar_historial_vacio(self):
        """Muestra mensaje cuando no hay historial"""
        empty_frame = tk.Frame(self.scrollable_frame, bg=theme.BG_CARD)
        empty_frame.pack(fill="both", expand=True, pady=80)

        # Icono
        icon_font = tkFont.Font(size=50)
        icon = tk.Label(
            empty_frame,
            text="📭",
            font=icon_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED
        )
        icon.pack()

        # Mensaje
        msg_font = tkFont.Font(family=theme.FONT_FAMILY, size=16)
        msg = tk.Label(
            empty_frame,
            text="No hay detecciones en el historial",
            font=msg_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY
        )
        msg.pack(pady=(15, 5))

        # Submensaje
        submsg_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
        submsg = tk.Label(
            empty_frame,
            text="Las detecciones que realices aparecerán aquí",
            font=submsg_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED
        )
        submsg.pack()

        # Botón para ir a analizar
        btn_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_BUTTON, weight="bold")
        btn_analizar = tk.Button(
            empty_frame,
            text="🔍  Realizar primera detección",
            font=btn_font,
            command=self.volver,
            **theme.get_accent_button_style()
        )
        btn_analizar.pack(pady=(25, 0), ipadx=20, ipady=10)

    def agregar_item_historial(self, imagen_path, fecha, resultado, armas_detectadas):
        """Agrega un item al historial (para uso futuro)"""
        item_frame = tk.Frame(
            self.scrollable_frame,
            bg=theme.BG_CARD,
            highlightbackground=theme.BORDER_COLOR,
            highlightthickness=1
        )
        item_frame.pack(fill="x", padx=10, pady=5)

        # Contenido del item
        content = tk.Frame(item_frame, bg=theme.BG_CARD, padx=15, pady=10)
        content.pack(fill="x")

        # Icono de estado
        estado_icon = "🔴" if armas_detectadas > 0 else "🟢"
        estado_text = f"⚠️ {armas_detectadas} arma(s) detectada(s)" if armas_detectadas > 0 else "✅ Seguro"

        # Info
        info_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_NORMAL)
        fecha_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)

        # Nombre del archivo
        nombre = tk.Label(
            content,
            text=f"{estado_icon} {imagen_path}",
            font=info_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY,
            anchor="w"
        )
        nombre.pack(anchor="w")

        # Resultado y fecha
        detalle = tk.Label(
            content,
            text=f"{estado_text}  •  {fecha}",
            font=fecha_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_SECONDARY,
            anchor="w"
        )
        detalle.pack(anchor="w")

    # =========================================================================
    # ACCIONES
    # =========================================================================

    def volver(self):
        """Vuelve a la pantalla principal"""
        from modulo_GUI_main import Principal
        Principal(self.root)

    def limpiar_historial(self):
        print("🗑️ Limpiando historial...")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = Tk()
    app = Historial(root)
    root.mainloop()
