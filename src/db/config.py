"""
PySentinel - Configuración de Base de Datos
Credenciales para conectar a MySQL (Docker)
"""

# =============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS (Docker)
# =============================================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "user",
    "password": "123123",
    "database": "pysentinel",
}

# Configuración alternativa con usuario root
DB_CONFIG_ROOT = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "12341234",
    "database": "pysentinel",
}

# =============================================================================
# CONFIGURACIÓN GENERAL
# =============================================================================

DEBUG = True
CONNECTION_TIMEOUT = 10
MAX_RETRIES = 3


