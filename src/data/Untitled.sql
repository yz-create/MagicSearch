CREATE TABLE "Card" (
  "idCard" int PRIMARY KEY NOT NULL,
  "convertedManaCost" float NOT NULL,
  "layout" int NOT NULL,
  "legalities" int NOT NULL,
  "manaValue" float NOT NULL,
  "name" str NOT NULL,
  "type" str NOT NULL,
  "text_to_embed" str NOT NULL,
  "embed" float[] NOT NULL,
  "asciiName" str,
  "defense" int,
  "edhrecRank" int,
  "edhrecSaltiness" float,
  "faceManaValue" float,
  "faceName" str,
  "firstPrinting" int,
  "hand" int,
  "hasAlternativeDeckLimit" bool,
  "isFunny" bool,
  "isReserved" bool,
  "life" int,
  "loyalty" str,
  "manaCost" str,
  "power" str,
  "side" str,
  "text" str,
  "toughness" str
);

CREATE TABLE "User" (
  "idUser" int PRIMARY KEY NOT NULL,
  "username" string NOT NULL,
  "password" string NOT NULL,
  "isAdmin" bool NOT NULL
);

CREATE TABLE "Favourite" (
  "idUser" int NOT NULL,
  "idCard" int NOT NULL,
  PRIMARY KEY ("idUser", "idCard")
);

CREATE TABLE "Color" (
  "idColor" int PRIMARY KEY NOT NULL,
  "colorName" str NOT NULL
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
  "language" str NOT NULL,
  "name" str NOT NULL,
  "faceName" str,
  "flavorText" str,
  "text" str,
  "type" str
);

CREATE TABLE "Keyword" (
  "idKeyword" int PRIMARY KEY NOT NULL,
  "name" str NOT NULL
);

CREATE TABLE "Keywords" (
  "idCard" int NOT NULL,
  "idKeyword" int NOT NULL,
  PRIMARY KEY ("idCard", "idKeyword")
);

CREATE TABLE "Set" (
  "idSet" int PRIMARY KEY NOT NULL,
  "name" str NOT NULL
);

CREATE TABLE "Layout" (
  "idLayout" int PRIMARY KEY NOT NULL,
  "name" str NOT NULL
);

CREATE TABLE "Leadership" (
  "idLeadership" int PRIMARY KEY NOT NULL,
  "brawl" bool NOT NULL,
  "commander" bool NOT NULL,
  "oathbreaker" bool NOT NULL
);

CREATE TABLE "LeadershipSkills" (
  "idLeadership" int NOT NULL,
  "idCard" int NOT NULL,
  PRIMARY KEY ("idLeadership", "idCard")
);

CREATE TABLE "Legality" (
  "idLegality" int PRIMARY KEY NOT NULL,
  "commander" int,
  "oathbreker" int,
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
  "alchemy" int,
  "oldschool" int
);

CREATE TABLE "LegalityType" (
  "idLegalityType" int PRIMARY KEY NOT NULL,
  "type" str NOT NULL
);

CREATE TABLE "Printings" (
  "idSet" int NOT NULL,
  "idCard" int NOT NULL,
  PRIMARY KEY ("idSet", "idCard")
);

CREATE TABLE "PurchaseURLs" (
  "idPurchaseURLs" int PRIMARY KEY NOT NULL,
  "idCard" int NOT NULL,
  "tcgplayer" str,
  "cardKingdom" str,
  "cardmarket" str,
  "cardKingdomFoil" str,
  "cardKingdromEtched" str,
  "tcgplayerEteched" str
);

CREATE TABLE "Ruling" (
  "idRuling" int PRIMARY KEY NOT NULL,
  "date" date NOT NULL,
  "text" str NOT NULL,
  "idCard" int NOT NULL
);

CREATE TABLE "Subtype" (
  "idSubtype" int PRIMARY KEY,
  "name" str
);

CREATE TABLE "Subtypes" (
  "idSubtype" int NOT NULL,
  "idCard" int NOT NULL,
  PRIMARY KEY ("idSubtype", "idCard")
);

CREATE TABLE "Supertype" (
  "idSupertype" int PRIMARY KEY,
  "name" str
);

CREATE TABLE "Supertypes" (
  "idSupertype" int NOT NULL,
  "idCard" int NOT NULL,
  PRIMARY KEY ("idSupertype", "idCard")
);

CREATE TABLE "Type" (
  "idType" int PRIMARY KEY,
  "name" str
);

CREATE TABLE "Types" (
  "idType" int NOT NULL,
  "idCard" int NOT NULL,
  PRIMARY KEY ("idType", "idCard")
);

ALTER TABLE "Card" ADD FOREIGN KEY ("layout") REFERENCES "Layout" ("idLayout");

ALTER TABLE "Card" ADD FOREIGN KEY ("legalities") REFERENCES "Legality" ("idLegality");

ALTER TABLE "Card" ADD FOREIGN KEY ("firstPrinting") REFERENCES "Set" ("idSet");

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

ALTER TABLE "LeadershipSkills" ADD FOREIGN KEY ("idLeadership") REFERENCES "Leadership" ("idLeadership");

ALTER TABLE "LeadershipSkills" ADD FOREIGN KEY ("idCard") REFERENCES "Card" ("idCard");

ALTER TABLE "Legality" ADD FOREIGN KEY ("commander") REFERENCES "LegalityType" ("idLegalityType");

ALTER TABLE "Legality" ADD FOREIGN KEY ("oathbreker") REFERENCES "LegalityType" ("idLegalityType");

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
