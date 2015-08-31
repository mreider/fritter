/*
    Create table:
        users
        items
        items_users
        comments
*/

SET autocommit = 0;
START TRANSACTION;

CREATE TABLE IF NOT EXISTS surveys (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100),
    description     VARCHAR(300),
    dollars         INT NOT NULL,
    created_date    DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id              INT NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(50) NOT NULL,
    avatar          VARCHAR(200),
    created_date    DATETIME NOT NULL,
    
    PRIMARY KEY(id),
    UNIQUE KEY email_uniq (email)
);

CREATE TABLE IF NOT EXISTS user_wallet (
    user_id         INT NOT NULL,
    survey_id       INT NOT NULL,
    dollars         INT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE,

    PRIMARY KEY(user_id, thing_id)
);

CREATE TABLE IF NOT EXISTS items (
    id              INT NOT NULL AUTO_INCREMENT,
    survey_id       INT NONT NULL,
    name            VARCHAR(100),
    description     TEXT,
    price           INT,
    created_date    DATETIME NOT NULL,

    FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE,

    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS items_users (
    user_id         INT NOT NULL,
    thing_id        INT NOT NULL,
    dollars         INT NOT NULL,
    bought_date     DATETIME NOT NULL,
    
    created_date    DATETIME NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (thing_id) REFERENCES items(id) ON DELETE CASCADE,

    PRIMARY KEY(user_id, thing_id)
);

CREATE TABLE IF NOT EXISTS comments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    item_id         INT NOT NULL,
    comment         TEXT,
    posted          DATETIME NOT NULL,
    
    created_date    DATETIME NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

COMMIT;
