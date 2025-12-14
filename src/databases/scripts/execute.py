2. Ejecución de procedimientos almacenados
Define una función para ejecutar un procedimiento almacenado con parámetros obtenidos desde una ventana Tkinter:

python
Copiar código
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
