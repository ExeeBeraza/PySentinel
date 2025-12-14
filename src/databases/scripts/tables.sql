
CREATE TABLE Usuario (
    ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Correo_electrónico VARCHAR(100) UNIQUE NOT NULL,
    Contraseña VARCHAR(255) NOT NULL,
    Rol ENUM('Admin', 'Usuario') DEFAULT 'Usuario',
    Fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Analisis (
    ID_analisis INT AUTO_INCREMENT PRIMARY KEY,
    ID_usuario INT NOT NULL,
    Fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Imagen_procesada LONGBLOB NOT NULL,
    FOREIGN KEY (ID_usuario) REFERENCES Usuario(ID_usuario)
);

CREATE TABLE Clasificacion_arma (
    ID_clasificacion INT AUTO_INCREMENT PRIMARY KEY,
    Tipo_arma VARCHAR(100) NOT NULL,
    Descripcion TEXT
);

CREATE TABLE Resultado_clasificacion (
    ID_resultado INT AUTO_INCREMENT PRIMARY KEY,
    ID_analisis INT NOT NULL,
    ID_clasificacion INT NOT NULL,
    FOREIGN KEY (ID_analisis) REFERENCES Analisis(ID_analisis),
    FOREIGN KEY (ID_clasificacion) REFERENCES Clasificacion_arma(ID_clasificacion)
);

CREATE TABLE Historial (
    ID_historial INT AUTO_INCREMENT PRIMARY KEY,
    ID_analisis INT NOT NULL,
    Fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_analisis) REFERENCES Analisis(ID_analisis)
);