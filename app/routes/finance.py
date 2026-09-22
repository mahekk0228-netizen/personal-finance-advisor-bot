from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import IncomeForm, ExpenseForm, BudgetForm
from app.models import Category, Income, Expense, Budget

finance_bp = Blueprint("finance", __name__, template_folder="../templates")


@finance_bp.route("/finance")
@login_required
def overview():
    total_income = db.session.query(db.func.coalesce(db.func.sum(Income.amount), 0)).filter_by(user_id=current_user.id).scalar() or 0
    total_expense = db.session.query(db.func.coalesce(db.func.sum(Expense.amount), 0)).filter_by(user_id=current_user.id).scalar() or 0
    budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.month.desc()).all()
    return render_template(
        "finance/overview.html",
        total_income=float(total_income),
        total_expense=float(total_expense),
        budgets=budgets,
    )


@finance_bp.route("/income", methods=["GET", "POST"])
@login_required
def income():
    form = IncomeForm()
    if form.validate_on_submit():
        income_entry = Income(
            source=form.source.data.strip(),
            amount=form.amount.data,
            received_date=form.received_date.data,
            notes=form.notes.data or "",
            user_id=current_user.id,
        )
        db.session.add(income_entry)
        db.session.commit()
        flash("Income added successfully.", "success")
        return redirect(url_for("finance.income"))
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.received_date.desc()).all()
    return render_template("finance/income.html", form=form, incomes=incomes)


@finance_bp.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    form = ExpenseForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id, kind="expense").all()]
    if form.validate_on_submit():
        expense_entry = Expense(
            title=form.title.data.strip(),
            amount=form.amount.data,
            expense_date=form.expense_date.data,
            notes=form.notes.data or "",
            category_id=form.category_id.data,
            user_id=current_user.id,
        )
        db.session.add(expense_entry)
        db.session.commit()
        flash("Expense saved successfully.", "success")
        return redirect(url_for("finance.expense"))
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.expense_date.desc()).all()
    return render_template("finance/expense.html", form=form, expenses=expenses)


@finance_bp.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    form = BudgetForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id, kind="expense").all()]
    if form.validate_on_submit():
        budget_entry = Budget(
            category_id=form.category_id.data,
            user_id=current_user.id,
            month=form.month.data,
            planned_amount=form.planned_amount.data,
        )
        db.session.add(budget_entry)
        db.session.commit()
        flash("Budget saved successfully.", "success")
        return redirect(url_for("finance.budget"))
    budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.month.desc()).all()
    return render_template("finance/budget.html", form=form, budgets=budgets)


@finance_bp.route("/analytics")
@login_required
def analytics():
    category_totals = db.session.query(Category.name, db.func.sum(Expense.amount).label("total")) \
        .join(Expense, Expense.category_id == Category.id) \
        .filter(Category.user_id == current_user.id) \
        .group_by(Category.name) \
        .all()
    return render_template("finance/analytics.html", category_totals=category_totals)
