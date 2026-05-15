# Library Management System — CS665 Project 3

A full-stack web application for managing a library's books, authors, members, and loans. Built with Python/Flask, SQLAlchemy, MySQL, and Bootstrap 5.

---

## Project Description

This app allows library staff to:
- Manage **authors**, **books**, **members**, and **loans** with full CRUD
- **Checkout books** with transaction logic that verifies availability before creating a loan
- **Return books** atomically, computing loan duration in the same transaction
- View a **dashboard** with aggregate statistics (total books, active loans, most borrowed titles, loans by month, average loan duration)
- Enforce **data validation** server-side (required fields, valid years, unique emails, date ordering)

---

## Tech Stack

| Layer     | Technology                     |
|-----------|-------------------------------|
| Language  | Python 3.10+                  |
| Backend   | Flask 3.0                     |
| ORM       | Flask-SQLAlchemy               |
| Database  | MySQL (via PyMySQL driver)    |
| Frontend  | HTML5 + Bootstrap 5 + Jinja2  |
| Version Control | Git                     |

---

## Installation Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd library_app
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your MySQL credentials:
```
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=library_db
SECRET_KEY=any-random-string-here
```

---

## Database Setup

### 1. Create the database in MySQL
```sql
CREATE DATABASE library_db;
```

### 2. Run the schema and seed scripts from Project 2
```bash
mysql -u root -p library_db < 2_create_tables.sql
mysql -u root -p library_db < 3_populate_and_modify.sql
```

The SQLAlchemy models match the existing schema exactly — no schema changes required.

---

## Running the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## Features & Navigation

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/` | Aggregate stats, top books, loans by month |
| Authors | `/authors` | List, add, edit, delete authors |
| Books | `/books` | List, add, edit, delete books; availability tracking |
| Members | `/members` | List, add, edit, delete members |
| Loans | `/loans` | List all loans, checkout books, return books, edit due dates |

### Key Feature: Transactional Checkout
When checking out a book, the app:
1. Verifies the book has available copies
2. Creates the loan record

Both steps happen inside a single database transaction. If availability check fails, no loan record is created.

### Key Feature: Transactional Return
When returning a book, the app:
1. Sets `return_date` to today
2. Computes and stores `loan_duration_days`

Both updates commit together or roll back together.

---

## Project Structure

```
library_app/
├── app.py                  # App factory & Flask config
├── models.py               # SQLAlchemy models
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── NORMALIZATION.md        # 3NF audit report
├── AI_LOG.md               # AI assistance disclosure
├── routes/
│   ├── main.py             # Dashboard
│   ├── authors.py          # Author CRUD
│   ├── books.py            # Book CRUD
│   ├── members.py          # Member CRUD
│   └── loans.py            # Loan CRUD + transaction logic
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── authors/            # index, form, show
│   ├── books/              # index, form, show
│   ├── members/            # index, form, show
│   └── loans/              # index, form, edit, show
└── static/
    └── css/style.css
```
