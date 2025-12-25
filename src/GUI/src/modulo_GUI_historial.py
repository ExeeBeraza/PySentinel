"""
PySentinel - Pantalla de Historial
Muestra el historial de detecciones realizadas
"""

import sys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, messagebox
from datetime import datetime
from pathlib import Path

# Agregar el directorio src al path para imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import theme
from db.connector import obtener_historial
from modulo_GUI_login import get_usuario_actual


class Historial:
    """Pantalla de historial de detecciones"""

    def __init__(self, root):
        self.root = root
        self.historial_data = []
        self.setup_window()
        self.cargar_historial()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Historial")

    def cargar_historial(self):
        """Carga el historial desde la BD"""
        usuario = get_usuario_actual()
        if usuario and usuario.get('id'):
            self.historial_data = obtener_historial(usuario['id'], limite=50)
        else:
            self.historial_data = []

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

        # Botón actualizar
        btn_actualizar = tk.Button(
            header,
            text="🔄 Actualizar",
            font=btn_font,
            command=self.actualizar_historial,
            **theme.get_button_style()
        )
        btn_actualizar.pack(side="right", padx=20, pady=15, ipadx=15, ipady=8)

    def create_main_content(self):
        """Crea el contenido principal"""
        main_frame = tk.Frame(self.root, bg=theme.PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Calcular estadísticas
        total_analisis = len(self.historial_data)
        total_armas = 0
        imagenes_seguras = 0
        ultimo_analisis = "N/A"

        for item in self.historial_data:
            if item.get('total_objetos', 0) > 0:
                total_armas += item.get('total_objetos', 0)
            else:
                imagenes_seguras += 1

        if self.historial_data and len(self.historial_data) > 0:
            fecha = self.historial_data[0].get('fecha_hora')
            if fecha:
                if hasattr(fecha, 'strftime'):
                    ultimo_analisis = fecha.strftime("%d/%m/%Y %H:%M")
                else:
                    ultimo_analisis = str(fecha)[:16]

        # Estadísticas rápidas
        stats_frame = tk.Frame(main_frame, bg=theme.PRIMARY)
        stats_frame.pack(fill="x", pady=(0, 20))

        stats = [
            ("📊", "Total Análisis", str(total_analisis)),
            ("🔫", "Objetos Detectados", str(total_armas)),
            ("✅", "Imágenes Seguras", str(imagenes_seguras)),
            ("📅", "Último Análisis", ultimo_analisis),
        ]

        self.stat_labels = {}
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
            self.stat_labels[label] = value_label

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

        # Mostrar historial
        if self.historial_data and len(self.historial_data) > 0:
            self.mostrar_historial()
        else:
            self.mostrar_historial_vacio()

    def mostrar_historial(self):
        """Muestra el historial de detecciones"""
        for item in self.historial_data:
            self.agregar_item_historial(item)

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

    def agregar_item_historial(self, item):
        """Agrega un item al historial"""
        item_frame = tk.Frame(
            self.scrollable_frame,
            bg=theme.BG_CARD,
            highlightbackground=theme.BORDER_COLOR,
            highlightthickness=1
        )
        item_frame.pack(fill="x", padx=10, pady=5)

        # Contenido del item
        content = tk.Frame(item_frame, bg=theme.BG_CARD, padx=15, pady=12)
        content.pack(fill="x")

        # Extraer datos
        id_analisis = item.get('id_analisis', 'N/A')
        fecha_hora = item.get('fecha_hora')
        objetos = item.get('objetos_detectados', '')
        total_objetos = item.get('total_objetos', 0)

        # Formatear fecha
        if fecha_hora:
            if hasattr(fecha_hora, 'strftime'):
                fecha_str = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
            else:
                fecha_str = str(fecha_hora)[:19]
        else:
            fecha_str = "Fecha desconocida"

        # Icono de estado
        if total_objetos > 0:
            estado_icon = "🔴"
            estado_text = f"⚠️ {total_objetos} objeto(s) detectado(s)"
            estado_color = "#e74c3c"
        else:
            estado_icon = "🟢"
            estado_text = "✅ Sin detecciones"
            estado_color = "#2ecc71"

        # Fila superior: ID y fecha
        top_row = tk.Frame(content, bg=theme.BG_CARD)
        top_row.pack(fill="x")

        info_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_NORMAL, weight="bold")
        id_label = tk.Label(
            top_row,
            text=f"{estado_icon} Análisis #{id_analisis}",
            font=info_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY,
            anchor="w"
        )
        id_label.pack(side="left")

        fecha_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
        fecha_label = tk.Label(
            top_row,
            text=f"📅 {fecha_str}",
            font=fecha_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED,
            anchor="e"
        )
        fecha_label.pack(side="right")

        # Fila inferior: Estado y objetos
        bottom_row = tk.Frame(content, bg=theme.BG_CARD)
        bottom_row.pack(fill="x", pady=(5, 0))

        estado_font = tkFont.Font(family=theme.FONT_FAMILY, size=theme.FONT_SIZE_SMALL)
        estado_label = tk.Label(
            bottom_row,
            text=estado_text,
            font=estado_font,
            bg=theme.BG_CARD,
            fg=estado_color,
            anchor="w"
        )
        estado_label.pack(side="left")

        # Mostrar objetos detectados si hay
        if objetos and total_objetos > 0:
            objetos_label = tk.Label(
                bottom_row,
                text=f"🏷️ {objetos}",
                font=fecha_font,
                bg=theme.BG_CARD,
                fg=theme.TEXT_SECONDARY,
                anchor="e"
            )
            objetos_label.pack(side="right")

    # =========================================================================
    # ACCIONES
    # =========================================================================

    def volver(self):
        """Vuelve a la pantalla principal"""
        from modulo_GUI_main import Principal
        Principal(self.root)

    def actualizar_historial(self):
        """Recarga el historial desde la BD"""
        self.cargar_historial()
        # Limpiar y recrear widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()
        print("🔄 Historial actualizado")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    root = Tk()
    app = Historial(root)
    root.mainloop()
