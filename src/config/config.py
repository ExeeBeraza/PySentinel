"""
PySentinel - Configuración General
Credenciales de BD y rutas del modelo
"""

import os

# =============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS (Docker)
# =============================================================================

DB_CONFIG = {
    "host": os.environ.get("PYSENTINEL_DB_HOST", "localhost"),
    "port": int(os.environ.get("PYSENTINEL_DB_PORT", 3306)),
    "user": os.environ.get("PYSENTINEL_DB_USER", "user"),
    "password": os.environ.get("PYSENTINEL_DB_PASSWORD", "123123"),
    "database": os.environ.get("PYSENTINEL_DB_NAME", "pysentinel"),
}

# Configuración alternativa con usuario root
DB_CONFIG_ROOT = {
    "host": os.environ.get("PYSENTINEL_DB_HOST", "localhost"),
    "port": int(os.environ.get("PYSENTINEL_DB_PORT", 3306)),
    "user": "root",
    "password": os.environ.get("PYSENTINEL_DB_ROOT_PASSWORD", "12341234"),
    "database": os.environ.get("PYSENTINEL_DB_NAME", "pysentinel"),
}

# =============================================================================
# CONFIGURACIÓN DEL MODELO YOLO
# =============================================================================

MODEL_PATH = os.environ.get("PYSENTINEL_MODEL_PATH", "C:\\Users\\Exequiel\\Documents\\Proyecto Exe\\WeaponEyEdetecting\\neural_network\\model\\pistolas.pt")

# =============================================================================
# CONFIGURACIÓN GENERAL
# =============================================================================

DEBUG = os.environ.get("PYSENTINEL_DEBUG", "true").lower() == "true"
CONNECTION_TIMEOUT = int(os.environ.get("PYSENTINEL_CONNECTION_TIMEOUT", 10))
MAX_RETRIES = int(os.environ.get("PYSENTINEL_MAX_RETRIES", 3))

