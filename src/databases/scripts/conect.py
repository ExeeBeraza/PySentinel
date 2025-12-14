1. Conectar Python con MySQL
Crea un archivo Python donde configurarás la conexión a la base de datos:

python
Copiar código
import mysql.connector
from mysql.connector import Error

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  # Cambia si tu servidor no está local
            user='tu_usuario',  # Usuario de MySQL
            password='tu_contraseña',  # Contraseña del usuario
            database='SistemaDeteccionArmas'  # Nombre de la base de datos
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
