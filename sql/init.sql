CREATE TABLE IF NOT EXISTS facts(
    id                      SERIAL PRIMARY KEY,
    fact_number             INTEGER,
    fact_hash               CHAR(32) UNIQUE,
    fact                    TEXT,
    created_date            TIMESTAMPTZ,
    effective_start_date    TIMESTAMPTZ NOT NULL DEFAULT now(),
    effective_end_date      TIMESTAMPTZ,
    is_current              BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx__facts__is_current ON facts (is_current);

CREATE TABLE IF NOT EXISTS lsh_buckets (
    fact_id     INTEGER,
    bucket_hash INTEGER,
    FOREIGN KEY(fact_id) REFERENCES facts(id)
);

CREATE INDEX idx__lsh_buckets__bucket_hash ON lsh_buckets (bucket_hash);