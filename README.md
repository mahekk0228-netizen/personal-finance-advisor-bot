# Personal Finance Advisor Bot

A Flask-based AI-powered personal finance management application for tracking income, expenses, budgets, financial summaries, and AI-generated recommendations.

## Features

- Secure user authentication
- Income and expense tracking
- Budget planning by category
- Monthly financial summary
- AI-powered budget and savings insights
- Dashboard with analytics
- SQLite/PostgreSQL support
- Environment-based configuration

## Tech Stack

- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLAlchemy
- Jinja2
- Bootstrap
- OpenAI or Gemini AI integration
- SQLite / PostgreSQL

## Quick Start

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
4. Update keys and database settings in `.env`.
5. Run the app:
   ```bash
   python run.py
   ```
6. Open `http://localhost:5000`

## Environment Variables

See `.env.example` for supported variables.

## Deployment

For public access, run the app locally and expose it via Ngrok:

```bash
ngrok http 5000
```

## Disclaimer

This project is for educational and personal finance tracking use. AI-generated recommendations are informational and not professional financial advice.
