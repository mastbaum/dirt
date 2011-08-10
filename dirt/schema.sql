CREATE TABLE IF NOT EXISTS record (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "number" integer NOT NULL,
    "description" text NOT NULL,
    "uuid" text
);

CREATE TABLE IF NOT EXISTS slave (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "hostname" varchar(100) NOT NULL,
    "last_login" datetime,
    "password" varchar(128) NOT NULL,
    "enabled" bool NOT NULL
);

CREATE TABLE IF NOT EXISTS task (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(100) NOT NULL,
    "record_id" integer NOT NULL REFERENCES record (id),
    "created" datetime NOT NULL,
    "slave_id" integer REFERENCES slave (id),
    "checked_out" datetime,
    "completed" datetime,
    "success" bool NOT NULL,
    "results" blob,
    "task_type" varchar(100) NOT NULL,
    "platform" varchar(50) NOT NULL
);

