

!-- 2. Procedimiento para validar datos del usuario Valida que los datos cumplen con ciertos criterios (longitud, unicidad del correo electrónico, etc.).

DELIMITER //
CREATE PROCEDURE ValidarDatosUsuario (
    IN p_nombre VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_contraseña VARCHAR(255)
)
BEGIN
    -- Validar que el nombre no excede la longitud permitida
    IF LENGTH(p_nombre) > 100 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El nombre excede el límite de 100 caracteres.';
    END IF;

    -- Validar que el correo es único
    IF EXISTS (SELECT 1 FROM Usuario WHERE Correo_electrónico = p_correo) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El correo electrónico ya está en uso.';
    END IF;

    -- Validar que la contraseña tiene al menos 8 caracteres
    IF LENGTH(p_contraseña) < 8 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La contraseña debe tener al menos 8 caracteres.';
    END IF;
END //
DELIMITER ;



!-- Procedimiento para registrar un usuario con validación previa  Usa el procedimiento de validación antes de registrar el usuario.


DELIMITER //
CREATE PROCEDURE RegistrarUsuarioValidado (
    IN p_nombre VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_contraseña VARCHAR(255),
    IN p_rol ENUM('Admin', 'Usuario')
)
BEGIN
    -- Llamar al procedimiento de validación
    CALL ValidarDatosUsuario(p_nombre, p_correo, p_contraseña);

    -- Registrar al usuario si todo es válido
    INSERT INTO Usuario (Nombre, Correo_electrónico, Contraseña, Rol)
    VALUES (p_nombre, p_correo, p_contraseña, p_rol);
END //
DELIMITER ;




!-- 4. Procedimiento para actualizar datos del usuario Permite al usuario actualizar sus datos, validando que no infringen restricciones.


DELIMITER //
CREATE PROCEDURE ActualizarDatosUsuario (
    IN p_id_usuario INT,
    IN p_nombre VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_contraseña VARCHAR(255)
)
BEGIN
    -- Validar que el usuario existe
    IF NOT EXISTS (SELECT 1 FROM Usuario WHERE ID_usuario = p_id_usuario) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El usuario no existe.';
    END IF;

    -- Llamar al procedimiento de validación
    CALL ValidarDatosUsuario(p_nombre, p_correo, p_contraseña);

    -- Actualizar datos del usuario
    UPDATE Usuario
    SET Nombre = p_nombre,
        Correo_electrónico = p_correo,
        Contraseña = p_contraseña
    WHERE ID_usuario = p_id_usuario;
END //
DELIMITER ;





!-- 5. Procedimiento para consultar el historial filtrado por fecha
-- Permite consultar el historial dentro de un rango de fechas.

DELIMITER //
CREATE PROCEDURE ConsultarHistorialPorFecha (
    IN p_fecha_inicio DATETIME,
    IN p_fecha_fin DATETIME
)
BEGIN
    -- Validar que las fechas son válidas
    IF p_fecha_inicio > p_fecha_fin THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de inicio no puede ser mayor que la fecha de fin.';
    END IF;

    -- Consultar el historial dentro del rango
    SELECT h.ID_historial,
           u.Nombre AS Usuario,
           a.Fecha_hora AS Fecha_analisis,
           c.Tipo_arma AS Tipo_arma,
           c.Descripcion AS Descripcion_arma
    FROM Historial h
    INNER JOIN Analisis a ON h.ID_analisis = a.ID_analisis
    INNER JOIN Usuario u ON a.ID_usuario = u.ID_usuario
    LEFT JOIN Resultado_clasificacion rc ON a.ID_analisis = rc.ID_analisis
    LEFT JOIN Clasificacion_arma c ON rc.ID_clasificacion = c.ID_clasificacion
    WHERE a.Fecha_hora BETWEEN p_fecha_inicio AND p_fecha_fin;
END //
DELIMITER ;



!-- 6. Procedimiento para registrar un análisis y su resultado Registra un análisis y el resultado de clasificación en un solo procedimiento.


DELIMITER //
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
END //
DELIMITER ;