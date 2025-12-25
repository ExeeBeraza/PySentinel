"""
PySentinel - Pantalla de Resultados
Muestra los resultados de la detección de armas
"""

import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk
from PIL import Image, ImageTk
from pathlib import Path
from datetime import datetime
import pytz

import cv2
import numpy as np

import theme


class Resultados:
    """Pantalla de resultados de detección"""

    def __init__(self, root, imagen_path, detecciones, imagen_resultado=None):
        """
        Args:
            root: Ventana principal de Tkinter
            imagen_path: Ruta de la imagen analizada
            detecciones: Lista de objetos detectados [(clase, confianza, bbox), ...]
            imagen_resultado: Imagen con las detecciones dibujadas (numpy array)
        """
        self.root = root
        self.imagen_path = imagen_path
        self.detecciones = detecciones or []
        self.imagen_resultado = imagen_resultado

        self.setup_window()
        self.load_resources()
        self.create_widgets()

    def setup_window(self):
        """Configura la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

        theme.configure_window(self.root, "PySentinel - Resultados del Análisis")

    def load_resources(self):
        """Carga la imagen analizada"""
        self.photo_imagen = None
        self.photo_resultado = None

        try:
            # Cargar imagen original como miniatura
            if Path(self.imagen_path).exists():
                img = Image.open(self.imagen_path)
                # Redimensionar manteniendo aspecto
                img.thumbnail((400, 300), Image.Resampling.LANCZOS)
                self.photo_imagen = ImageTk.PhotoImage(img)

            # Cargar imagen con resultados si existe
            if self.imagen_resultado is not None:

                # Convertir de BGR a RGB
                if len(self.imagen_resultado.shape) == 3:
                    img_rgb = cv2.cvtColor(self.imagen_resultado, cv2.COLOR_BGR2RGB)
                else:
                    img_rgb = self.imagen_resultado

                img_pil = Image.fromarray(img_rgb)
                img_pil.thumbnail((400, 300), Image.Resampling.LANCZOS)
                self.photo_resultado = ImageTk.PhotoImage(img_pil)

        except Exception as e:
            print(f"Error cargando imagen: {e}")

    def create_widgets(self):
        """Crea todos los widgets"""
        self.create_header()
        self.create_main_content()

    def create_header(self):
        """Crea el header"""
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
            text="📊 Resultados del Análisis",
            font=title_font,
            bg=theme.SECONDARY,
            fg=theme.TEXT_PRIMARY
        )
        title.pack(side="left", padx=20, pady=15)

        # Botón nueva imagen
        btn_nueva = tk.Button(
            header,
            text="📷 Nueva imagen",
            font=btn_font,
            command=self.nueva_imagen,
            **theme.get_accent_button_style()
        )
        btn_nueva.pack(side="right", padx=20, pady=15, ipadx=15, ipady=8)

    def create_main_content(self):
        """Crea el contenido principal"""
        main_frame = tk.Frame(self.root, bg=theme.PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Contenedor de dos columnas
        content = tk.Frame(main_frame, bg=theme.PRIMARY)
        content.pack(fill="both", expand=True)

        # =====================================================================
        # COLUMNA IZQUIERDA - Imagen
        # =====================================================================
        left_col = tk.Frame(content, bg=theme.PRIMARY)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Card de imagen
        img_card = tk.Frame(left_col, bg=theme.BG_CARD, padx=20, pady=20)
        img_card.pack(fill="both", expand=True)

        # Título de sección
        section_font = tkFont.Font(family=theme.FONT_FAMILY, size=14, weight="bold")
        img_title = tk.Label(
            img_card,
            text="🖼️ Imagen Analizada",
            font=section_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY
        )
        img_title.pack(anchor="w", pady=(0, 15))

        # Mostrar imagen (resultado si existe, sino original)
        img_frame = tk.Frame(img_card, bg=theme.BG_DARK, padx=10, pady=10)
        img_frame.pack(fill="both", expand=True)

        photo_to_show = self.photo_resultado if self.photo_resultado else self.photo_imagen

        if photo_to_show:
            img_label = tk.Label(img_frame, image=photo_to_show, bg=theme.BG_DARK)
            img_label.pack(pady=10)
        else:
            no_img_font = tkFont.Font(size=40)
            no_img = tk.Label(
                img_frame,
                text="🖼️",
                font=no_img_font,
                bg=theme.BG_DARK,
                fg=theme.TEXT_MUTED
            )
            no_img.pack(pady=30)

            no_img_text = tk.Label(
                img_frame,
                text="No se pudo cargar la imagen",
                font=tkFont.Font(family=theme.FONT_FAMILY, size=12),
                bg=theme.BG_DARK,
                fg=theme.TEXT_MUTED
            )
            no_img_text.pack()

        # Nombre del archivo
        filename = Path(self.imagen_path).name if self.imagen_path else "Desconocido"
        file_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)
        file_label = tk.Label(
            img_card,
            text=f"📁 {filename}",
            font=file_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED
        )
        file_label.pack(anchor="w", pady=(10, 0))

        # =====================================================================
        # COLUMNA DERECHA - Resultados
        # =====================================================================
        right_col = tk.Frame(content, bg=theme.PRIMARY, width=350)
        right_col.pack(side="right", fill="both", padx=(15, 0))
        right_col.pack_propagate(False)

        # Card de resumen
        summary_card = tk.Frame(right_col, bg=theme.BG_CARD, padx=20, pady=20)
        summary_card.pack(fill="x", pady=(0, 15))

        summary_title = tk.Label(
            summary_card,
            text="📋 Resumen",
            font=section_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY
        )
        summary_title.pack(anchor="w", pady=(0, 15))

        # Estadísticas
        total_objetos = len(self.detecciones)
        armas_detectadas = sum(1 for d in self.detecciones if self._es_arma(d))

        tz_utc_minus_3 = pytz.timezone('America/Argentina/Buenos_Aires')

        stats = [
            ("🔍 Objetos detectados:", str(total_objetos)),
            ("🔫 Armas encontradas:", str(armas_detectadas)),
            ("📅 Fecha análisis:", datetime.now(tz_utc_minus_3).strftime("%d/%m/%Y %H:%M")),
        ]

        stat_font = tkFont.Font(family=theme.FONT_FAMILY, size=11)
        value_font = tkFont.Font(family=theme.FONT_FAMILY, size=11, weight="bold")

        for label_text, value in stats:
            stat_frame = tk.Frame(summary_card, bg=theme.BG_CARD)
            stat_frame.pack(fill="x", pady=5)

            stat_label = tk.Label(
                stat_frame,
                text=label_text,
                font=stat_font,
                bg=theme.BG_CARD,
                fg=theme.TEXT_SECONDARY
            )
            stat_label.pack(side="left")

            stat_value = tk.Label(
                stat_frame,
                text=value,
                font=value_font,
                bg=theme.BG_CARD,
                fg=theme.ACCENT if "Armas" in label_text and int(value) > 0 else theme.TEXT_PRIMARY
            )
            stat_value.pack(side="right")

        # Estado de alerta
        if armas_detectadas > 0:
            alert_frame = tk.Frame(summary_card, bg=theme.ERROR, padx=15, pady=10)
            alert_frame.pack(fill="x", pady=(15, 0))

            alert_text = tk.Label(
                alert_frame,
                text=f"⚠️ ¡ALERTA! Se detectaron {armas_detectadas} arma(s)",
                font=tkFont.Font(family=theme.FONT_FAMILY, size=11, weight="bold"),
                bg=theme.ERROR,
                fg=theme.TEXT_PRIMARY
            )
            alert_text.pack()
        else:
            safe_frame = tk.Frame(summary_card, bg=theme.SUCCESS, padx=15, pady=10)
            safe_frame.pack(fill="x", pady=(15, 0))

            safe_text = tk.Label(
                safe_frame,
                text="✅ No se detectaron armas",
                font=tkFont.Font(family=theme.FONT_FAMILY, size=11, weight="bold"),
                bg=theme.SUCCESS,
                fg=theme.TEXT_PRIMARY
            )
            safe_text.pack()

        # Card de objetos detectados
        objects_card = tk.Frame(right_col, bg=theme.BG_CARD, padx=20, pady=20)
        objects_card.pack(fill="both", expand=True)

        objects_title = tk.Label(
            objects_card,
            text="🏷️ Objetos Detectados",
            font=section_font,
            bg=theme.BG_CARD,
            fg=theme.TEXT_PRIMARY
        )
        objects_title.pack(anchor="w", pady=(0, 15))

        # Lista de objetos con scroll
        list_frame = tk.Frame(objects_card, bg=theme.BG_DARK)
        list_frame.pack(fill="both", expand=True)

        # Canvas para scroll
        canvas = tk.Canvas(list_frame, bg=theme.BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=theme.BG_DARK)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Agregar objetos detectados a la lista
        if self.detecciones:
            for i, det in enumerate(self.detecciones):
                self._agregar_item_deteccion(scrollable_frame, i + 1, det)
        else:
            no_det_label = tk.Label(
                scrollable_frame,
                text="No se detectaron objetos",
                font=stat_font,
                bg=theme.BG_DARK,
                fg=theme.TEXT_MUTED,
                pady=20
            )
            no_det_label.pack()

    def _agregar_item_deteccion(self, parent, numero, deteccion):
        """Agrega un item de detección a la lista"""
        # Extraer información de la detección
        if isinstance(deteccion, dict):
            clase = deteccion.get('name', 'Desconocido')
            confianza = deteccion.get('confidence', 0)
        elif isinstance(deteccion, (list, tuple)) and len(deteccion) >= 2:
            clase = str(deteccion[0])
            confianza = float(deteccion[1]) if len(deteccion) > 1 else 0
        else:
            clase = str(deteccion)
            confianza = 0

        es_arma = self._es_arma({'name': clase})

        # Frame del item
        item_frame = tk.Frame(parent, bg=theme.BG_INPUT, padx=10, pady=8)
        item_frame.pack(fill="x", padx=5, pady=3)

        # Icono según tipo
        icono = "🔫" if es_arma else "📦"
        color = theme.ERROR if es_arma else theme.TEXT_PRIMARY

        # Contenido
        item_font = tkFont.Font(family=theme.FONT_FAMILY, size=11)
        conf_font = tkFont.Font(family=theme.FONT_FAMILY, size=10)

        # Número e icono
        num_label = tk.Label(
            item_frame,
            text=f"{icono} {numero}.",
            font=item_font,
            bg=theme.BG_INPUT,
            fg=color
        )
        num_label.pack(side="left")

        # Nombre de clase
        clase_label = tk.Label(
            item_frame,
            text=f" {clase.capitalize()}",
            font=tkFont.Font(family=theme.FONT_FAMILY, size=11, weight="bold"),
            bg=theme.BG_INPUT,
            fg=color
        )
        clase_label.pack(side="left")

        # Confianza
        if confianza > 0:
            conf_text = f"{confianza*100:.1f}%" if confianza <= 1 else f"{confianza:.1f}%"
            conf_label = tk.Label(
                item_frame,
                text=conf_text,
                font=conf_font,
                bg=theme.BG_INPUT,
                fg=theme.SUCCESS if confianza > 0.7 else theme.WARNING
            )
            conf_label.pack(side="right")

    def _es_arma(self, deteccion):
        """Determina si una detección es un arma"""
        armas_keywords = ['gun', 'pistol', 'rifle', 'weapon', 'firearm', 'arma', 'pistola', 'revolver']

        if isinstance(deteccion, dict):
            nombre = deteccion.get('name', '').lower()
        else:
            nombre = str(deteccion).lower()

        return any(keyword in nombre for keyword in armas_keywords)

    # =========================================================================
    # ACCIONES
    # =========================================================================

    def volver(self):
        """Vuelve a la pantalla principal"""
        from modulo_GUI_main import Principal
        Principal(self.root)

    def nueva_imagen(self):
        """Permite seleccionar una nueva imagen"""
        import tkinter.filedialog

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
            from modulo_GUI_main import Principal
            principal = Principal(self.root)
            # Simular click en seleccionar imagen con la ruta
            principal.analizar_imagen_directa(image_path)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    # Prueba con datos de ejemplo
    root = Tk()

    detecciones_ejemplo = [
        {'name': 'person', 'confidence': 0.95},
        {'name': 'gun', 'confidence': 0.87},
        {'name': 'car', 'confidence': 0.72},
    ]

    app = Resultados(root, "", detecciones_ejemplo)
    root.mainloop()

