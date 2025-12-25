
-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS pysentinel
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE pysentinel;

-- =============================================================================
-- TABLAS
-- =============================================================================

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL UNIQUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    nombre VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(50) NOT NULL UNIQUE,
    contrasenia VARCHAR(100) NOT NULL,
    rol VARCHAR(20) DEFAULT 'usuario'
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS objeto (
    id_objeto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS analisis (
    id_analisis INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    imagen_procesada LONGBLOB NOT NULL,
    CONSTRAINT fk_analisis_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Objeto_x_analisis (
    id_objeto INT NOT NULL,
    id_analisis INT NOT NULL,
    porcentaje_fiabilidad DECIMAL(5,2) DEFAULT NULL,
    PRIMARY KEY (id_objeto, id_analisis),
    CONSTRAINT fk_oxa_objeto
        FOREIGN KEY (id_objeto) REFERENCES objeto(id_objeto)
        ON DELETE CASCADE,
    CONSTRAINT fk_oxa_analisis
        FOREIGN KEY (id_analisis) REFERENCES analisis(id_analisis)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =============================================================================
-- ÍNDICES
-- =============================================================================

CREATE INDEX idx_usuario_username ON usuario(username);
CREATE INDEX idx_usuario_correo ON usuario(correo_electronico);
CREATE INDEX idx_analisis_usuario ON analisis(id_usuario);
CREATE INDEX idx_analisis_fecha ON analisis(fecha_hora);


