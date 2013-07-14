CREATE TABLE "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE source (id INTEGER PRIMARY KEY, u_id INTEGER, username TEXT, password TEXT, host TEXT, port INTEGER, extra TEXT, title TEXT, provider TEXT);
CREATE TABLE destination (id INTEGER PRIMARY KEY, u_id INTEGER, username TEXT, password TEXT, host TEXT, port INTEGER, extra TEXT, title TEXT, provider TEXT);
CREATE TABLE profile (id INTEGER PRIMARY KEY, u_id INTEGER, s_id INTEGER, d_id INTEGER, title TEXT, cron TEXT, compress INTEGER, email_notify INTEGER, split_size INTEGER);
CREATE TABLE event_log (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "type" TEXT,
    "text" TEXT,
    "created_at" TEXT,
    "j_id" INTEGER,
    "u_id" INTEGER,
    "event" TEXT
);
