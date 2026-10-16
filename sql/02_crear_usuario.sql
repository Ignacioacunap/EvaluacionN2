-- 02_crear_usuario.sql
-- Crea el usuario que usará Django (la clave debe ser igual a DB_PASSWORD del .env).
CREATE USER IF NOT EXISTS 'voluntariado_user'@'localhost' IDENTIFIED BY 'Cambiar_Esta_Clave_123';
