CREATE TABLE IF NOT EXISTS facts(
    fact_hash      CHAR(32) PRIMARY KEY,
    fact            TEXT,
    created_date    TIMESTAMP
);