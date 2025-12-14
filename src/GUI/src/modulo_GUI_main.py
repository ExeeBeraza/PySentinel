import tkinter.filedialog
from pathlib import Path
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk
from PIL import Image, ImageTk
import sys

# Agregar el directorio src al path para poder importar módulos
src_dir = Path(__file__).resolve().parent.parent.parent  # Sube de src/GUI/src a src/
sys.path.insert(0, str(src_dir))

# from modulo_GUI_singin import Registro
from modulo_GUI_Perfil import Perfil
from modulo_GUI_historial import Historial
from detectores.detect import detectar_pistola


#--------------------------PRINCIPAL--------------------------------------------
class Principal:
    def __init__(self, root):
        self.root = root

        # Limpia los widgets existentes de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("WeaponEyEdetecting")

        # --- Construcción de rutas a recursos ---
        base_dir = Path(__file__).resolve().parent   # carpeta donde está este archivo
        resource_dir = base_dir.parent / "resource"  # sube un nivel y entra a resource

        ruta_perfil = resource_dir / "perfil.png"
        ruta_historial = resource_dir / "reloj.png"

        # Cargar imágenes con verificación
        self.photo_perfil = None
        self.photo_historial = None

        if ruta_perfil.exists():
            # Redimensionar imagen para que quepa en el botón
            img_perfil = Image.open(ruta_perfil)
            img_perfil = img_perfil.resize((20, 20), Image.Resampling.LANCZOS)
            self.photo_perfil = ImageTk.PhotoImage(img_perfil)
        else:
            print("⚠️ No se encontró perfil.png")

        if ruta_historial.exists():
            # Redimensionar imagen para que quepa en el botón
            img_historial = Image.open(ruta_historial)
            img_historial = img_historial.resize((20, 20), Image.Resampling.LANCZOS)
            self.photo_historial = ImageTk.PhotoImage(img_historial)
        else:
            print("⚠️ No se encontró reloj.png")

        # Configuración de ventana
        width, height = 600, 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # Botón Perfil (esquina superior izquierda)
        if self.photo_perfil:
            GButton_560 = tk.Button(root, image=self.photo_perfil,
                                    text=" Perfil", compound="left",
                                    bg="#f0f0f0",
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#000000", justify="center",
                                    command=self.GButton_560_command)
        else:
            GButton_560 = tk.Button(root, text="👤 Perfil",
                                    bg="#f0f0f0",
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#000000", justify="center",
                                    command=self.GButton_560_command)
        GButton_560.place(x=20, y=20, width=90, height=30)

        # Botón Historial (esquina superior derecha)
        if self.photo_historial:
            GButton_759 = tk.Button(root, image=self.photo_historial,
                                    text=" Historial", compound="left",
                                    bg="#f0f0f0",
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#000000", justify="center",
                                    command=self.GButton_759_command)
        else:
            GButton_759 = tk.Button(root, text="🕐 Historial",
                                    bg="#f0f0f0",
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#000000", justify="center",
                                    command=self.GButton_759_command)
        GButton_759.place(x=490, y=20, width=100, height=30)

        # Botón Add Images
        GButton_534 = tk.Button(root, bg="#f0f0f0",
                                font=tkFont.Font(family='Times', size=10),
                                fg="#000000", justify="center",
                                text="+ ADD IMAGES",
                                command=self.buscar_imagen)
        GButton_534.place(x=10, y=60, width=580, height=424)

    def GButton_560_command(self):
        Perfil(self.root)

    def GButton_759_command(self):
        Historial(self.root)

    def buscar_imagen(self):
       image_path = tkinter.filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=(("png", "*.png"), ("jpeg", "*.jpg")),
       )
       detectar_pistola(image_path)
       print("deteccion realizada")


if __name__ == "__main__":
    root = Tk()
    principal = Principal(root)
    root.mainloop()
