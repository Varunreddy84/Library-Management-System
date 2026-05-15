from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from datetime import date
from app import db
from models import Member

members_bp = Blueprint("members", __name__)

@members_bp.route("/")
def index():
    members = Member.query.order_by(Member.last_name).all()
    return render_template("members/index.html", members=members)

@members_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        join_date = request.form.get("join_date", "").strip()
        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if not email or "@" not in email:
            errors.append("A valid email is required.")
        parsed_date = date.fromisoformat(join_date) if join_date else date.today()
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("members/form.html", action="Create", member=None, form_data=request.form)
        member = Member(first_name=first_name, last_name=last_name, email=email, phone=phone or None, join_date=parsed_date)
        try:
            db.session.add(member)
            db.session.commit()
            flash(f"Member '{member.full_name}' added!", "success")
            return redirect(url_for("members.index"))
        except IntegrityError:
            db.session.rollback()
            flash("That email is already registered.", "danger")
            return render_template("members/form.html", action="Create", member=None, form_data=request.form)
    return render_template("members/form.html", action="Create", member=None, form_data={})

@members_bp.route("/<int:member_id>")
def show(member_id):
    member = Member.query.get_or_404(member_id)
    return render_template("members/show.html", member=member)

@members_bp.route("/<int:member_id>/edit", methods=["GET", "POST"])
def edit(member_id):
    member = Member.query.get_or_404(member_id)
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if not email or "@" not in email:
            errors.append("A valid email is required.")
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("members/form.html", action="Update", member=member, form_data=request.form)
        member.first_name = first_name
        member.last_name = last_name
        member.email = email
        member.phone = phone or None
        try:
            db.session.commit()
            flash(f"Member '{member.full_name}' updated!", "success")
            return redirect(url_for("members.index"))
        except IntegrityError:
            db.session.rollback()
            flash("That email is already in use.", "danger")
            return render_template("members/form.html", action="Update", member=member, form_data=request.form)
    return render_template("members/form.html", action="Update", member=member, form_data=member)

@members_bp.route("/<int:member_id>/delete", methods=["POST"])
def delete(member_id):
    member = Member.query.get_or_404(member_id)
    if any(l.return_date is None for l in member.loans):
        flash("Cannot delete member — they have active loans.", "danger")
        return redirect(url_for("members.index"))
    name = member.full_name
    db.session.delete(member)
    db.session.commit()
    flash(f"Member '{name}' deleted.", "warning")
    return redirect(url_for("members.index"))
