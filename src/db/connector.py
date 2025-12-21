"""
PySentinel - Conector de Base de Datos
Funciones para interactuar con MySQL usando stored procedures
"""

import sys
import pathlib
import json
import mysql.connector
from mysql.connector import Error

# Agregar el directorio src al path para imports
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from config.application_config import DB_CONFIG, DEBUG, CONNECTION_TIMEOUT, MAX_RETRIES


class DatabaseConnector:
    """Clase para manejar la conexión y operaciones con la base de datos"""

    def __init__(self):
        self.connection = None

    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
                connection_timeout=CONNECTION_TIMEOUT
            )
            if self.connection.is_connected():
                if DEBUG:
                    print("✅ Conexión exitosa a la base de datos")
                return True
        except Error as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            return False
        return False

    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            if DEBUG:
                print("🔌 Conexión cerrada")

    def _ejecutar_procedure(self, nombre_procedure, params):
        """
        Ejecuta un stored procedure y retorna el resultado

        Args:
            nombre_procedure: Nombre del procedure a ejecutar
            params: Tupla con los parámetros

        Returns:
            dict con el resultado o None si hay error
        """
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.conectar():
                    return None

            cursor = self.connection.cursor(dictionary=True)
            cursor.callproc(nombre_procedure, params)

            # Obtener el resultado del procedure
            resultado = None
            for result in cursor.stored_results():
                resultado = result.fetchone()

            # Hacer commit para guardar los cambios (INSERT, UPDATE, DELETE)
            self.connection.commit()

            cursor.close()
            return resultado

        except Error as e:
            print(f"❌ Error ejecutando {nombre_procedure}: {e}")
            # Rollback en caso de error
            if self.connection:
                self.connection.rollback()
            return None

    # =========================================================================
    # OPERACIONES DE USUARIO
    # =========================================================================

    def registrar_usuario(self, username: str, nombre: str, correo: str, contraseña: str, rol: str = None) -> dict:
        """
        Registra un nuevo usuario en el sistema

        Args:
            username: Nombre de usuario (único)
            nombre: Nombre completo del usuario
            correo: Correo electrónico (único)
            contraseña: Contraseña del usuario
            rol: Rol del usuario (default: 'usuario')

        Returns:
            dict: {exito: bool, mensaje: str, id_usuario: int|None}
        """
        resultado = self._ejecutar_procedure(
            'sp_registrar_usuario',
            (username, nombre, correo, contraseña, rol)
        )

        if resultado:
            return {
                'exito': bool(resultado.get('exito')),
                'mensaje': resultado.get('mensaje'),
                'id_usuario': resultado.get('id_usuario')
            }

        return {
            'exito': False,
            'mensaje': 'Error de conexión con la base de datos',
            'id_usuario': None
        }

    def login_usuario(self, username: str, contraseña: str) -> dict:
        """
        Valida las credenciales del usuario

        Args:
            username: Nombre de usuario
            contraseña: Contraseña

        Returns:
            dict: {exito: bool, mensaje: str, id_usuario: int|None, nombre: str|None, rol: str|None}
        """
        resultado = self._ejecutar_procedure(
            'sp_login_usuario',
            (username, contraseña)
        )

        if resultado:
            return {
                'exito': bool(resultado.get('exito')),
                'mensaje': resultado.get('mensaje'),
                'id_usuario': resultado.get('id_usuario'),
                'nombre': resultado.get('nombre'),
                'rol': resultado.get('rol')
            }

        return {
            'exito': False,
            'mensaje': 'Error de conexión con la base de datos',
            'id_usuario': None,
            'nombre': None,
            'rol': None
        }

    # =========================================================================
    # OPERACIONES DE ANÁLISIS
    # =========================================================================

    def guardar_analisis(self, id_usuario: int, imagen_blob: bytes, fecha_hora=None) -> dict:
        """
        Guarda un análisis sin objetos detectados

        Args:
            id_usuario: ID del usuario que realiza el análisis
            imagen_blob: Imagen procesada en bytes
            fecha_hora: Fecha/hora del análisis (opcional, default: NOW())

        Returns:
            dict: {exito: bool, mensaje: str, id_analisis: int|None}
        """
        resultado = self._ejecutar_procedure(
            'sp_insertar_analisis',
            (id_usuario, fecha_hora, imagen_blob)
        )

        if resultado:
            return {
                'exito': bool(resultado.get('exito')),
                'mensaje': resultado.get('mensaje'),
                'id_analisis': resultado.get('id_analisis')
            }

        return {
            'exito': False,
            'mensaje': 'Error de conexión con la base de datos',
            'id_analisis': None
        }

    def guardar_resultado_completo(self, id_usuario: int, imagen_blob: bytes,
                                    objetos_detectados: list, fecha_hora=None) -> dict:
        """
        Guarda un análisis completo con todos los objetos detectados

        Args:
            id_usuario: ID del usuario que realiza el análisis
            imagen_blob: Imagen procesada en bytes
            objetos_detectados: Lista de objetos detectados
                               [{"nombre": "pistola", "porcentaje_fiabilidad": 95.5}, ...]
            fecha_hora: Fecha/hora del análisis (opcional)

        Returns:
            dict: {exito: bool, mensaje: str, id_analisis: int|None}
        """
        # Convertir lista a JSON string
        objetos_json = json.dumps(objetos_detectados)

        resultado = self._ejecutar_procedure(
            'sp_guardar_resultado_completo',
            (id_usuario, fecha_hora, imagen_blob, objetos_json)
        )

        if resultado:
            return {
                'exito': bool(resultado.get('exito')),
                'mensaje': resultado.get('mensaje'),
                'id_analisis': resultado.get('id_analisis')
            }

        return {
            'exito': False,
            'mensaje': 'Error de conexión con la base de datos',
            'id_analisis': None
        }

    def insertar_objeto_detectado(self, id_analisis: int, nombre_objeto: str,
                                   porcentaje_fiabilidad: float) -> dict:
        """
        Asocia un objeto detectado a un análisis existente

        Args:
            id_analisis: ID del análisis
            nombre_objeto: Nombre del objeto detectado
            porcentaje_fiabilidad: Porcentaje de confianza de la detección

        Returns:
            dict: {exito: bool, mensaje: str}
        """
        resultado = self._ejecutar_procedure(
            'sp_insertar_objeto_detectado',
            (id_analisis, nombre_objeto, porcentaje_fiabilidad)
        )

        if resultado:
            return {
                'exito': bool(resultado.get('exito')),
                'mensaje': resultado.get('mensaje')
            }

        return {
            'exito': False,
            'mensaje': 'Error de conexión con la base de datos'
        }

    def obtener_historial(self, id_usuario: int, limite: int = 50) -> list:
        """
        Obtiene el historial de análisis de un usuario

        Args:
            id_usuario: ID del usuario
            limite: Cantidad máxima de registros (default: 50)

        Returns:
            list: Lista de análisis con sus objetos detectados
        """
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.conectar():
                    return []

            cursor = self.connection.cursor(dictionary=True)
            cursor.callproc('sp_obtener_historial_usuario', (id_usuario, limite))

            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchall()

            cursor.close()
            return resultados

        except Error as e:
            print(f"❌ Error obteniendo historial: {e}")
            return []


# =============================================================================
# INSTANCIA GLOBAL (Singleton)
# =============================================================================

_db_instance = None

def get_db() -> DatabaseConnector:
    """Obtiene la instancia global del conector de BD"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnector()
    return _db_instance


# =============================================================================
# FUNCIONES DE CONVENIENCIA
# =============================================================================

def registrar_usuario(username: str, nombre: str, correo: str, contraseña: str, rol: str = None) -> dict:
    """Wrapper para registrar usuario"""
    return get_db().registrar_usuario(username, nombre, correo, contraseña, rol)

def login_usuario(username: str, contraseña: str) -> dict:
    """Wrapper para login de usuario"""
    return get_db().login_usuario(username, contraseña)

def guardar_resultado_completo(id_usuario: int, imagen_blob: bytes,
                                objetos_detectados: list, fecha_hora=None) -> dict:
    """Wrapper para guardar resultado completo"""
    return get_db().guardar_resultado_completo(id_usuario, imagen_blob, objetos_detectados, fecha_hora)

def obtener_historial(id_usuario: int, limite: int = 50) -> list:
    """Wrapper para obtener historial"""
    return get_db().obtener_historial(id_usuario, limite)


# =============================================================================
# TEST DE CONEXIÓN
# =============================================================================

if __name__ == "__main__":
    print("🔍 Probando conexión a la base de datos...")
    db = get_db()

    if db.conectar():
        print("✅ Conexión exitosa!")

        # Test de login (si hay usuarios)
        print("\n📝 Probando login con usuario de prueba...")
        resultado = db.login_usuario("test@test.com", "test123")
        print(f"Resultado: {resultado}")

        db.desconectar()
    else:
        print("❌ No se pudo conectar a la base de datos")
        print("   Verifica que MySQL esté corriendo y las credenciales sean correctas")
