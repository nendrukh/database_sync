CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    position VARCHAR(255)
);

INSERT INTO employees (first_name, last_name, position) VALUES
('Robert', 'Martin', 'Dev'),
('Mark', 'Zuckerberg', 'Qa'),
('Craig', 'Federighi', 'DevRel');