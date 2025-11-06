CREATE TABLE "Card" (
  "idCard" int PRIMARY KEY NOT NULL,
  "layout" int NOT NULL,
  "name" VARCHAR(500) NOT NULL,
  "type" int NOT NULL,
  "embed" vector(1024) NOT NULL,
  "shortEmbed" vector(1024) NOT NULL,
  "asciiName" VARCHAR(500),
  "convertedManaCost" float,
  "defense" int,
  "edhrecRank" int,
  "edhrecSaltiness" float,
  "faceManaValue" float,
  "faceName" VARCHAR(500),
  "firstPrinting" int,
  "hand" int,
  "hasAlternativeDeckLimit" bool,
  "isFunny" bool,
  "isReserved" bool,
  "leadershipSkills" int,
  "legalities" int,
  "life" int,
  "loyalty" VARCHAR(500),
  "manaCost" VARCHAR(500),
  "manaValue" float,
  "power" VARCHAR(500),
  "side" VARCHAR(500),
  "text" VARCHAR(10000),
  "toughness" VARCHAR(500)
);

CREATE TABLE "User" (
  "idUser" int PRIMARY KEY NOT NULL,
  "username" VARCHAR(500) NOT NULL,
  "password" VARCHAR(500) NOT NULL,
  "isAdmin" bool NOT NULL
);

CREATE TABLE "Favourite" (
  "idUser" int NOT NULL,
  "idCard" int NOT NULL,
  PRIMARY KEY ("idUser", "idCard")
);

CREATE TABLE "Color" (
  "idColor" int PRIMARY KEY NOT NULL,
  "colorName" VARCHAR(500) NOT NULL
);

CREATE TABLE "Colors" (
  "idCard" int NOT NULL,
  "idColor" int NOT NULL,
  PRIMARY KEY ("idCard", "idColor")
);

CREATE TABLE "ColorIdentity" (
  "idCard" int NOT NULL,
  "idColor" int NOT NULL,
  PRIMARY KEY ("idCard", "idColor")
);

CREATE TABLE "ColorIndicator" (
  "idCard" int NOT NULL,
  "idColor" int NOT NULL,
  PRIMARY KEY ("idCard", "idColor")
);

CREATE TABLE "ForeignData" (
  "idForeign" int PRIMARY KEY NOT NULL,
  "idCard" int NOT NULL,
  "language" VARCHAR(500) NOT NULL,
  "name" VARCHAR(500) NOT NULL,
  "faceName" VARCHAR(500),
  "flavorText" VARCHAR(500),
  "text" VARCHAR(10000),
  "type" VARCHAR(500)
);

CREATE TABLE "Keyword" (
  "idKeyword" int PRIMARY KEY NOT NULL,
  "name" VARCHAR(500) NOT NULL
);

CREATE TABLE "Keywords" (
  "idCard" int NOT NULL,
  "idKeyword" int NOT NULL,
  PRIMARY KEY ("idCard", "idKeyword")
);

CREATE TABLE "Set" (
  "idSet" int PRIMARY KEY NOT NULL,
  "name" VARCHAR(500) NOT NULL
);

CREATE TABLE "Layout" (
  "idLayout" int PRIMARY KEY NOT NULL,
  "name" VARCHAR(500) NOT NULL
);

CREATE TABLE "LeadershipSkills" (
  "idLeadership" int PRIMARY KEY NOT NULL,
  "brawl" bool NOT NULL,
  "commander" bool NOT NULL,
  "oathbreaker" bool NOT NULL
);

CREATE TABLE "Legality" (
  "idLegality" int PRIMARY KEY NOT NULL,
  "commander" int,
  "oathbreaker" int,
  "duel" int,
  "legacy" int,
  "vintage" int,
  "modern" int,
  "penny" int,
  "timeless" int,
  "brawl" int,
  "historic" int,
  "gladiator" int,
  "pioneer" int,
  "predh" int,
  "paupercommander" int,
  "pauper" int,
  "premodern" int,
  "future" int,
  "standardbrawl" int,
  "standard" int,
  "alchemy" int,
  "oldschool" int
);

CREATE TABLE "LegalityType" (
  "idLegalityType" int PRIMARY KEY NOT NULL,
  "type" VARCHAR(500) NOT NULL
);

CREATE TABLE "Printings" (
  "idCard" int NOT NULL,
  "idSet" int NOT NULL,
  PRIMARY KEY ("idSet", "idCard")
);

CREATE TABLE "PurchaseURLs" (
  "idPurchaseURLs" int PRIMARY KEY NOT NULL,
  "idCard" int NOT NULL,
  "tcgplayer" VARCHAR(500),
  "cardKingdom" VARCHAR(500),
  "cardmarket" VARCHAR(500),
  "cardKingdomFoil" VARCHAR(500),
  "cardKingdomEtched" VARCHAR(500),
  "tcgplayerEtched" VARCHAR(500)
);

CREATE TABLE "Ruling" (
  "idRuling" int PRIMARY KEY NOT NULL,
  "idCard" int NOT NULL,
  "date" date NOT NULL,
  "text" VARCHAR(10000) NOT NULL
);

CREATE TABLE "Subtype" (
  "idSubtype" int PRIMARY KEY,
  "name" VARCHAR(500)
);

CREATE TABLE "Subtypes" (
  "idCard" int NOT NULL,
  "idSubtype" int NOT NULL,
  PRIMARY KEY ("idSubtype", "idCard")
);

CREATE TABLE "Supertype" (
  "idSupertype" int PRIMARY KEY,
  "name" VARCHAR(500)
);

CREATE TABLE "Supertypes" (
  "idCard" int NOT NULL,
  "idSupertype" int NOT NULL,
  PRIMARY KEY ("idSupertype", "idCard")
);

CREATE TABLE "Type" (
  "idType" int PRIMARY KEY,
  "name" VARCHAR(500)
);

CREATE TABLE "Types" (
  "idCard" int NOT NULL,
  "idType" int NOT NULL,
  PRIMARY KEY ("idType", "idCard")
);

ALTER TABLE "Card" ADD FOREIGN KEY ("layout") REFERENCES "Layout" ("idLayout");

ALTER TABLE "Card" ADD FOREIGN KEY ("legalities") REFERENCES "Legality" ("idLegality");

ALTER TABLE "Card" ADD FOREIGN KEY ("firstPrinting") REFERENCES "Set" ("idSet");

ALTER TABLE "Card" ADD FOREIGN KEY ("type") REFERENCES "Type" ("idType");

ALTER TABLE "Card" ADD FOREIGN KEY ("leadershipSkills") REFERENCES "LeadershipSkills" ("idLeadership");

ALTER TABLE "Favourite" ADD FOREIGN KEY ("idUser") REFERENCES "User" ("idUser");

ALTER TABLE "Favourite" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Colors" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Colors" ADD FOREIGN KEY ("idColor") REFERENCES "Color" ("idColor");

ALTER TABLE "ColorIdentity" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "ColorIdentity" ADD FOREIGN KEY ("idColor") REFERENCES "Color" ("idColor");

ALTER TABLE "ColorIndicator" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "ColorIndicator" ADD FOREIGN KEY ("idColor") REFERENCES "Color" ("idColor");

ALTER TABLE "ForeignData" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Keywords" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Keywords" ADD FOREIGN KEY ("idKeyword") REFERENCES "Keyword" ("idKeyword");

ALTER TABLE "Legality" ADD FOREIGN KEY ("commander") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("oathbreaker") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("duel") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("legacy") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("vintage") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("modern") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("penny") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("timeless") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("brawl") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("historic") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("gladiator") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("pioneer") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("predh") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("paupercommander") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("pauper") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("premodern") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("future") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("standardbrawl") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("standard") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("alchemy") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("oldschool") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Printings" ADD FOREIGN KEY ("idSet") REFERENCES "Set" ("idSet");

ALTER TABLE "Printings" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "PurchaseURLs" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Ruling" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Subtypes" ADD FOREIGN KEY ("idSubtype") REFERENCES "Subtype" ("idSubtype");

ALTER TABLE "Subtypes" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Supertypes" ADD FOREIGN KEY ("idSupertype") REFERENCES "Supertype" ("idSupertype");

ALTER TABLE "Supertypes" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Types" ADD FOREIGN KEY ("idType") REFERENCES "Type" ("idType");

ALTER TABLE "Types" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");
