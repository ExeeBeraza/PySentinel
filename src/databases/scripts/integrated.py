Integración con Tkinter
3. Crear una interfaz básica
python
Copiar código
import tkinter as tk
from tkinter import messagebox

def registrar_usuario():
    # Obtener datos del formulario
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    contraseña = entry_contraseña.get()
    
    # Validar que los campos no estén vacíos
    if not nombre or not correo or not contraseña:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    # Conectar a la base de datos
    conexion = conectar_bd()
    if conexion is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return

    # Ejecutar el procedimiento almacenado
    try:
        ejecutar_procedimiento(
            conexion,
            'RegistrarUsuarioValidado',
            (nombre, correo, contraseña, 'Usuario')  # Parámetros del procedimiento
        )
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar el usuario: {e}")
    finally:
        conexion.close()

# Crear ventana Tkinter
ventana = tk.Tk()
ventana.title("Registro de Usuario")

# Etiquetas y entradas
tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

tk.Label(ventana, text="Correo:").grid(row=1, column=0, padx=10, pady=10)
entry_correo = tk.Entry(ventana)
entry_correo.grid(row=1, column=1, padx=10, pady=10)

tk.Label(ventana, text="Contraseña:").grid(row=2, column=0, padx=10, pady=10)
entry_contraseña = tk.Entry(ventana, show="*")
entry_contraseña.grid(row=2, column=1, padx=10, pady=10)

# Botón de registro
tk.Button(ventana, text="Registrar", command=registrar_usuario).grid(row=3, column=0, columnspan=2, pady=10)

# Iniciar la ventana
ventana.mainloop()
Aspectos a considerar


#Gestión de excepciones: Asegúrate de manejar todos los errores posibles en la conexión o durante la ejecución de los procedimientos.
