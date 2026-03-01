
-- Creación de la tabla de versiones
CREATE TABLE IF NOT EXISTS schema_versions (
    version INTEGER UNIQUE NOT NULL
);

-- Crea la versión 2 al iniciar el schema, evita duplicidades (no saltará error del UNIQUE)
INSERT INTO schema_versions (version)
SELECT 2
WHERE NOT EXISTS (
    SELECT 1 FROM schema_versions WHERE version = 2
);

-- Creamos la nueva fila 
ALTER TABLE books
ADD acquired_at TEXT DEFAULT "2025-01-01";