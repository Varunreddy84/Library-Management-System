from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date, timedelta
# from app import db
from extensions import db
from models import Loan, Book, Member

loans_bp = Blueprint("loans", __name__)


@loans_bp.route("/")
def index():
    loans = Loan.query.order_by(Loan.loan_date.desc()).all()
    return render_template("loans/index.html", loans=loans)


@loans_bp.route("/new", methods=["GET", "POST"])
def new():
    """
    TRANSACTION LOGIC:
    Checking out a book involves two steps that must both succeed:
      1. Verify the book has available copies
      2. Create the loan record
    If either step fails, the whole operation rolls back.
    """
    members = Member.query.order_by(Member.last_name).all()
    books = Book.query.order_by(Book.title).all()

    if request.method == "POST":
        member_id = request.form.get("member_id", "").strip()
        book_id = request.form.get("book_id", "").strip()
        loan_date = request.form.get("loan_date", "").strip()
        due_date = request.form.get("due_date", "").strip()

        errors = []
        if not member_id:
            errors.append("Please select a member.")
        if not book_id:
            errors.append("Please select a book.")

        parsed_loan_date = None
        parsed_due_date = None

        if loan_date:
            try:
                parsed_loan_date = date.fromisoformat(loan_date)
            except ValueError:
                errors.append("Loan date must be a valid date.")
        else:
            parsed_loan_date = date.today()

        if due_date:
            try:
                parsed_due_date = date.fromisoformat(due_date)
            except ValueError:
                errors.append("Due date must be a valid date.")
        else:
            parsed_due_date = date.today() + timedelta(days=14)

        if parsed_loan_date and parsed_due_date and parsed_due_date <= parsed_loan_date:
            errors.append("Due date must be after the loan date.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("loans/form.html", members=members, books=books,
                                   form_data=request.form)

        # --- TRANSACTION: check availability then create loan ---
        try:
            book = Book.query.get(int(book_id))
            if not book:
                flash("Selected book not found.", "danger")
                return render_template("loans/form.html", members=members, books=books,
                                       form_data=request.form)

            # Step 1: Check availability
            if book.available_copies < 1:
                flash(f"No copies of '{book.title}' are currently available.", "danger")
                return render_template("loans/form.html", members=members, books=books,
                                       form_data=request.form)

            # Step 2: Create the loan record
            loan = Loan(
                member_id=int(member_id),
                book_id=int(book_id),
                loan_date=parsed_loan_date,
                due_date=parsed_due_date,
                return_date=None
            )
            db.session.add(loan)
            db.session.commit()  # Both steps committed together

            flash(f"Book '{book.title}' checked out successfully! Due: {parsed_due_date}", "success")
            return redirect(url_for("loans.index"))

        except Exception as e:
            db.session.rollback()
            flash(f"Checkout failed — transaction rolled back. Error: {str(e)}", "danger")
            return render_template("loans/form.html", members=members, books=books,
                                   form_data=request.form)

    default_data = {
        "loan_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=14)).isoformat()
    }
    return render_template("loans/form.html", members=members, books=books, form_data=default_data)


@loans_bp.route("/<int:loan_id>")
def show(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    return render_template("loans/show.html", loan=loan)


@loans_bp.route("/<int:loan_id>/return", methods=["POST"])
def return_book(loan_id):
    """
    TRANSACTION LOGIC:
    Returning a book involves:
      1. Setting return_date on the loan
      2. Computing loan_duration_days
    Both happen atomically.
    """
    loan = Loan.query.get_or_404(loan_id)

    if loan.return_date is not None:
        flash("This book has already been returned.", "warning")
        return redirect(url_for("loans.index"))

    try:
        return_date = date.today()
        loan.return_date = return_date
        loan.loan_duration_days = (return_date - loan.loan_date).days
        db.session.commit()
        flash(f"Book returned successfully! Loan duration: {loan.loan_duration_days} days.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Return failed — transaction rolled back. Error: {str(e)}", "danger")

    return redirect(url_for("loans.index"))


@loans_bp.route("/<int:loan_id>/edit", methods=["GET", "POST"])
def edit(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    members = Member.query.order_by(Member.last_name).all()
    books = Book.query.order_by(Book.title).all()

    if request.method == "POST":
        due_date = request.form.get("due_date", "").strip()

        errors = []
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = date.fromisoformat(due_date)
                if parsed_due_date <= loan.loan_date:
                    errors.append("Due date must be after the loan date.")
            except ValueError:
                errors.append("Due date must be a valid date.")
        else:
            errors.append("Due date is required.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("loans/edit.html", loan=loan, members=members, books=books)

        loan.due_date = parsed_due_date
        db.session.commit()
        flash("Due date updated successfully!", "success")
        return redirect(url_for("loans.index"))

    return render_template("loans/edit.html", loan=loan, members=members, books=books)


@loans_bp.route("/<int:loan_id>/delete", methods=["POST"])
def delete(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    db.session.delete(loan)
    db.session.commit()
    flash("Loan record deleted.", "warning")
    return redirect(url_for("loans.index"))
