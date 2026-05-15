from app import db
from datetime import datetime, date


class Author(db.Model):
    __tablename__ = "authors"

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50))
    birth_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship: one author -> many books
    books = db.relationship("Book", backref="author", lazy=True)

    def __repr__(self):
        return f"<Author {self.first_name} {self.last_name}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Member(db.Model):
    __tablename__ = "members"

    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(100))
    join_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship: one member -> many loans
    loans = db.relationship("Loan", backref="member", lazy=True)

    def __repr__(self):
        return f"<Member {self.first_name} {self.last_name}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(50))
    published_year = db.Column(db.Integer)
    total_copies = db.Column(db.Integer, default=1)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship: one book -> many loans
    loans = db.relationship("Loan", backref="book", lazy=True)

    def __repr__(self):
        return f"<Book {self.title}>"

    @property
    def active_loans_count(self):
        return sum(1 for loan in self.loans if loan.return_date is None)

    @property
    def available_copies(self):
        return max(0, self.total_copies - self.active_loans_count)


class Loan(db.Model):
    __tablename__ = "loans"

    loan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.member_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    loan_duration_days = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Loan {self.loan_id}>"

    @property
    def is_overdue(self):
        if self.return_date is None and self.due_date < date.today():
            return True
        return False

    @property
    def status(self):
        if self.return_date:
            return "Returned"
        elif self.is_overdue:
            return "Overdue"
        else:
            return "Active"
