DELIMITER //

CREATE PROCEDURE InsertarUsuario (
    IN p_nombre VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_contraseña VARCHAR(255),
    IN p_rol ENUM('Admin', 'Usuario')
)
BEGIN
    INSERT INTO Usuario (Nombre, Correo_electrónico, Contraseña, Rol)
    VALUES (p_nombre, p_correo, p_contraseña, p_rol);
END //
DELIMITER ;



!-- Registrar un análisis


DELIMITER //
CREATE PROCEDURE RegistrarAnalisis (
    IN p_id_usuario INT,
    IN p_imagen LONGBLOB
)
BEGIN
    INSERT INTO Analisis (ID_usuario, Imagen_procesada)
    VALUES (p_id_usuario, p_imagen);
END //
DELIMITER ;


!-- Registrar un resultado de clasificación

DELIMITER //
CREATE PROCEDURE RegistrarResultado (
    IN p_id_analisis INT,
    IN p_id_clasificacion INT
)
BEGIN
    INSERT INTO Resultado_clasificacion (ID_analisis, ID_clasificacion)
    VALUES (p_id_analisis, p_id_clasificacion);
END //
DELIMITER ;