import os
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import User, Category, Income, Expense, Budget
from app.forms import RegistrationForm, LoginForm


auth_bp = Blueprint("auth", __name__, template_folder="../templates", url_prefix="/auth")


def create_default_categories(user):
    default_categories = [
        ("Housing", "expense"),
        ("Food", "expense"),
        ("Transportation", "expense"),
        ("Utilities", "expense"),
        ("Insurance", "expense"),
        ("Entertainment", "expense"),
        ("Health", "expense"),
        ("Savings", "expense"),
        ("Salary", "income"),
        ("Freelance", "income"),
        ("Investment", "income"),
    ]

    for name, kind in default_categories:
        if not Category.query.filter_by(user_id=user.id, name=name, kind=kind).first():
            db.session.add(Category(name=name, kind=kind, user_id=user.id))
    db.session.commit()


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("This email is already registered.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(full_name=form.full_name.data.strip(), email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        create_default_categories(user)
        login_user(user)
        flash("Registration successful! Welcome.", "success")
        return redirect(url_for("dashboard.index"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard.index"))

        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
