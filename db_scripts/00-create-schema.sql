/*
    Create table:
        users
        items
        items_users
        comments
*/

SET autocommit = 0;
START TRANSACTION;

CREATE TABLE IF NOT EXISTS users (
    id              INT NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100) NOT NULL,
    avatar          VARCHAR(200),
    dollars         INT(11) NOT NULL DEFAULT '100',
    created_date    DATETIME NOT NULL,
    
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS items (
    id              INT NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100),
    description     TEXT,
    price           INT,
    
    created_date    DATETIME NOT NULL,

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
