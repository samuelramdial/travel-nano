CREATE TABLE comment (
    comment_id SERIAL NOT NULL,
    comment VARCHAR(255) NULL,
    web_user_id INT NOT NULL,
    post_id INT NOT NULL,
    PRIMARY KEY (comment_id),
    CONSTRAINT fk_web_user
        FOREIGN KEY (web_user_id)
        REFERENCES web_user(web_user_id),
    CONSTRAINT fk_post
        FOREIGN KEY (post_id)
        REFERENCES post(post_id)
);