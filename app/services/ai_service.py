from flask import current_app
from app.extensions import db
from app.models import Category, Expense, Income


def _heuristic_advice(user):
    total_income = (
        db.session.query(db.func.coalesce(db.func.sum(Income.amount), 0))
        .filter_by(user_id=user.id)
        .scalar()
        or 0
    )
    total_expense = (
        db.session.query(db.func.coalesce(db.func.sum(Expense.amount), 0))
        .filter_by(user_id=user.id)
        .scalar()
        or 0
    )
    categories = (
        db.session.query(Category.name, db.func.sum(Expense.amount).label("total"))
        .join(Expense, Expense.category_id == Category.id)
        .filter(Category.user_id == user.id)
        .group_by(Category.name)
        .all()
    )

    if total_income <= 0:
        return "Add income records to generate a personalized budget and savings plan."

    expense_ratio = (total_expense / total_income) * 100 if total_income else 0
    top_category = max(categories, key=lambda item: item[1]) if categories else None

    if expense_ratio > 80:
        advice = "Your spending is high relative to income. Reduce discretionary spending and increase automated savings."
    elif expense_ratio > 60:
        advice = "Your spending is moderate. Focus on a 20% savings target and cut impulse purchases."
    else:
        advice = "You are spending within a healthy range. Prioritize building an emergency fund and reducing debt."

    if top_category:
        advice += f" Your largest expense category is {top_category[0]} at ${top_category[1]:.2f}."

    return advice


def generate_financial_advice(user):
    provider = current_app.config.get("AI_PROVIDER", "gemini").lower()

    total_income = (
        db.session.query(db.func.coalesce(db.func.sum(Income.amount), 0))
        .filter_by(user_id=user.id)
        .scalar()
        or 0
    )
    total_expense = (
        db.session.query(db.func.coalesce(db.func.sum(Expense.amount), 0))
        .filter_by(user_id=user.id)
        .scalar()
        or 0
    )
    categories = (
        db.session.query(Category.name, db.func.sum(Expense.amount).label("total"))
        .join(Expense, Expense.category_id == Category.id)
        .filter(Category.user_id == user.id)
        .group_by(Category.name)
        .all()
    )

    prompt = (
        f"You are a personal finance advisor. The user has ${total_income:.2f} in income and ${total_expense:.2f} in expenses. "
        f"Category breakdown: {', '.join(f'{name}: ${total:.2f}' for name, total in categories) if categories else 'No expense records yet'}. "
        "Give 3 practical recommendations with immediate actions. Keep it concise and actionable."
    )

    if provider == "openai" and current_app.config.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI

            client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a personal finance assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return _heuristic_advice(user)

    if provider == "gemini" and current_app.config.get("GEMINI_API_KEY"):
        try:
            import google.generativeai as genai

            genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return _heuristic_advice(user)

    return _heuristic_advice(user)
