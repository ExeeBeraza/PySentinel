CREATE PROCEDURE InsertarUsuario (
    IN p_nombre VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_contraseña VARCHAR(255),
    IN p_rol ENUM('Admin', 'Usuario')
)
BEGIN
    INSERT INTO Usuario (Nombre, Correo_electrónico, Contraseña, Rol)
    VALUES (p_nombre, p_correo, p_contraseña, p_rol);
END;


!-- Registrar un análisis
CREATE PROCEDURE RegistrarAnalisis (
    IN p_id_usuario INT,
    IN p_imagen LONGBLOB
)
BEGIN
    INSERT INTO Analisis (ID_usuario, Imagen_procesada)
    VALUES (p_id_usuario, p_imagen);
END


-- Registrar un resultado de clasificación
CREATE PROCEDURE RegistrarResultado (
    IN p_id_analisis INT,
    IN p_id_clasificacion INT
)
BEGIN
    INSERT INTO Resultado_clasificacion (ID_analisis, ID_clasificacion)
    VALUES (p_id_analisis, p_id_clasificacion);
END;

-- Procedimiento para registrar un usuario con validación previa  Usa el procedimiento de validación antes de registrar el usuario.
CREATE PROCEDURE RegistrarUsuarioValidado (
    IN p_nombre VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_contraseña VARCHAR(255),
    IN p_rol ENUM('Admin', 'Usuario')
)
BEGIN
    -- Registrar al usuario
    INSERT INTO Usuario (Nombre, Correo_electrónico, Contraseña, Rol)
    VALUES (p_nombre, p_correo, p_contraseña, p_rol);
END


-- Procedimiento para registrar un análisis y su resultado Registra un análisis y el resultado de clasificación en un solo procedimiento.
CREATE PROCEDURE Registrar_AnalisisConResultado (
    IN p_id_usuario INT,
    IN p_imagen LONGBLOB,
    IN p_id_clasificacion INT
)
BEGIN
    -- Validar que el usuario existe
    IF NOT EXISTS (SELECT 1 FROM Usuario WHERE ID_usuario = p_id_usuario) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El usuario no existe.';
    END IF;

    -- Validar que la clasificación existe
    IF NOT EXISTS (SELECT 1 FROM Clasificacion_arma WHERE ID_clasificacion = p_id_clasificacion) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La clasificación de arma no existe.';
    END IF;

    -- Registrar el análisis
    INSERT INTO Analisis (ID_usuario, Imagen_procesada)
    VALUES (p_id_usuario, p_imagen);

    -- Obtener el ID del análisis recién creado
    SET @ultimo_id_analisis = LAST_INSERT_ID();

    -- Registrar el resultado de la clasificación
    INSERT INTO Resultado_clasificacion (ID_analisis, ID_clasificacion)
    VALUES (@ultimo_id_analisis, p_id_clasificacion);
END;