CREATE TABLE post (
    post_id SERIAL NOT NULL,
    post_title VARCHAR(255) NOT NULL,
    picture_file VARCHAR(255) NOT NULL,
    caption VARCHAR(2200) NULL,
    username VARCHAR(255) NOT NULL,
    post_month VARCHAR(10) NOT NULL,
    post_day VARCHAR(3) NOT NULL,
    post_year VARCHAR(5) NOT NULL,
    PRIMARY KEY (post_id)
);