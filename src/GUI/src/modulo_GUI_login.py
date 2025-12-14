import os
import tkinter as tk
import tkinter.font as tkFont
from modulo_GUI_singin import Registro
from modulo_GUI_main import Principal
from PIL import Image, ImageTk  # Para manejar imágenes



#-------------------------------------------------------------

#----------------------------INCIO DE SESION-----------------------------------

class Login:
    def __init__(self, root):
        self.root = root

        # Limpia los widgets existentes de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        #setting title
        self.root.title("login")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_426=tk.Label(root)
        ft = tkFont.Font(family='Times',size=13)
        GLabel_426["font"] = ft
        GLabel_426["fg"] = "#1e9fff"
        GLabel_426["justify"] = "center"
        GLabel_426["text"] = "¿No tienes una cuenta?"
        GLabel_426.place(x=200,y=350,width=169,height=30)

        GLabel_74=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_74["font"] = ft
        GLabel_74["fg"] = "#333333"
        GLabel_74["justify"] = "center"
        GLabel_74["text"] = "___________________________________________________________________________________________________"
        GLabel_74.place(x=20,y=370,width=562,height=42)

        GButton_705=tk.Button(root)
        GButton_705["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_705["font"] = ft
        GButton_705["fg"] = "#1e9fff"
        GButton_705["justify"] = "center"
        GButton_705["text"] = "Iniciar"
        GButton_705.place(x=240,y=460,width=70,height=25)
        GButton_705["command"] = self.GButton_705_command

        GButton_614=tk.Button(root)
        GButton_614["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_614["font"] = ft
        GButton_614["fg"] = "#1e9fff"
        GButton_614["justify"] = "center"
        GButton_614["text"] = "Registrarse"
        GButton_614.place(x=460,y=360,width=70,height=25)
        GButton_614["command"] = self.GButton_614_command

        GLineEdit_497=tk.Entry(root, show = "*")
        GLineEdit_497["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_497["font"] = ft
        GLineEdit_497["fg"] = "#333333"
        GLineEdit_497["justify"] = "center"
        GLineEdit_497.insert(0, "Ingrese su contraseña")
        GLineEdit_497.place(x=80,y=210,width=411,height=30)

        GLineEdit_133=tk.Entry(root)
        GLineEdit_133["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_133["font"] = ft
        GLineEdit_133["fg"] = "#333333"
        GLineEdit_133["justify"] = "center"
        GLineEdit_133.insert(0, "Ingrese su nombre de usuario")
        GLineEdit_133.place(x=80,y=110,width=419,height=34)

        GLabel_504=tk.Label(root)
        ft = tkFont.Font(family='Times',size=48)
        GLabel_504["font"] = ft
        GLabel_504["fg"] = "#333333"
        GLabel_504["justify"] = "center"
        GLabel_504["text"] = "Inicio de Sesión"
        GLabel_504.place(x=20,y=20,width=408,height=64)

    def GButton_705_command(self):
        Principal(self.root)  # instancia propia de esta funcion comando del boton

    def GButton_614_command(self):
        Registro(self.root)    #instancia propia de esta funcion comando del boton


    def iniciar_sesion(self):
        print("Iniciar sesión presionado")

    def volver(self):
        from modulo_GUI_Inicio import Inicio  # Importación local para evitar bucles de importación
        ruta_imagen = "/home/exequiel/Documentos/WeaponEyEdetecting_/WED_/src/GUI/resource/main_image.jpg"
        Inicio(self.root, ruta_imagen)  # Redibuja la ventana de inicio



if __name__ == "__main__":
    root = tk.Tk()
    login = Login(root)
    root.mainloop()



