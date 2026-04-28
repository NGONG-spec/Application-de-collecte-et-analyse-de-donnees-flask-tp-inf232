-- Création de la table Etudiant (Infos fixes)
CREATE TABLE IF NOT EXISTS Etudiant (
    id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    sexe TEXT,
    date_naissance DATE,
    telephone TEXT
);

-- Création de la table Consultation (Infos variables)
-- Liée à l'étudiant par une clé étrangère
CREATE TABLE IF NOT EXISTS Consultation (
    id_consultation INTEGER PRIMARY KEY AUTOINCREMENT,
    date_visite TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    taille REAL,
    poids REAL,
    imc REAL,
    tension TEXT,
    diagnostic_auto TEXT,
    fk_etudiant_id INTEGER,
    FOREIGN KEY (fk_etudiant_id) REFERENCES Etudiant(id_etudiant)
);