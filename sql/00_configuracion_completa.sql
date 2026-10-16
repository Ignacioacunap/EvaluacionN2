-- 00_configuracion_completa.sql
-- Ejecuta los tres pasos en un solo script (alternativa a los archivos 01, 02 y 03).
--   mysql -u root -p < sql/00_configuracion_completa.sql

-- 1) Crear base de datos
CREATE DATABASE IF NOT EXISTS voluntariado_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 2) Crear usuario
CREATE USER IF NOT EXISTS 'voluntariado_user'@'localhost' IDENTIFIED BY 'Cambiar_Esta_Clave_123';

-- 3) Asignar permisos
GRANT ALL PRIVILEGES ON voluntariado_db.* TO 'voluntariado_user'@'localhost';
FLUSH PRIVILEGES;
