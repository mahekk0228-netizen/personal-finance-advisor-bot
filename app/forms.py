from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class IncomeForm(FlaskForm):
    source = StringField("Source", validators=[DataRequired(), Length(max=120)])
    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=0.01)])
    received_date = DateField("Received Date", format="%Y-%m-%d", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Save income")


class ExpenseForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=120)])
    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=0.01)])
    expense_date = DateField("Expense Date", format="%Y-%m-%d", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save expense")


class BudgetForm(FlaskForm):
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    month = StringField("Month", validators=[DataRequired(), Length(min=7, max=7)])
    planned_amount = FloatField("Monthly Budget", validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField("Save budget")
