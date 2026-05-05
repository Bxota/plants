-- Migration 004 : ajout de la colonne JSONB levels sur plants
-- Structure : {"water": 1-5, "light": 1-5, "temp": 1-5, "humidity": 1-5, "fertilizer": 1-5}
-- null = pas encore évalué ; le frontend calcule des fallbacks depuis les champs texte.

ALTER TABLE plants ADD COLUMN IF NOT EXISTS levels JSONB;
