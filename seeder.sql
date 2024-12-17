INSERT INTO "users" ("username", "password", "is_admin")
VALUES ('admin', 'scrypt:32768:8:1$o3Yrx54yHYKC1LIV$464df00efa0064e32aefe239d895ce002a4b9aee40fe02f600cf108f99896cafcf51baa52e1787853becc588fd0777cd09b1720b033950e0c0900efbd42e4b0e', 1);

INSERT INTO "games" ("title", "description", "release_date")
VALUES ('Agni: Village of Calamity', 'Agni, a determined investigator from a covert Indonesian police unit who defied orders and ventures into a remote village despite ominous warnings. What begins as an unauthorized investigation quickly plunges Agni into a horrifying reality', UNIXEPOCH('1970-01-01')),
    ('A Space for the Unbound', 'A magical adventure about two high school sweethearts set at the end of their school days - and the end of the world. Explore a crumbling town and help friends face their inner demons, which could be the key to stopping reality itself disintegrating. And don’t forget to pet the cats.', UNIXEPOCH('2023-01-19')),
    ('DIVINATION', '"What if you''re born into this world without your permission?" DIVINATION is a very short visual novel where you act as a fortune teller in a futuristic world. Talk and listen to people''s stories, then foresee their future using the runes they had drawn.', UNIXEPOCH('2019-12-13')),
    ('DreadOut 2', 'A third-person horror adventure that draws inspiration from Indonesian urban legend. Play as Linda, a high school student with the ability to sense and see ghosts. This spine-chilling sequel expands on the cult hit original, making DreadOut 2 another terrifying addition to the horror genre.', UNIXEPOCH('2022-02-22'));

INSERT INTO "genres" ("name")
VALUES ('Adventure'),
    ('Horror'),
    ('MOBA'),
    ('Multiplayer'),
    ('Pixel Graphics'),
    ('Strategy'),
    ('Visual Novel');

INSERT INTO "platforms" ("name")
VALUES ('PC'),
    ('PlayStation 4'),
    ('PlayStation 5'),
    ('Xbox One'),
    ('Xbox Series X'),
    ('Nintendo Switch'),
    ('iOS'),
    ('Android');

INSERT INTO "companies" ("name", "founding_date")
VALUES ('Separuh Interactive', 0),
    ('Digital Happiness', UNIXEPOCH('2013-01-01')),
    ('Toge Productions', UNIXEPOCH('2009-01-20')),
    ('Mojiken Studio', UNIXEPOCH('2013-01-01'));

INSERT INTO "headquarters" ("company_id", "location")
VALUES (
    (SELECT "id" FROM "companies" WHERE "name" = 'Separuh Interactive'),
    'Jakarta'
), (
    (SELECT "id" FROM "companies" WHERE "name" = 'Digital Happiness'),
    'Bandung, West Java'
);

INSERT INTO "roles" ("name")
VALUES ('Developer'),
    ('Publisher');

INSERT INTO "game_genres" ("game_id", "genre_id")
VALUES (
    (SELECT "id" FROM "games" WHERE "title" = 'Agni: Village of Calamity'), 
    (SELECT "id" FROM "genres" WHERE "name" = 'Adventure')
), (
    (SELECT "id" FROM "games" WHERE "title" = 'Agni: Village of Calamity'), 
    (SELECT "id" FROM "genres" WHERE "name" = 'Horror')
), (
    (SELECT "id" FROM "games" WHERE "title" = 'A Space for the Unbound'),
    (SELECT "id" FROM "genres" WHERE "name" = 'Adventure')
), (
    (SELECT "id" FROM "games" WHERE "title" = 'A Space for the Unbound'),
    (SELECT "id" FROM "genres" WHERE "name" = 'Pixel Graphics')
);

INSERT INTO "game_platforms" ("game_id", "platform_id")
VALUES (
    (SELECT "id" FROM "games" WHERE "title" = 'Agni: Village of Calamity'),
    (SELECT "id" FROM "platforms" WHERE "name" = 'PC')
), (
    (SELECT "id" FROM "games" WHERE "title" = 'Agni: Village of Calamity'),
    (SELECT "id" FROM "platforms" WHERE "name" = 'PlayStation 4')
);

INSERT INTO "game_companies" ("game_id", "company_id")
VALUES (
    (SELECT "id" FROM "games" WHERE "title" = 'Agni: Village of Calamity'),
    (SELECT "id" FROM "companies" WHERE "name" = 'Separuh Interactive')
), (
    (SELECT "id" FROM "games" WHERE "title" = 'Agni: Village of Calamity'),
    (SELECT "id" FROM "companies" WHERE "name" = 'Digital Happiness')
);

INSERT INTO "company_roles" ("company_id", "role_id")
VALUES (
    (SELECT "id" FROM "companies" WHERE "name" = 'Separuh Interactive'),
    (SELECT "id" FROM "roles" WHERE "name" = 'Developer')
), (
    (SELECT "id" FROM "companies" WHERE "name" = 'Separuh Interactive'),
    (SELECT "id" FROM "roles" WHERE "name" = 'Publisher')
), (
    (SELECT "id" FROM "companies" WHERE "name" = 'Digital Happiness'),
    (SELECT "id" FROM "roles" WHERE "name" = 'Developer')
);