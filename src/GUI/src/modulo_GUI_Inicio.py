import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk
from PIL import Image, ImageTk
from modulo_GUI_login import Login


class Inicio:
    def __init__(self, root, ruta_imagen):
        self.root = root
        self.ruta_imagen = ruta_imagen

        # Título
        self.root.title("¡Bienvenidos!")

        # Cargar imagen
        img = Image.open(self.ruta_imagen)
        self.photo = ImageTk.PhotoImage(img)

        # Tamaño ventana
        width, height = 649, 556
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # Botón
        GButton_973 = tk.Button(root, text="Identificarse",
                                font=tkFont.Font(family='Times', size=10),
                                bg="#f0f0f0", fg="#000000",
                                relief="sunken", cursor="spraycan",
                                command=self.GButton_973_command)
        GButton_973.place(x=510, y=10, width=115, height=30)

        # Imagen
        GLabel_909 = tk.Label(root, image=self.photo,
                              font=tkFont.Font(family='Times', size=10),
                              fg="#333333", justify="center")
        GLabel_909.place(x=10, y=40, width=639, height=512)

    def GButton_973_command(self):
        Login(self.root)


if __name__ == "__main__":
    # Construir ruta absoluta a la imagen
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(BASE_DIR, "..", "resource", "main_image.jpg")

    root = tk.Tk()
    inicio = Inicio(root, ruta_imagen)
    root.mainloop()

"""
import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, Label
from PIL import Image, ImageTk  # Para manejar imágenes
from modulo_GUI_login import Login





#TODO: @archivo por cada ventana




# archivo de como manual de instalar bilbiotecas o readme algo sencillo una guia README o bien un doc
#--------------------------INICIO
class Inicio:
    def __init__(self, root, ruta_imagen):
        self.root = root
        self.ruta_imagen = ruta_imagen

        #setting title
        self.root.title("¡Bienvenidos!")
        img = Image.open(ruta_imagen)
        self.photo = ImageTk.PhotoImage(img)
        #setting window size
        width=649
        height=556
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GButton_973=tk.Button(root)
        GButton_973["anchor"] = "center"
        GButton_973["bg"] = "#f0f0f0"
        GButton_973["cursor"] = "spraycan"
        ft = tkFont.Font(family='Times',size=10)
        GButton_973["font"] = ft
        GButton_973["fg"] = "#000000"
        GButton_973["justify"] = "center"
        GButton_973["text"] = "Identificarse"
        GButton_973["relief"] = "sunken"
        GButton_973.place(x=510,y=10,width=115,height=30)
        GButton_973["command"] = self.GButton_973_command

        GLabel_909=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_909["font"] = ft
        GLabel_909["fg"] = "#333333"
        GLabel_909["justify"] = "center"
        GLabel_909["image"] = self.photo
        GLabel_909.place(x=10,y=40,width=639,height=512)

        try:
            etiqueta_imagen = tk.Label(Inicio, image=img_tk)
            etiqueta_imagen.image = img_tk  # Necesario para mantener la referencia a la imagen
            etiqueta_imagen.pack()
        except Exception as e:
            tk.Label(Inicio, text=f"Error al cargar la imagen: {e}").pack()

    def GButton_973_command(self):
        Login(self.root)#instancia propia de esta funcion comando del boton



if __name__ == "__main__":
    ruta_imagen = "src/GUI/resource/main_image.jpg"
    root = tk.Tk()
    inicio = Inicio(root, ruta_imagen)
    root.mainloop()



"""

