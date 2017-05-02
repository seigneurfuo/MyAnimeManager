CREATE_TABLE_ANIME = """
CREATE TABLE anime (
    animeId             VARCHAR        PRIMARY KEY
                                       NOT NULL,
    animeTitre          VARCHAR (100)  NOT NULL,
    animeAnnee          INT (4),
    animeStudio         VARCHAR (30),
    animeFansub         VARCHAR (30),
    animeEtatVisionnage INT,
    animeFavori         BOOLEAN (1),
    animeDateAjout      VARCHAR (50),
    animeNbVisionnage   INT,
    animeNotes          VARCHAR (2000) 
);
"""

CREATE_TABLE_PLANNING = """
CREATE TABLE planning (
    planningDate                  TEXT NOT NULL,
    planningIdentifiantJournalier TEXT,
    planningAnime                 TEXT,
    planningEpisode               TEXT
);
"""

CREATE_TABLE_INFORMATION = """
CREATE TABLE information (
    version TEXT UNIQUE
);
"""
