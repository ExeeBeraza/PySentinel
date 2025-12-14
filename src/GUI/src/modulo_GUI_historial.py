import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Tk, Label
from PIL import Image, ImageTk




#-------------------------------------------------------------




#------------------------------------HISTORIAL-------------------------------------------------
class Historial:
    def __init__(self, root):
        #setting title
        #self.top = tk.Toplevel(root)
        self.root = root

        # Limpia los widgets existentes de la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("WeaponEyEdetecting")
        #setting window size
        width=606
        height=535
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        GLabel_76=tk.Label(root)
        ft = tkFont.Font(family='Times',size=48)
        GLabel_76["font"] = ft
        GLabel_76["fg"] = "#333333"
        GLabel_76["justify"] = "center"
        GLabel_76["text"] = "Historial"
        GLabel_76.place(x=30,y=10,width=250,height=64)

        GListBox_290=tk.Listbox(root)
        GListBox_290["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_290["font"] = ft
        GListBox_290["fg"] = "#333333"
        GListBox_290["justify"] = "center"
        GListBox_290.place(x=30,y=110,width=554,height=389)

        GLabel_95=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_95["font"] = ft
        GLabel_95["fg"] = "#333333"
        GLabel_95["justify"] = "center"
        GLabel_95["text"] = "____________________________________________________________________________________________________"
        GLabel_95.place(x=30,y=70,width=549,height=30)


if __name__ == "__main__":
    root = tk.Tk()
    historial = Historial(root)
    root.mainloop()
