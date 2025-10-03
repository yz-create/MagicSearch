-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS joueur CASCADE ;
CREATE TABLE joueur(
    id_joueur    SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    mdp          VARCHAR(256),
    age          INTEGER,
    mail         VARCHAR(50),
    fan_pokemon  BOOLEAN
);
