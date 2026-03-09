CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin      BOOLEAN NOT NULL DEFAULT false
);

-- Plantes (liées à un user)
CREATE TABLE IF NOT EXISTS plants (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    common_name     TEXT NOT NULL,
    scientific_name TEXT,
    emoji           TEXT DEFAULT '🌿',

    photo_url       TEXT,

    watering        TEXT,
    light           TEXT,
    temperature     TEXT,
    humidity        TEXT,
    fertilization   TEXT,

    notes           TEXT,
    tags            TEXT[] DEFAULT '{}',

    sort_order      INTEGER DEFAULT 0,

    ai_identified   BOOLEAN DEFAULT false,
    ai_raw_response JSONB
);

CREATE INDEX IF NOT EXISTS plants_user_id_idx ON plants(user_id);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS plants_updated_at ON plants;
CREATE TRIGGER plants_updated_at
    BEFORE UPDATE ON plants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- L'admin initial est créé au démarrage de l'app (via ADMIN_USERNAME + ADMIN_PASSWORD_HASH dans .env)
