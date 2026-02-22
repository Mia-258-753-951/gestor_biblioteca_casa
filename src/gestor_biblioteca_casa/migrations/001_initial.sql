
-- Creación de la tabla de versiones
CREATE TABLE IF NOT EXISTS schema_versions (
    version INTEGER UNIQUE NOT NULL
);

-- Crea la versión 1 al inicial el schema, evita duplicidades (no saltará error del UNIQUE)
INSERT INTO schema_versions (version)
SELECT 1
WHERE NOT EXISTS (
    SELECT 1 FROM schema_versions WHERE version = 1
);

-- Creamos la tabla books
CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL
);