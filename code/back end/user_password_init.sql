# 存储用户信息

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    student_id INT NOT NULL,
    CONSTRAINT unique_username UNIQUE (username),
    CONSTRAINT unique_student_id UNIQUE (student_id)
);

# 创建root用户
INSERT INTO users (username, password, student_id) VALUES ('root', 'root', 0);

# 显示所有用户
SELECT * FROM users;