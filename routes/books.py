from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app import db
from extensions import db
from models import Book, Author

books_bp = Blueprint("books", __name__)

@books_bp.route("/")
def index():
    books = Book.query.order_by(Book.title).all()
    return render_template("books/index.html", books=books)

@books_bp.route("/new", methods=["GET", "POST"])
def new():
    authors = Author.query.order_by(Author.last_name).all()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        genre = request.form.get("genre", "").strip()
        published_year = request.form.get("published_year", "").strip()
        total_copies = request.form.get("total_copies", "1").strip()
        author_id = request.form.get("author_id", "").strip()
        errors = []
        if not title:
            errors.append("Title is required.")
        if published_year:
            try:
                published_year = int(published_year)
            except ValueError:
                errors.append("Published year must be a valid number.")
        else:
            published_year = None
        try:
            total_copies = int(total_copies)
            if total_copies < 1:
                errors.append("Total copies must be at least 1.")
        except ValueError:
            errors.append("Total copies must be a valid number.")
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("books/form.html", action="Create", book=None, authors=authors, form_data=request.form)
        book = Book(title=title, genre=genre or None, published_year=published_year, total_copies=total_copies, author_id=int(author_id) if author_id else None)
        db.session.add(book)
        db.session.commit()
        flash(f"Book '{book.title}' added!", "success")
        return redirect(url_for("books.index"))
    return render_template("books/form.html", action="Create", book=None, authors=authors, form_data={})

@books_bp.route("/<int:book_id>")
def show(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("books/show.html", book=book)

@books_bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    authors = Author.query.order_by(Author.last_name).all()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        genre = request.form.get("genre", "").strip()
        published_year = request.form.get("published_year", "").strip()
        total_copies = request.form.get("total_copies", "1").strip()
        author_id = request.form.get("author_id", "").strip()
        errors = []
        if not title:
            errors.append("Title is required.")
        try:
            total_copies = int(total_copies)
        except ValueError:
            errors.append("Total copies must be a number.")
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("books/form.html", action="Update", book=book, authors=authors, form_data=request.form)
        book.title = title
        book.genre = genre or None
        book.published_year = int(published_year) if published_year else None
        book.total_copies = total_copies
        book.author_id = int(author_id) if author_id else None
        db.session.commit()
        flash(f"Book '{book.title}' updated!", "success")
        return redirect(url_for("books.index"))
    return render_template("books/form.html", action="Update", book=book, authors=authors, form_data=book)

@books_bp.route("/<int:book_id>/delete", methods=["POST"])
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    if book.loans:
        flash("Cannot delete book — it has loan records.", "danger")
        return redirect(url_for("books.index"))
    title = book.title
    db.session.delete(book)
    db.session.commit()
    flash(f"Book '{title}' deleted.", "warning")
    return redirect(url_for("books.index"))
