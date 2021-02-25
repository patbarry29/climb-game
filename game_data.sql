DROP TABLE IF EXISTS game_data;
CREATE TABLE game_data
(
    id_num INT AUTO_INCREMENT,
    name VARCHAR(15) DEFAULT 'idkwihtdt',
    score INT NOT NULL,
    difficulty VARCHAR(6) DEFAULT '' NOT NULL,
    PRIMARY KEY (id_num)
);