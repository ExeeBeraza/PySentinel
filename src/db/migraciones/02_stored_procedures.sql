-- =============================================================================
-- PySentinel - Stored Procedures
-- =============================================================================

USE pysentinel;

-- Eliminar procedures existentes
DROP PROCEDURE IF EXISTS sp_registrar_usuario;
DROP PROCEDURE IF EXISTS sp_login_usuario;
DROP PROCEDURE IF EXISTS sp_insertar_analisis;
DROP PROCEDURE IF EXISTS sp_insertar_objeto_detectado;
DROP PROCEDURE IF EXISTS sp_guardar_resultado_completo;
DROP PROCEDURE IF EXISTS sp_obtener_historial_usuario;
DROP PROCEDURE IF EXISTS sp_obtener_perfil_usuario;
DROP PROCEDURE IF EXISTS sp_actualizar_perfil_usuario;

DELIMITER $$

-- =============================================================================
-- sp_registrar_usuario
-- =============================================================================
CREATE PROCEDURE sp_registrar_usuario(
    IN p_username VARCHAR(30),
    IN p_nombre VARCHAR(50),
    IN p_correo VARCHAR(50),
    IN p_contrasenia VARCHAR(100),
    IN p_rol VARCHAR(20)
)
BEGIN
    DECLARE v_existe_correo INT DEFAULT 0;
    DECLARE v_existe_username INT DEFAULT 0;
    DECLARE v_rol VARCHAR(20);
    SELECT COUNT(*) INTO v_existe_username FROM usuario WHERE username = p_username;
    IF v_existe_username > 0 THEN
        SELECT FALSE AS exito, 'El nombre de usuario ya está en uso' AS mensaje, NULL AS id_usuario;
    ELSE
        SELECT COUNT(*) INTO v_existe_correo FROM usuario WHERE correo_electronico = p_correo;
        IF v_existe_correo > 0 THEN
            SELECT FALSE AS exito, 'El correo electrónico ya está registrado' AS mensaje, NULL AS id_usuario;
        ELSE
            SET v_rol = IFNULL(p_rol, 'usuario');
            INSERT INTO usuario (username, nombre, correo_electronico, contrasenia, rol) VALUES (p_username, p_nombre, p_correo, p_contrasenia, v_rol);
            SELECT TRUE AS exito, 'Usuario registrado exitosamente' AS mensaje, LAST_INSERT_ID() AS id_usuario;
        END IF;
    END IF;
END$$

-- =============================================================================
-- sp_login_usuario
-- =============================================================================
CREATE PROCEDURE sp_login_usuario(
    IN p_username VARCHAR(30),
    IN p_contrasenia VARCHAR(100)
)
BEGIN
    DECLARE v_id_usuario INT DEFAULT NULL;
    DECLARE v_nombre VARCHAR(50);
    DECLARE v_rol VARCHAR(20);
    SELECT id_usuario, nombre, rol INTO v_id_usuario, v_nombre, v_rol FROM usuario WHERE username = p_username AND contrasenia = p_contrasenia LIMIT 1;
    IF v_id_usuario IS NOT NULL THEN
        SELECT TRUE AS exito, 'Login exitoso' AS mensaje, v_id_usuario AS id_usuario, v_nombre AS nombre, v_rol AS rol;
    ELSE
        SELECT FALSE AS exito, 'Usuario o contrasenia incorrectos' AS mensaje, NULL AS id_usuario, NULL AS nombre, NULL AS rol;
    END IF;
END$$

-- =============================================================================
-- sp_insertar_analisis
-- =============================================================================
CREATE PROCEDURE sp_insertar_analisis(
    IN p_id_usuario INT,
    IN p_fecha_hora DATETIME,
    IN p_imagen_procesada LONGBLOB
)
BEGIN
    DECLARE v_usuario_existe INT DEFAULT 0;
    DECLARE v_fecha DATETIME;
    SELECT COUNT(*) INTO v_usuario_existe FROM usuario WHERE id_usuario = p_id_usuario;
    IF v_usuario_existe = 0 THEN
        SELECT FALSE AS exito, 'El usuario no existe' AS mensaje, NULL AS id_analisis;
    ELSE
        SET v_fecha = IFNULL(p_fecha_hora, NOW());
        INSERT INTO analisis (id_usuario, fecha_hora, imagen_procesada) VALUES (p_id_usuario, v_fecha, p_imagen_procesada);
        SELECT TRUE AS exito, 'Análisis guardado exitosamente' AS mensaje, LAST_INSERT_ID() AS id_analisis;
    END IF;
END$$

-- =============================================================================
-- sp_insertar_objeto_detectado
-- =============================================================================
CREATE PROCEDURE sp_insertar_objeto_detectado(
    IN p_id_analisis INT,
    IN p_nombre_objeto VARCHAR(50),
    IN p_porcentaje_fiabilidad DECIMAL(5,2)
)
BEGIN
    DECLARE v_id_objeto INT DEFAULT NULL;
    DECLARE v_analisis_existe INT DEFAULT 0;
    SELECT COUNT(*) INTO v_analisis_existe FROM analisis WHERE id_analisis = p_id_analisis;
    IF v_analisis_existe = 0 THEN
        SELECT FALSE AS exito, 'El análisis no existe' AS mensaje;
    ELSE
        SELECT id_objeto INTO v_id_objeto FROM objeto WHERE nombre = p_nombre_objeto LIMIT 1;
        IF v_id_objeto IS NULL THEN
            INSERT INTO objeto (nombre) VALUES (p_nombre_objeto);
            SET v_id_objeto = LAST_INSERT_ID();
        END IF;
        INSERT IGNORE INTO Objeto_x_analisis (id_objeto, id_analisis, porcentaje_fiabilidad) VALUES (v_id_objeto, p_id_analisis, p_porcentaje_fiabilidad);
        SELECT TRUE AS exito, 'Objeto detectado registrado' AS mensaje;
    END IF;
END$$

-- =============================================================================
-- sp_guardar_resultado_completo
-- =============================================================================
CREATE PROCEDURE sp_guardar_resultado_completo(
    IN p_id_usuario INT,
    IN p_fecha_hora DATETIME,
    IN p_imagen_procesada LONGBLOB,
    IN p_objetos_json JSON
)
BEGIN
    DECLARE v_id_analisis INT;
    DECLARE v_usuario_existe INT DEFAULT 0;
    DECLARE v_i INT DEFAULT 0;
    DECLARE v_total_objetos INT;
    DECLARE v_nombre_objeto VARCHAR(50);
    DECLARE v_porcentaje_fiabilidad DECIMAL(5,2);
    DECLARE v_id_objeto INT;
    DECLARE v_fecha DATETIME;
    SELECT COUNT(*) INTO v_usuario_existe FROM usuario WHERE id_usuario = p_id_usuario;
    IF v_usuario_existe = 0 THEN
        SELECT FALSE AS exito, 'El usuario no existe' AS mensaje, NULL AS id_analisis;
    ELSE
        SET v_fecha = IFNULL(p_fecha_hora, NOW());
        START TRANSACTION;
        INSERT INTO analisis (id_usuario, fecha_hora, imagen_procesada) VALUES (p_id_usuario, v_fecha, p_imagen_procesada);
        SET v_id_analisis = LAST_INSERT_ID();
        SET v_total_objetos = JSON_LENGTH(p_objetos_json);
        WHILE v_i < v_total_objetos DO
            SET v_nombre_objeto = JSON_UNQUOTE(JSON_EXTRACT(p_objetos_json, CONCAT('$[', v_i, '].nombre')));
            SET v_porcentaje_fiabilidad = JSON_EXTRACT(p_objetos_json, CONCAT('$[', v_i, '].porcentaje_fiabilidad'));
            SELECT id_objeto INTO v_id_objeto FROM objeto WHERE nombre = v_nombre_objeto LIMIT 1;
            IF v_id_objeto IS NULL THEN
                INSERT INTO objeto (nombre) VALUES (v_nombre_objeto);
                SET v_id_objeto = LAST_INSERT_ID();
            END IF;
            INSERT IGNORE INTO Objeto_x_analisis (id_objeto, id_analisis, porcentaje_fiabilidad) VALUES (v_id_objeto, v_id_analisis, v_porcentaje_fiabilidad);
            SET v_id_objeto = NULL;
            SET v_i = v_i + 1;
        END WHILE;
        COMMIT;
        SELECT TRUE AS exito, 'Resultado guardado exitosamente' AS mensaje, v_id_analisis AS id_analisis;
    END IF;
END$$

-- =============================================================================
-- sp_obtener_historial_usuario
-- =============================================================================
CREATE PROCEDURE sp_obtener_historial_usuario(
    IN p_id_usuario INT,
    IN p_limite INT
)
BEGIN
    DECLARE v_limite INT;
    SET v_limite = IFNULL(p_limite, 50);
    SELECT a.id_analisis, a.fecha_hora,
        GROUP_CONCAT(CONCAT(o.nombre, ' (', ROUND(oxa.porcentaje_fiabilidad, 1), '%)') ORDER BY oxa.porcentaje_fiabilidad DESC SEPARATOR ', ') AS objetos_detectados,
        COUNT(oxa.id_objeto) AS total_objetos
    FROM analisis a
    LEFT JOIN Objeto_x_analisis oxa ON a.id_analisis = oxa.id_analisis
    LEFT JOIN objeto o ON oxa.id_objeto = o.id_objeto
    WHERE a.id_usuario = p_id_usuario
    GROUP BY a.id_analisis, a.fecha_hora
    ORDER BY a.fecha_hora DESC
    LIMIT v_limite;
END$$

-- =============================================================================
-- sp_obtener_perfil_usuario
-- =============================================================================
CREATE PROCEDURE sp_obtener_perfil_usuario(
    IN p_id_usuario INT
)
BEGIN
    SELECT u.id_usuario, u.username, u.nombre, u.correo_electronico, u.fecha_registro, u.rol,
        (SELECT COUNT(*) FROM analisis WHERE id_usuario = p_id_usuario) AS total_analisis
    FROM usuario u WHERE u.id_usuario = p_id_usuario;
END$$

-- =============================================================================
-- sp_actualizar_perfil_usuario
-- =============================================================================
CREATE PROCEDURE sp_actualizar_perfil_usuario(
    IN p_id_usuario INT,
    IN p_nombre VARCHAR(50),
    IN p_correo VARCHAR(50)
)
BEGIN
    DECLARE v_usuario_existe INT DEFAULT 0;
    DECLARE v_correo_duplicado INT DEFAULT 0;
    SELECT COUNT(*) INTO v_usuario_existe FROM usuario WHERE id_usuario = p_id_usuario;
    IF v_usuario_existe = 0 THEN
        SELECT FALSE AS exito, 'El usuario no existe' AS mensaje;
    ELSE
        SELECT COUNT(*) INTO v_correo_duplicado FROM usuario WHERE correo_electronico = p_correo AND id_usuario != p_id_usuario;
        IF v_correo_duplicado > 0 THEN
            SELECT FALSE AS exito, 'El correo electrónico ya está en uso por otro usuario' AS mensaje;
        ELSE
            UPDATE usuario SET nombre = p_nombre, correo_electronico = p_correo WHERE id_usuario = p_id_usuario;
            SELECT TRUE AS exito, 'Perfil actualizado exitosamente' AS mensaje;
        END IF;
    END IF;
END$$

DELIMITER ;
