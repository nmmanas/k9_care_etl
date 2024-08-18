-- connect to new db
\connect k9_care

-- create tables
CREATE TABLE IF NOT EXISTS facts(
    id                      SERIAL PRIMARY KEY,
    fact_number             INTEGER NOT NULL,
    fact_hash               CHAR(32) UNIQUE,
    fact                    TEXT NOT NULL,
    created_date            TIMESTAMPTZ NOT NULL,
    is_numeric              BOOLEAN NOT NULL DEFAULT FALSE,
    effective_start_date    TIMESTAMPTZ NOT NULL DEFAULT now(),
    effective_end_date      TIMESTAMPTZ,
    is_current              BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx__facts__is_current ON facts (is_current);
CREATE INDEX idx__facts__is_numeric ON facts (is_numeric);

CREATE TABLE IF NOT EXISTS lsh_buckets (
    fact_id     INTEGER,
    bucket_hash BIGINT,
    FOREIGN KEY(fact_id) REFERENCES facts(id)
);

CREATE INDEX idx__lsh_buckets__bucket_hash ON lsh_buckets (bucket_hash);