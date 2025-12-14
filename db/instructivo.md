# Procedimiento de conexion con BD MySQL
1. Conectar Python con MySQL
Crea un archivo Python donde configurarás la conexión a la base de datos:

```python
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
```

2. Ejecución de procedimientos almacenados
Define una función para ejecutar un procedimiento almacenado con parámetros obtenidos desde una ventana Tkinter:

```python
    def ejecutar_procedimiento(conexion, procedimiento, parametros):
        try:
            cursor = conexion.cursor()
            cursor.callproc(procedimiento, parametros)
            conexion.commit()
            print("Procedimiento ejecutado correctamente")
        except Error as e:
            print(f"Error al ejecutar el procedimiento: {e}")
        finally:
            cursor.close()
```