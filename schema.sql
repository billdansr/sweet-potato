DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "user_profiles";
DROP TABLE IF EXISTS "games";
DROP TABLE IF EXISTS "media";
DROP TABLE IF EXISTS "ratings";
DROP TABLE IF EXISTS "platforms";
DROP TABLE IF EXISTS "game_platforms";
DROP TABLE IF EXISTS "genres";
DROP TABLE IF EXISTS "game_genres";
DROP TABLE IF EXISTS "companies";
DROP TABLE IF EXISTS "headquarters";
DROP TABLE IF EXISTS "game_companies";
DROP TABLE IF EXISTS "roles";
DROP TABLE IF EXISTS "company_roles";
DROP VIEW IF EXISTS "view_upcoming_games";
DROP VIEW IF EXISTS "view_recent_games";
DROP VIEW IF EXISTS "view_popular_games";
DROP VIEW IF EXISTS "view_top_rated_games";
DROP VIEW IF EXISTS "view_game_genres";
DROP VIEW IF EXISTS "view_game_platforms";
DROP VIEW IF EXISTS "view_game_companies";
DROP TRIGGER IF EXISTS "trigger_update_user_profile";
DROP TRIGGER IF EXISTS "trigger_update_rating";

CREATE TABLE "users" (
    "id" INTEGER,
    "username" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "is_admin" NUMERIC NOT NULL DEFAULT 0 CHECK("is_admin" IN (0, 1)),
    "created_at" INTEGER DEFAULT (unixepoch('now')),
    PRIMARY KEY("id")
);

CREATE TABLE "user_profiles" (
    "user_id" INTEGER,
    "name" TEXT,
    "avatar_filename" TEXT,
    "updated_at" INTEGER,
    PRIMARY KEY("user_id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "games" (
    "id" INTEGER,
    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT,
    "release_date" INTEGER,
    PRIMARY KEY("id")
);

CREATE TABLE "media" (
    "id" INTEGER,
    "game_id" INTEGER,
    "filename" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id"),
    FOREIGN KEY("game_id") REFERENCES "games"("id") ON DELETE RESTRICT ON UPDATE SET NULL
);

CREATE TABLE "ratings" (
    "user_id" INTEGER,
    "game_id" INTEGER,
    "score" INTEGER NOT NULL DEFAULT 0 CHECK("score" BETWEEN 0 AND 10),
    "review" TEXT,
    "created_at" INTEGER DEFAULT (unixepoch('now')),
    "updated_at" INTEGER,
    PRIMARY KEY("user_id", "game_id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY("game_id") REFERENCES "games"("id") ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE "platforms" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

CREATE TABLE "game_platforms" (
    "game_id" INTEGER,
    "platform_id" INTEGER,
    PRIMARY KEY("game_id", "platform_id"),
    FOREIGN KEY("game_id") REFERENCES "games"("id") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY("platform_id") REFERENCES "platforms"("id") ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "genres" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

CREATE TABLE "game_genres" (
    "game_id" INTEGER,
    "genre_id" INTEGER,
    PRIMARY KEY("game_id", "genre_id"),
    FOREIGN KEY("game_id") REFERENCES "games"("id") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY("genre_id") REFERENCES "genres"("id") ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "companies" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "founding_date" INTEGER,
    PRIMARY KEY("id")
);

CREATE TABLE "headquarters" (
    "id" INTEGER,
    "company_id" INTEGER,
    "location" TEXT NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("company_id") REFERENCES "companies"("id") ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "game_companies" (
    "game_id" INTEGER,
    "company_id" INTEGER,
    PRIMARY KEY("game_id", "company_id"),
    FOREIGN KEY("game_id") REFERENCES "games"("id") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY("company_id") REFERENCES "companies"("id") ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "roles" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

CREATE TABLE "company_roles" (
    "company_id" INTEGER,
    "role_id" INTEGER,
    PRIMARY KEY("company_id", "role_id"),
    FOREIGN KEY("company_id") REFERENCES "companies"("id") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY("role_id") REFERENCES "roles"("id") ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE VIEW "view_upcoming_games" AS
SELECT * FROM "games"
WHERE "release_date" > (unixepoch('now'));

CREATE VIEW "view_recent_games" AS
SELECT * FROM "games"
WHERE "release_date" <= (unixepoch('now'))
ORDER BY "release_date" DESC;

CREATE VIEW "view_popular_games" AS
SELECT "games"."id",
    "games"."title",
    "games"."description",
    "games"."release_date",
    COUNT("ratings"."score") AS "rating_count"
FROM "games"
INNER JOIN "ratings"
ON "ratings"."game_id" = "games"."id"
GROUP BY "games"."id",
    "games"."title",
    "games"."description",
    "games"."release_date"
ORDER BY "rating_count" DESC;

CREATE VIEW "view_top_rated_games" AS
SELECT "games"."id",
    "games"."title",
    "games"."description",
    "games"."release_date",
    AVG("ratings"."score") AS "average_score",
    DENSE_RANK() OVER(ORDER BY "average_score" DESC) AS "rank"
FROM "games"
INNER JOIN "ratings"
ON "ratings"."game_id" = "games"."id"
GROUP BY "games"."id",
    "games"."title",
    "games"."description",
    "games"."release_date"
ORDER BY "average_score" DESC;

CREATE VIEW "view_game_genres" AS
SELECT "games"."id" AS "game_id",
    "games"."title",
    "games"."description",
    "games"."release_date",
    "genres"."id" AS "genre_id",
    "genres"."name" AS "genre"
FROM "games"
INNER JOIN "game_genres" ON "game_genres"."game_id" = "games"."id"
INNER JOIN "genres" ON "genres"."id" = "game_genres"."genre_id";

CREATE VIEW "view_game_platforms" AS
SELECT "games"."id" AS "game_id",
    "games"."title",
    "games"."description",
    "games"."release_date",
    "platforms"."id" AS "platform_id",
    "platforms"."name" AS "platform"
FROM "games"
INNER JOIN "game_platforms" ON "game_platforms"."game_id" = "games"."id"
INNER JOIN "platforms" ON "platforms"."id" = "game_platforms"."platform_id";

CREATE VIEW "view_game_companies" AS
SELECT "games"."id" AS "game_id",
    "games"."title",
    "games"."description",
    "games"."release_date",
    "companies"."id" AS "company_id",
    "companies"."name" AS "company"
FROM "games"
INNER JOIN "game_companies" ON "game_companies"."game_id" = "games"."id"
INNER JOIN "companies" ON "companies"."id" = "game_companies"."company_id";

CREATE TRIGGER "trigger_update_user_profile"
AFTER UPDATE
ON "user_profiles"
FOR EACH ROW
BEGIN
    UPDATE "user_profiles"
    SET "updated_at" = (unixepoch('now'))
    WHERE "user_id" = NEW."user_id";
END;

CREATE TRIGGER "trigger_update_rating"
AFTER UPDATE
ON "ratings"
FOR EACH ROW
BEGIN
    UPDATE "ratings"
    SET "updated_at" = (unixepoch('now'))
    WHERE "user_id" = NEW."user_id" AND "game_id" = NEW."game_id";
END;