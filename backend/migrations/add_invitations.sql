-- Migration : ajout de la table invitations
CREATE TABLE IF NOT EXISTS invitations (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    token         UUID NOT NULL UNIQUE DEFAULT uuid_generate_v4(),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at    TIMESTAMPTZ,
    used_at       TIMESTAMPTZ,
    created_by_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    used_by_id    UUID REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS invitations_token_idx ON invitations(token);
