SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS calendar_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_event_id TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    start_at DATETIME NOT NULL,
    end_at DATETIME NOT NULL,
    is_all_day BOOLEAN NOT NULL DEFAULT 0,
    notified_7d BOOLEAN NOT NULL DEFAULT 0,
    notified_3d BOOLEAN NOT NULL DEFAULT 0,
    notified_1d BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    delete_after DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS contents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_id TEXT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    author_name TEXT,
    published_at DATETIME,
    collected_at DATETIME NOT NULL,
    raw_text TEXT,
    summary TEXT,
    keywords TEXT,
    is_immediate_target BOOLEAN NOT NULL DEFAULT 0,
    is_briefing_target BOOLEAN NOT NULL DEFAULT 1,
    immediate_sent BOOLEAN NOT NULL DEFAULT 0,
    briefing_sent BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    delete_after DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS notification_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_type TEXT NOT NULL,
    target_id INTEGER NOT NULL,
    notification_type TEXT NOT NULL,
    discord_channel TEXT,
    sent_at DATETIME NOT NULL,
    status TEXT NOT NULL,
    message_preview TEXT,
    created_at DATETIME NOT NULL,
    delete_after DATETIME NOT NULL
);
"""