ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS sentiment_label TEXT,
    ADD COLUMN IF NOT EXISTS sentiment_score REAL,
    ADD COLUMN IF NOT EXISTS sentiment_model TEXT,
    ADD COLUMN IF NOT EXISTS scored_at       TIMESTAMPTZ;

-- small index that only contains posts still waiting to be scored
CREATE INDEX IF NOT EXISTS idx_posts_unscored
    ON posts (id) WHERE sentiment_label IS NULL;