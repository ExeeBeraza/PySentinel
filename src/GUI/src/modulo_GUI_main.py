'''

import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, Label
from PIL import Image, ImageTk
#from modulo_GUI_singin import Registro
from modulo_GUI_Perfil import Perfil
from modulo_GUI_historial import Historial





#--------------------------PRINCIPAL--------------------------------------------
class Principal:
    def __init__(self, root):
        #setting title
        #self.top = tk.Toplevel(root)
        self.root = root

        # Limpia los widgets existentes de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("WeaponEyEdetecting")

        img_ = Image.open("/home/exequiel/Documentos/WeaponEyEdetecting_/WED_/src/GUI/resource/descargar.png")          #foto
        self.photo1 = ImageTk.PhotoImage(img_)

        im_g = Image.open("/home/exequiel/Documentos/WeaponEyEdetecting_/WED_/src/GUI/resource/descargar (1).png")          #foto
        self.photo2 = ImageTk.PhotoImage(im_g)

        #setting window size
        width=649
        height=556
        screenwidth = root.winfo_screenwidth()
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GButton_560=tk.Button(root)
        GButton_560["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_560["font"] = ft
        GButton_560["fg"] = "#000000"
        GButton_560["justify"] = "center"
        GButton_560["image"] = self.photo1                  #foto
        GButton_560.place(x=20,y=20,width=70,height=25)
        GButton_560["command"] = self.GButton_560_command

        GButton_759=tk.Button(root)
        GButton_759["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_759["font"] = ft
        GButton_759["fg"] = "#000000"
        GButton_759["justify"] = "center"
        GButton_759["image"] = self.photo2                                          #foto
        GButton_759.place(x=520,y=20,width=70,height=25)
        GButton_759["command"] = self.GButton_759_command

        GButton_534=tk.Button(root)
        GButton_534["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_534["font"] = ft
        GButton_534["fg"] = "#000000"
        GButton_534["justify"] = "center"
        GButton_534["text"] = "+ ADD IMAGES"
        GButton_534.place(x=10,y=60,width=580,height=424)
        GButton_534["command"] = self.GButton_534_command

    def GButton_560_command(self):
        Perfil(self.root)


    def GButton_759_command(self):
        Historial(self.root)

    def GButton_534_command(self):
        print("commaasdfasdnd")
        
        


if __name__ == "__main__":
    #ruta_imagen =
    #ruta_imag_en =
    root = tk.Tk()
    principal = Principal(root)
    root.mainloop()

'''

from pathlib import Path
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk
from PIL import Image, ImageTk
# from modulo_GUI_singin import Registro
from modulo_GUI_Perfil import Perfil
from modulo_GUI_historial import Historial


#--------------------------PRINCIPAL--------------------------------------------
class Principal:
    def __init__(self, root):
        self.root = root

        # Limpia los widgets existentes de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("WeaponEyEdetecting")

        # --- Construcción de rutas relativas ---
        base_dir = Path(__file__).resolve().parent   # carpeta donde está este archivo
        resource_dir = base_dir.parent / "resource"  # sube un nivel y entra a resource

        ruta_img1 = resource_dir / "descargar.png"
        ruta_img2 = resource_dir / "descargar (1).png"

        # Depuración: imprime rutas y existencia
        print("Ruta 1:", ruta_img1, "Existe?", ruta_img1.exists())
        print("Ruta 2:", ruta_img2, "Existe?", ruta_img2.exists())

        # Cargar imágenes con verificación
        self.photo1 = None
        self.photo2 = None

        if ruta_img1.exists():
            self.photo1 = ImageTk.PhotoImage(Image.open(ruta_img1))
        else:
            print("⚠️ No se encontró descargar.png")

        if ruta_img2.exists():
            self.photo2 = ImageTk.PhotoImage(Image.open(ruta_img2))
        else:
            print("⚠️ No se encontró descargar (1).png")

        # Configuración de ventana
        width, height = 600, 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # Botón Perfil
        if self.photo1:
            GButton_560 = tk.Button(root, image=self.photo1,
                                    bg="#f0f0f0",
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#000000", justify="center",
                                    command=self.GButton_560_command)
        else:
            GButton_560 = tk.Button(root, text="Perfil",
                                    bg="#f0f0f0",
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#000000", justify="center",
                                    command=self.GButton_560_command)
        GButton_560.place(x=20, y=20, width=70, height=25)

        # Botón Historial
        if self.photo2:
            GButton_759 = tk.Button(root, image=self.photo2,
                                    bg="#f0f0f0",
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#000000", justify="center",
                                    command=self.GButton_759_command)
        else:
            GButton_759 = tk.Button(root, text="Historial",
                                    bg="#f0f0f0",
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#000000", justify="center",
                                    command=self.GButton_759_command)
        GButton_759.place(x=520, y=20, width=70, height=25)

        # Botón Add Images
        GButton_534 = tk.Button(root, bg="#f0f0f0",
                                font=tkFont.Font(family='Times', size=10),
                                fg="#000000", justify="center",
                                text="+ ADD IMAGES",
                                command=self.GButton_534_command)
        GButton_534.place(x=10, y=60, width=580, height=424)

    def GButton_560_command(self):
        Perfil(self.root)

    def GButton_759_command(self):
        Historial(self.root)

    def GButton_534_command(self):
        print("commaasdfasdnd")


if __name__ == "__main__":
    root = Tk()
    principal = Principal(root)
    root.mainloop()
