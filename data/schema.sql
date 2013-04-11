CREATE TABLE "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE "source" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "u_id" INTEGER NOT NULL,
    "username" TEXT,
    "password" TEXT,
    "host" TEXT,
    "port" INTEGER,
    "extra" TEXT,
    "title" TEXT,
    "provider" TEXT
);
CREATE TABLE "destination" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "u_id" INTEGER NOT NULL,
    "username" TEXT,
    "password" TEXT,
    "host" TEXT,
    "port" INTEGER,
    "extra" TEXT,
    "title" TEXT,
    "provider" TEXT
);
CREATE TABLE "profile" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "u_id" INTEGER,
    "s_id" INTEGER,
    "d_id" INTEGER,
    "schedule" TEXT,
    "repeat" INTEGER,
    "compress" INTEGER
);
