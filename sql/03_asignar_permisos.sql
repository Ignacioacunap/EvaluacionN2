-- 03_asignar_permisos.sql
-- Concede al usuario permisos SOLO sobre la base de datos del proyecto.
GRANT ALL PRIVILEGES ON voluntariado_db.* TO 'voluntariado_user'@'localhost';
FLUSH PRIVILEGES;
