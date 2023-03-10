-- SQLite

-- description de la table user de notre base de données
DROP TABLE user; --supprime la db pour remettre à zéro lors de nos tests

-- création des colonnes de la table user
CREATE TABLE IF NOT EXISTS user ( 
	user_id INTEGER PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	password VARCHAR(50),
	status VARCHAR(50),
	date VARCHAR(50),
	medical_files VARCHAR(250)
);
-- insertion des valeurs de chaque colonne d'un user
INSERT INTO user (username,first_name, last_name, password, status, date, medical_files) 
VALUES('Sudo','sudo', 'sudo','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','sudo','2022-01-25', NULL),
('Admin1','admin', 'admin','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','admin','2022-01-25',NULL),
('Admin2','admin', 'admin','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','admin','2023-01-25',NULL),
('Admin3','admin', 'admin','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','admin','2023-01-25',NULL),
('Admin4','admin', 'admin','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','admin','2023-01-25',NULL),
('CCOUSIN','Clemence', 'COUSIN','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'patient','2023-01-25', 'medical file'),
('MARRAR','Mordjane', 'ARRAR','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'patient','2023-01-25', 'medical file'),
('Dr','John', 'SMITH','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'doctor','2023-01-25','patient list');

---------------- POUR TESTER / MDP POUR CHAQUE USER : test -----------------------

SELECT * FROM user; 


-- afficher la table user

-- Requetes test

--DELETE FROM user WHERE pseudo is 'Admin';
--UPDATE user SET first_name = 'Michel' WHERE username = 'Clem';
--SELECT * FROM user WHERE username = 'Clem'; 

-- SELECT status FROM user WHERE username = 'Admin' AND password = 'test';
-- SELECT password from user;
-- SELECT status from user where status = 'dzilz';