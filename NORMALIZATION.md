# Normalization Report — Library Management System

## Original Schema (from Project 2)

```
authors(author_id, first_name, last_name, nationality, birth_year, created_at, updated_at)
members(member_id, first_name, last_name, email, phone, join_date, created_at, updated_at)
books(book_id, title, genre, published_year, total_copies, author_id, created_at, updated_at)
loans(loan_id, member_id, book_id, loan_date, due_date, return_date, loan_duration_days, created_at, updated_at)
```

---

## 1. Original Functional Dependencies

### authors
- `author_id → first_name, last_name, nationality, birth_year`
- Primary key: `author_id`

### members
- `member_id → first_name, last_name, email, phone, join_date`
- `email → member_id` (email is unique — a candidate key)
- Primary key: `member_id`

### books
- `book_id → title, genre, published_year, total_copies, author_id`
- `author_id → (nationality, birth_year)` — but those attributes live in the `authors` table, not `books`
- Primary key: `book_id`

### loans
- `loan_id → member_id, book_id, loan_date, due_date, return_date`
- `loan_id → loan_duration_days` (derived from `return_date - loan_date`)
- Primary key: `loan_id`

---

## 2. First Normal Form (1NF) Check

**Rule:** Every column must be atomic (no repeating groups or multi-valued attributes).

| Table   | 1NF? | Notes |
|---------|------|-------|
| authors | ✅   | All columns are atomic |
| members | ✅   | All columns are atomic |
| books   | ✅   | All columns are atomic |
| loans   | ✅   | All columns are atomic |

**Result:** All four tables satisfy 1NF.

---

## 3. Second Normal Form (2NF) Check

**Rule:** Must be in 1NF and every non-key attribute must depend on the *entire* primary key (no partial dependencies). Partial dependencies only apply to composite primary keys.

All four tables use single-column surrogate integer primary keys (`author_id`, `member_id`, `book_id`, `loan_id`). A partial dependency cannot exist with a single-column primary key.

| Table   | 2NF? | Notes |
|---------|------|-------|
| authors | ✅   | Single PK, no partial deps |
| members | ✅   | Single PK, no partial deps |
| books   | ✅   | Single PK, no partial deps |
| loans   | ✅   | Single PK, no partial deps |

**Result:** All four tables satisfy 2NF.

---

## 4. Third Normal Form (3NF) Check

**Rule:** Must be in 2NF and no non-key attribute may transitively depend on the primary key through another non-key attribute.

### Potential Transitive Dependencies Investigated

**books table:**  
`book_id → author_id → (first_name, last_name, nationality, birth_year)`  
However, the author's details are **not stored in `books`**. The `books` table only stores the foreign key `author_id`. The author attributes live exclusively in `authors`. ✅ No transitive dependency violation.

**loans table — `loan_duration_days`:**  
`loan_id → loan_date, return_date → loan_duration_days`  
`loan_duration_days` is derivable from `return_date - loan_date`. This is a **computed/derived attribute**, which is technically a functional dependency on non-key columns. Strictly speaking, this violates 3NF purity.

> **Decision:** We retain `loan_duration_days` as a stored column intentionally for **performance and query simplicity**, since recomputing it on every query is wasteful. This is a standard, accepted denormalization tradeoff. The column is always kept in sync via application logic (set when a book is returned) and was part of the original schema requirements (Project 2, Question 3.5).

**members table — `email` as candidate key:**  
`email → member_id` (email uniquely identifies a member). Since `email` itself is a key (a candidate key), this is not a 3NF violation.

| Table   | 3NF? | Notes |
|---------|------|-------|
| authors | ✅   | No transitive dependencies |
| members | ✅   | `email` is a candidate key, not a transitive dep |
| books   | ✅   | Author details not stored here, only FK |
| loans   | ⚠️ → ✅ | `loan_duration_days` is a derived value; retained intentionally with controlled redundancy |

**Result:** All tables satisfy 3NF. The one borderline case (`loan_duration_days`) is a justified, controlled denormalization.

---

## 5. Anomaly Identification

### Update Anomalies
- **authors/books relationship:** Because author details are stored once in `authors` and referenced by FK in `books`, updating an author's name only requires changing one row. No update anomaly. ✅
- **loan_duration_days:** If `return_date` were manually changed without recalculating `loan_duration_days`, the derived column could become stale. The application prevents this by only setting `return_date` through the return workflow, which also computes the duration. ✅ (mitigated by application logic)

### Insertion Anomalies
- You cannot add a book without a valid `author_id` (or NULL if no author). No author details need to be duplicated.
- You cannot add a loan without valid `member_id` and `book_id` foreign keys, enforcing referential integrity. ✅

### Deletion Anomalies
- Deleting an author who has books is prevented at the application level (FK constraint would cascade or block). The app explicitly checks and blocks deletion of authors with existing books. ✅
- Deleting a member with active loans is blocked by the application. ✅

---

## 6. Final Relational Schema (3NF)

```
authors(
    author_id   INT PK AUTO_INCREMENT,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    nationality VARCHAR(50),
    birth_year  INT,
    created_at  TIMESTAMP,
    updated_at  TIMESTAMP
)

members(
    member_id  INT PK AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    email      VARCHAR(50) NOT NULL UNIQUE,   -- candidate key
    phone      VARCHAR(100),
    join_date  DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)

books(
    book_id        INT PK AUTO_INCREMENT,
    title          VARCHAR(150) NOT NULL,
    genre          VARCHAR(50),
    published_year INT,
    total_copies   INT DEFAULT 1,
    author_id      INT FK → authors(author_id),
    created_at     TIMESTAMP,
    updated_at     TIMESTAMP
)

loans(
    loan_id           INT PK AUTO_INCREMENT,
    member_id         INT FK → members(member_id) NOT NULL,
    book_id           INT FK → books(book_id) NOT NULL,
    loan_date         DATE NOT NULL,
    due_date          DATE NOT NULL,
    return_date       DATE,
    loan_duration_days INT,    -- controlled denormalization: derived from return_date - loan_date
    created_at        TIMESTAMP,
    updated_at        TIMESTAMP
)
```

### Relationships
- `authors` ← `books`: One-to-Many (one author writes many books)
- `members` ← `loans`: One-to-Many (one member has many loans)
- `books` ← `loans`: One-to-Many (one book has many loan records)

**No decomposition was required.** The original schema from Project 2 already conforms to 3rd Normal Form.
