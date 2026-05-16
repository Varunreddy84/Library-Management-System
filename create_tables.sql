CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS authors;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    nationality VARCHAR(50),
    birth_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

SELECT 'OUTPUT for question 2.1 authors table created' AS Message;

CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(100),
    join_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

SELECT 'OUTPUT for question 2.1 members table created' AS Message;

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    genre VARCHAR(50),
    published_year INT,
    total_copies INT DEFAULT 1,
    author_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_books_author
        FOREIGN KEY (author_id) REFERENCES authors(author_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

SELECT 'OUTPUT for question 2.1 books table created' AS Message;

CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    book_id INT,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_loans_member
        FOREIGN KEY (member_id) REFERENCES members(member_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_loans_book
        FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

SELECT 'OUTPUT for question 2.1 loans table created' AS Message;

SELECT 'OUTPUT for question 2.1' AS Message;

SELECT table_name
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY table_name;