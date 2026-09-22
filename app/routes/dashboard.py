from collections import defaultdict
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import IncomeForm, ExpenseForm, BudgetForm
from app.models import Category, Income, Expense, Budget
from app.services.ai_service import generate_financial_advice


dashboard_bp = Blueprint("dashboard", __name__, template_folder="../templates")


def compute_summary(user_id):
    total_income = db.session.query(db.func.coalesce(db.func.sum(Income.amount), 0)).filter_by(user_id=user_id).scalar() or 0
    total_expense = db.session.query(db.func.coalesce(db.func.sum(Expense.amount), 0)).filter_by(user_id=user_id).scalar() or 0
    total_budget = db.session.query(db.func.coalesce(db.func.sum(Budget.planned_amount), 0)).filter_by(user_id=user_id).scalar() or 0
    net_savings = total_income - total_expense
    category_totals = db.session.query(Category.name, db.func.sum(Expense.amount).label("total")) \
        .join(Expense, Expense.category_id == Category.id) \
        .filter(Category.user_id == user_id) \
        .group_by(Category.name) \
        .all()
    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "total_budget": float(total_budget),
        "net_savings": float(net_savings),
        "category_totals": category_totals,
    }


@dashboard_bp.route("/")
@login_required
def index():
    summary = compute_summary(current_user.id)
    recent_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.expense_date.desc()).limit(5).all()
    recent_income = Income.query.filter_by(user_id=current_user.id).order_by(Income.received_date.desc()).limit(5).all()
    financial_advice = generate_financial_advice(current_user)
    return render_template(
        "dashboard/index.html",
        summary=summary,
        recent_expenses=recent_expenses,
        recent_income=recent_income,
        financial_advice=financial_advice,
    )
