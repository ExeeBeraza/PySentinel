a. Registrar automáticamente en el historial cada vez que se crea un análisis

sql
Copiar código
DELIMITER $$
CREATE TRIGGER AfterInsertAnalisis
AFTER INSERT ON Analisis
FOR EACH ROW
BEGIN
    INSERT INTO Historial (ID_analisis)
    VALUES (NEW.ID_analisis);
END $$
DELIMITER ;