import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, Label
from modulo_GUI_main import Principal



#------------------




#-------------------REGISTRO------------------------------------
class Registro:
    def __init__(self, root):
        #setting title
        self.root = root
        self.top = tk.Toplevel(root)

        # Limpia los widgets existentes de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("login")
        #setting window size
        width=524
        height=477
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_812=tk.Label(root)
        ft = tkFont.Font(family='Times',size=45)
        GLabel_812["font"] = ft
        GLabel_812["fg"] = "#333333"
        GLabel_812["justify"] = "center"
        GLabel_812["text"] = "Registrarse"
        GLabel_812.place(x=0,y=0,width=370,height=64)

        GLineEdit_676=tk.Entry(root)
        GLineEdit_676["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_676["font"] = ft
        GLineEdit_676["fg"] = "#333333"
        GLineEdit_676["justify"] = "left"
        GLineEdit_676.insert(0, "Ingrese su nombre de usuario")
        GLineEdit_676.place(x=30,y=85,width=470,height=30)

        GLineEdit_534=tk.Entry(root)
        GLineEdit_534["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_534["font"] = ft
        GLineEdit_534["fg"] = "#333333"
        GLineEdit_534["justify"] = "left"
        GLineEdit_534.insert(0, "Ingrese su Nombre")
        GLineEdit_534.place(x=30,y=150,width=470,height=30)

        GLineEdit_715=tk.Entry(root)
        GLineEdit_715["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_715["font"] = ft
        GLineEdit_715["fg"] = "#333333"
        GLineEdit_715["justify"] = "left"
        GLineEdit_715.insert(0, "Ingrese su email")
        GLineEdit_715.place(x=30,y=210,width=469,height=30)

        GButton_282=tk.Button(root)
        GButton_282["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_282["font"] = ft
        GButton_282["fg"] = "#1e9fff"
        GButton_282["justify"] = "center"
        GButton_282["text"] = "Registrarse"
        GButton_282.place(x=230,y=390,width=70,height=25)
        GButton_282["command"] = self.GButton_282_command

        GLineEdit_842=tk.Entry(root, show = "*")
        GLineEdit_842["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_842["font"] = ft
        GLineEdit_842["fg"] = "#333333"
        GLineEdit_842["justify"] = "left"
        GLineEdit_842.insert(0, "Ingrese su contraseña")
        GLineEdit_842.place(x=30,y=270,width=469,height=30)

        GLabel_443=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_443["font"] = ft
        GLabel_443["fg"] = "#333333"
        GLabel_443["justify"] = "center"
        GLabel_443["text"] = "___________________________________________________________________________________"
        GLabel_443.place(x=30,y=330,width=466,height=38)

    def GButton_282_command(self):
        Principal(self.root)    #instancia propia de esta funcion comando del boton
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    reg = Registro(root)
    root.mainloop()
