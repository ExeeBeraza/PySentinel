import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, Label
from PIL import Image, ImageTk


# -------------------------------------------------------------


# --------------------------------PERFIL----------------------------------------------------------


class Perfil:
    def __init__(self, root):
        # setting title
        self.root = root

        # Limpia los widgets existentes de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Perfil")
        img = Image.open("../resource/perfil.png")
        self.photo = ImageTk.PhotoImage(img)
        # setting window size
        width = 716
        height = 444
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_856 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_856["font"] = ft
        GLabel_856["fg"] = "#333333"
        GLabel_856["justify"] = "center"
        GLabel_856["image"] = self.photo  # foto
        GLabel_856.place(x=30, y=20, width=287, height=350)

        GButton_813 = tk.Button(root)
        GButton_813["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_813["font"] = ft
        GButton_813["fg"] = "#000000"
        GButton_813["justify"] = "center"
        GButton_813["text"] = "Guardar"
        GButton_813.place(x=20, y=380, width=70, height=30)
        GButton_813["command"] = self.GButton_813_command

        GButton_266 = tk.Button(root)
        GButton_266["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_266["font"] = ft
        GButton_266["fg"] = "#000000"
        GButton_266["justify"] = "center"
        GButton_266["text"] = "Cerrar Sesión"
        GButton_266.place(x=100, y=380, width=91, height=30)
        GButton_266["command"] = self.GButton_266_command

        GLabel_496 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_496["font"] = ft
        GLabel_496["fg"] = "#333333"
        GLabel_496["justify"] = "center"
        GLabel_496["text"] = "___________________________________________________________________"
        GLabel_496.place(x=320, y=40, width=374, height=30)

        GLabel_164 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_164["font"] = ft
        GLabel_164["fg"] = "#333333"
        GLabel_164["justify"] = "center"
        GLabel_164["text"] = "___________________________________________________________________"
        GLabel_164.place(x=320, y=130, width=370, height=30)

        GLabel_289 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_289["font"] = ft
        GLabel_289["fg"] = "#333333"
        GLabel_289["justify"] = "center"
        GLabel_289["text"] = "___________________________________________________________________"
        GLabel_289.place(x=320, y=210, width=364, height=48)

        GLabel_755 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_755["font"] = ft
        GLabel_755["fg"] = "#333333"
        GLabel_755["justify"] = "center"
        GLabel_755["text"] = "___________________________________________________________________"
        GLabel_755.place(x=320, y=300, width=364, height=52)

        GLineEdit_923 = tk.Entry(root)
        GLineEdit_923["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_923["font"] = ft
        GLineEdit_923["fg"] = "#333333"
        GLineEdit_923["justify"] = "center"
        GLineEdit_923.insert(0, "Nombre de usuario")
        GLineEdit_923.place(x=320, y=20, width=120, height=30)

        GLineEdit_974 = tk.Entry(root)
        GLineEdit_974["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_974["font"] = ft
        GLineEdit_974["fg"] = "#333333"
        GLineEdit_974["justify"] = "center"
        GLineEdit_974.insert(0, "Nombre")
        GLineEdit_974.place(x=320, y=120, width=70, height=25)

        GLineEdit_565 = tk.Entry(root)
        GLineEdit_565["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_565["font"] = ft
        GLineEdit_565["fg"] = "#333333"
        GLineEdit_565["justify"] = "center"
        GLineEdit_565.insert(0, "email")
        GLineEdit_565.place(x=330, y=210, width=70, height=25)

        GLineEdit_717 = tk.Entry(root)
        GLineEdit_717["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_717["font"] = ft
        GLineEdit_717["fg"] = "#333333"
        GLineEdit_717["justify"] = "center"
        GLineEdit_717.insert(0, "contraseña")
        GLineEdit_717.place(x=330, y=300, width=70, height=25)

    def GButton_813_command(self):
        print("command")

    def GButton_266_command(self):
        print("command")



if __name__ == "__main__":
    root = tk.Tk()
    perfil = Perfil(root)
    root.mainloop()

    # ---------coments: faltaba intalar el archvio dentro del entorno no verifique, y ademas era por paquete