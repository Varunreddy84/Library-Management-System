-- Retrieving: Genres that have more than 1 book in the catalog.
-- GROUP BY is needed to group all books by their genre so we can count how many books belong to each genre
-- here we use having instead of WHERE because we are filtering on an aggregate function COUNT(*)


SELECT 'Output for 4.1' AS Message;
SELECT genre, COUNT(*) AS total_books
FROM books
GROUP BY genre
HAVING COUNT(*)>1
ORDER BY total_books DESC;

-- Question 4.2 | MAX + JOIN + GROUP BY
--  The most recently published book for each author. GROUP BY is needed to group results per author so MAX

SELECT 'output for question 4.2' AS Message;
SELECT a.first_name, a.last_name, MAX(b.published_year) AS latest_published_year
FROM authors a
JOIN books b ON a.author_id = b.author_id
GROUP BY a.author_id, a.first_name, a.last_name
ORDER BY latest_published_year DESC;

-- Retrieving member names in uppercase and join year only; UPPER standardizes formatting, EXTRACT pulls the year from the date.

SELECT 'output for question 4.3' AS Message;
SELECT UPPER(CONCAT(first_name, ' ' , last_name)) AS full_name,
    EXTRACT( YEAR FROM join_date) AS join_year FROM members
ORDER BY join_year;

-- Retrieving the top 3 most borrowed books; JOIN links tables, COUNT tallies loans, GROUP BY groups per book, LIMIT cuts to top 3
SELECT 'output for  question 4.4' AS Message;
SELECT b.title, COUNT(l.loan_id) AS times_borrowed FROM books b 
JOIN loans l ON b.book_id = l.book_id
GROUP BY b.book_id, b.title
ORDER BY times_borrowed DESC
LIMIT 3;

-- REtrieving members with unreturned books; join link tables here and WHERE NOT keeps open loans only
-- DISTINCT removes the duplicate members 

SELECT 'output for question 4.5' AS Message;
SELECT DISTINCT m.member_id, m.first_name, m.last_name, m.email FROM members m
JOIN loans l ON m.member_id = l.member_id
WHERE NOT (l.return_date IS NOT NULL);

-- HERE REtrieving the totall loans per month; EXTRACT pulls year and month
-- count tallies loans
-- GROUP BY groups by timem period

SELECT 'output for question 4.6' AS Message;
SELECT EXTRACT(YEAR FROM loan_date) AS loan_year,
    EXTRACT(MONTH FROM loan_date) AS loan_month,
    COUNT(*) AS total_loans
FROM loans
GROUP BY loan_year, loan_month
ORDER BY loan_year, loan_month;
 
 -- retrieving books that were never borrowed
 -- WHERE builds a list of loaned book IDs and NOT IN excludes them

SELECT 'output for question  4.7' AS Message;
SELECT book_id, title, genre FROM books 
WHERE book_id NOT IN (
    SELECT DISTINCT book_id FROM loans
    WHERE book_id IS NOT NULL
);

-- retrieving active loans with member and book details
-- JOIN pulls the names
-- WHERE is used to filter the unreturned and ORDER BY surfaces most overdue first_name

SELECT 'output for question  4.8' AS Message;
SELECT CONCAT(m.first_name, '  ', m.last_name) AS member_name, b.title AS book_title, l.loan_date, l.due_date
FROM loans l
JOIN members m ON l.member_id = m.member_id
JOIN books b ON l.book_id = b.book_id
WHERE l.return_date IS NULL
ORDER BY l.due_date ASC;

-- retrieving the active loans with members and book details
-- JOIN helps to pull the names here and WHERE filters the unreturned.

SELECT 'output for question 4.9' AS Message;
SELECT ROUND(AVG(loan_duration_days),2)AS avg_loan_duration_days
FROM loans 
WHERE return_date IS NOT NULL
AND loan_duration_days IS NOT NULL;

