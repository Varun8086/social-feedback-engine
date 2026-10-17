CREATE TABLE sources (
    id          SERIAL PRIMARY KEY,
    platform    TEXT NOT NULL,          -- 'reddit' | 'youtube'
    external_id TEXT NOT NULL,          -- subreddit name or video id
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (platform, external_id)
);

CREATE TABLE posts (
    id                BIGSERIAL PRIMARY KEY,
    source_id         INT NOT NULL REFERENCES sources(id),
    external_id       TEXT NOT NULL,    -- the platform's own post/comment id
    author            TEXT,
    title             TEXT,
    body              TEXT NOT NULL,
    url               TEXT,
    score             INT,
    posted_at         TIMESTAMPTZ NOT NULL,
    ingested_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_id, external_id)
);

CREATE INDEX idx_posts_posted_at ON posts (posted_at);

CREATE TABLE ingestion_runs (
    id              SERIAL PRIMARY KEY,
    source_id       INT REFERENCES sources(id),
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at     TIMESTAMPTZ,
    status          TEXT NOT NULL DEFAULT 'running',  -- running | success | failed
    posts_fetched   INT DEFAULT 0,
    posts_inserted  INT DEFAULT 0,
    error           TEXT
);