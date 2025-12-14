

a. Vista para consultar el historial con información detallada del usuario y análisis

sql
Copiar código
CREATE VIEW VistaHistorial AS
SELECT 
    h.ID_historial,
    u.Nombre AS Usuario,
    a.Fecha_hora AS Fecha_analisis,
    c.Tipo_arma AS Tipo_arma,
    c.Descripcion AS Descripcion_arma
FROM 
    Historial h
    INNER JOIN Analisis a ON h.ID_analisis = a.ID_analisis
    INNER JOIN Usuario u ON a.ID_usuario = u.ID_usuario
    LEFT JOIN Resultado_clasificacion rc ON a.ID_analisis = rc.ID_analisis
    LEFT JOIN Clasificacion_arma c ON rc.ID_clasificacion = c.ID_clasificacion;
Consideraciones adicionales


sql
Copiar código
DELIMITER $$
CREATE PROCEDURE GuardarEnHistorial (
    IN p_id_analisis INT
)
BEGIN
    -- Validar que el análisis existe antes de guardarlo en el historial
    IF EXISTS (SELECT 1 FROM Analisis WHERE ID_analisis = p_id_analisis) THEN
        INSERT INTO Historial (ID_analisis)
        VALUES (p_id_analisis);
    ELSE
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'El ID de análisis no existe.';
    END IF;
END $$
DELIMITER ;