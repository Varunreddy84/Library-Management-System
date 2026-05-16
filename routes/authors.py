from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app import db
from extensions import db
from models import Author

authors_bp = Blueprint("authors", __name__)

@authors_bp.route("/")
def index():
    authors = Author.query.order_by(Author.last_name).all()
    return render_template("authors/index.html", authors=authors)

@authors_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        nationality = request.form.get("nationality", "").strip()
        birth_year = request.form.get("birth_year", "").strip()
        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if birth_year:
            try:
                birth_year = int(birth_year)
                if birth_year < 0 or birth_year > 2025:
                    errors.append("Birth year must be between 0 and 2025.")
            except ValueError:
                errors.append("Birth year must be a valid number.")
        else:
            birth_year = None
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("authors/form.html", action="Create", author=None, form_data=request.form)
        author = Author(first_name=first_name, last_name=last_name, nationality=nationality or None, birth_year=birth_year)
        db.session.add(author)
        db.session.commit()
        flash(f"Author '{author.full_name}' created successfully!", "success")
        return redirect(url_for("authors.index"))
    return render_template("authors/form.html", action="Create", author=None, form_data={})

@authors_bp.route("/<int:author_id>")
def show(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template("authors/show.html", author=author)

@authors_bp.route("/<int:author_id>/edit", methods=["GET", "POST"])
def edit(author_id):
    author = Author.query.get_or_404(author_id)
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        nationality = request.form.get("nationality", "").strip()
        birth_year = request.form.get("birth_year", "").strip()
        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if birth_year:
            try:
                birth_year = int(birth_year)
            except ValueError:
                errors.append("Birth year must be a valid number.")
        else:
            birth_year = None
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("authors/form.html", action="Update", author=author, form_data=request.form)
        author.first_name = first_name
        author.last_name = last_name
        author.nationality = nationality or None
        author.birth_year = birth_year
        db.session.commit()
        flash(f"Author '{author.full_name}' updated!", "success")
        return redirect(url_for("authors.index"))
    return render_template("authors/form.html", action="Update", author=author, form_data=author)

@authors_bp.route("/<int:author_id>/delete", methods=["POST"])
def delete(author_id):
    author = Author.query.get_or_404(author_id)
    if author.books:
        flash("Cannot delete author — they have books in the catalog.", "danger")
        return redirect(url_for("authors.index"))
    name = author.full_name
    db.session.delete(author)
    db.session.commit()
    flash(f"Author '{name}' deleted.", "warning")
    return redirect(url_for("authors.index"))
