-- Create user table
CREATE TABLE web_user (
    web_user_id SERIAL    NOT NULL,
    fullname   VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (web_user_id)
);