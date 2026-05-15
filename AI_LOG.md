# AI Assistance Log — CS665 Project 3

This file documents all instances where Generative AI was used as an assistant during this project, per course policy.

---

## Entry 1

**Tool:** Claude (Anthropic — claude.ai)

**Prompt:**
> I submitted these 3 SQL files in project 2 as DDL, DML and DQL. Now my professor asked me to continue with that project. This time it's a continuation of project 2. I have attached the additional info requirement requested by my professor. Help me proceed and work on project 3 from scratch. I have my Git and VS Code connected and I created a repository.

**AI Output Summary:**
Claude generated the full project scaffold including:
- Flask app factory pattern (`app.py`) with environment variable configuration
- SQLAlchemy models (`models.py`) for Author, Book, Member, Loan — matching the existing MySQL schema
- Four route blueprints with full CRUD: authors, books, members, loans
- Transaction logic in `loans.py` for book checkout (availability check + loan creation) and return (sets return_date + computes loan_duration_days)
- Server-side validation in all routes (required fields, numeric ranges, email format, date ordering, unique email enforcement)
- Jinja2 templates using Bootstrap 5 for all pages (dashboard, index/form/show for each entity)
- A dashboard with aggregate SQL queries (COUNT, AVG, top borrowed books, loans by month)
- `NORMALIZATION.md` documenting functional dependencies and 3NF analysis
- `README.md`, `requirements.txt`, `.gitignore`, `.env.example`

**My Modifications and Verification:**
- Verified that all SQLAlchemy model column names and types exactly match the existing Project 2 MySQL schema (`2_create_tables.sql`), including `loan_duration_days` which was added in `3_populate_and_modify.sql`
- Confirmed the `available_copies` property logic accounts for the `total_copies` column in `books`
- Verified the transaction pattern in `loans.py` uses `db.session.rollback()` on exception, which is the correct Flask-SQLAlchemy pattern
- Reviewed the normalization analysis for accuracy — confirmed the schema is already in 3NF and the `loan_duration_days` retained-derivation justification is sound
- Adjusted template paths to match the actual folder structure
- Tested that the `return_date is none` Jinja2 filter syntax correctly shows the Return button only for active loans

---

*All AI-generated code was reviewed, understood, and verified against the project requirements and existing database schema before inclusion.*
