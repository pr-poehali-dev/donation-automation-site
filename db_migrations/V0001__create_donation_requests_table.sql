CREATE TABLE IF NOT EXISTS donation_requests (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(255) NOT NULL,
    amount INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    telegram_message_id VARCHAR(255)
);

CREATE INDEX idx_donation_status ON donation_requests(status);
CREATE INDEX idx_donation_created ON donation_requests(created_at DESC);