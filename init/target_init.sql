CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

INSERT INTO users (first_name, last_name) VALUES
('John', 'Doe'),
('John', 'Cena'),
('Martin', 'Scorsese');