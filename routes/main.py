from flask import Blueprint, render_template
from sqlalchemy import func
from app import db
from models import Author, Book, Member, Loan

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def dashboard():
    total_books = db.session.query(func.count(Book.book_id)).scalar()
    total_authors = db.session.query(func.count(Author.author_id)).scalar()
    total_members = db.session.query(func.count(Member.member_id)).scalar()
    total_loans = db.session.query(func.count(Loan.loan_id)).scalar()
    active_loans = db.session.query(func.count(Loan.loan_id)).filter(Loan.return_date == None).scalar()
    avg_loan_duration = db.session.query(func.round(func.avg(Loan.loan_duration_days), 2)).filter(Loan.return_date != None, Loan.loan_duration_days != None).scalar()
    top_books = db.session.query(Book.title, func.count(Loan.loan_id).label("times_borrowed")).join(Loan, Book.book_id == Loan.book_id).group_by(Book.book_id, Book.title).order_by(func.count(Loan.loan_id).desc()).limit(5).all()
    loans_by_month = db.session.query(func.extract("year", Loan.loan_date).label("year"), func.extract("month", Loan.loan_date).label("month"), func.count(Loan.loan_id).label("total")).group_by("year", "month").order_by("year", "month").all()
    active_members = db.session.query(Member).join(Loan, Member.member_id == Loan.member_id).filter(Loan.return_date == None).distinct().count()
    never_borrowed = db.session.query(Book).filter(~Book.loans.any()).count()
    return render_template("dashboard.html", total_books=total_books, total_authors=total_authors, total_members=total_members, total_loans=total_loans, active_loans=active_loans, avg_loan_duration=avg_loan_duration or 0, top_books=top_books, loans_by_month=loans_by_month, active_members=active_members, never_borrowed=never_borrowed)
