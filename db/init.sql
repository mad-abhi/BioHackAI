-- This table stores the raw data from health devices/APIs
CREATE TABLE IF NOT EXISTS health_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT,         -- e.g., 'Google_Fit'
    metric_type TEXT,    -- e.g., 'heart_rate'
    value FLOAT
);

-- This table stores your voice notes and the AI's "extraction"
CREATE TABLE IF NOT EXISTS voice_journals (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_transcript TEXT,
    structured_json JSONB, -- The key-value pairs Llama extracts
    sentiment TEXT
);