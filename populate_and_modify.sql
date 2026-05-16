INSERT INTO authors (first_name, last_name, nationality, birth_year) VALUES
('Varun', 'Nomulla', 'indian', 2004),
('J.K.','Rowling',  'British',  1965),
('Toni', 'Morrison', 'American', 1931),
('Mark',    'Twain',    'American', 1835),
('Alka',    'Christie',    'African', 1835);

SELECT 'Output for Populate Authors' AS Message;
SELECT *FROM authors;

INSERT INTO members (first_name, last_name, email, phone, join_date ) VALUES

    ('Alison',  'Johnson',  'alice@email.com',  '316-555-0101', '2024-01-15'),
    ('Bob',    'Martinez', 'bob@email.com',    '316-555-0102', '2024-02-20'),
    ('Carol',  'Smith',    'carol@email.com',  '316-555-0103', '2024-03-05'),
    ('David',  'Lee',      'david@email.com',  '316-555-0104', '2024-04-10'),
    ('Eva',    'Brown',    'eva@email.com',    '316-555-0105', '2024-05-22'),
    ('Ram',    'Brown',    'ramaa@email.com',    '316-555-0105', '2024-05-22');

SELECT 'Output for Populate Members' AS Message;
SELECT *FROM members;

INSERT INTO books (title, genre, published_year, total_copies, author_id) VALUES
    ('1984',                             'Dystopian', 1949, 3, 1),
    ('Animal Farm',                      'Satire',    1945, 2, 1),
    ('Harry Potter and the Sorcerers Stone', 'Fantasy', 1997, 5, 2),
    ('The Shining',                      'Horror',    1977, 2, 3),
    ('Murder on the Orient Express',     'Mystery',   1934, 3, 4),
    ('Beloved',                          'Fiction',   1987, 2, 5);

SELECT 'Output for Populate Members' AS Message;
SELECT *FROM books;

INSERT INTO loans (member_id, book_id, loan_date, due_date, return_date) VALUES
(1,1, '2026-01-01', '2026-01-20', '2026-01-18'),
(1,1, '2026-02-01', '2026-02-20', '2026-02-18'),
(1,1, '2026-02-18', '2026-02-28', NULL),
(1,1, '2026-01-01', '2026-01-20', '2026-01-18'),
(1,1, '2026-01-01', '2026-01-20', '2026-01-18'),
(1,1, '2026-01-01', '2026-01-20', NULL);

SELECT 'Output for Populate Members' AS Message;
SELECT *FROM loans;

UPDATE loans
SET due_date = '2026-04-01', updated_At = CURRENT_TIMESTAMP WHERE loan_id= 2;
SELECT 'Output for Question 3.1:' AS Message;
SELECT 'Output for Question 3.1:' AS Message;


update members
SET email = 'alice.new@email.com', updated_At = CURRENT_TIMESTAMP WHERE member_id= 1;
SELECT *FROM members WHERE member_id = 1;

DELETE FROM authors WHERE author_id = 6;
SELECT 'Output for Question 3.3:' AS Message;
SELECT * FROM authors;

ALTER TABLE loans
ADD COLUMN loan_duration_days INT;

SELECT 'OUTPUT for 3.4' AS MESSAGE;
SELECT * FROM loans;

UPDATE loans
SET loan_duration_days= DATEDIFF(
    COALESCE(return_date, CURDATE()),
    loan_date
);

SELECT 'OUTPUT for 3.5' AS MESSAGE;
SELECT loan_id, loan_date, due_date, return_date, loan_duration_days
FROM loans;

ALTER TABLE members ADD CONSTRAINT unique_member_email UNIQUE(email);

SELECT 'Output for 3.6' AS Message;
SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE FROM information_schema.TABLE_CONSTRAINTS 
WHERE TABLE_NAME = 'members' AND TABLE_SCHEMA = DATABASE();