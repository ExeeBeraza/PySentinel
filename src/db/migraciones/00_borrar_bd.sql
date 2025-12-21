-- Desactivar restricciones de FK temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar tablas en orden
DROP TABLE IF EXISTS Objeto_x_analisis;
DROP TABLE IF EXISTS analisis;
DROP TABLE IF EXISTS objeto;
DROP TABLE IF EXISTS usuario;

-- Reactivar restricciones de FK
SET FOREIGN_KEY_CHECKS = 1;

-- Eliminar stored procedures
DROP PROCEDURE IF EXISTS sp_registrar_usuario;
DROP PROCEDURE IF EXISTS sp_login_usuario;
DROP PROCEDURE IF EXISTS sp_insertar_analisis;
DROP PROCEDURE IF EXISTS sp_insertar_objeto_detectado;
DROP PROCEDURE IF EXISTS sp_guardar_resultado_completo;
DROP PROCEDURE IF EXISTS sp_obtener_historial_usuario;

-- Eliminar la base de datos completa (opcional, descomentar si es necesario)
-- DROP DATABASE IF EXISTS pysentinel;

SELECT '✅ Base de datos limpiada exitosamente' AS resultado;

