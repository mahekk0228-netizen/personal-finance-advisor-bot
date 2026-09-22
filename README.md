# Personal Finance Advisor Bot

A Flask-based AI-powered personal finance management application for tracking income, expenses, budgets, financial summaries, and AI-generated recommendations.

## Features
- Secure user authentication
- Income and expense tracking
- Budget planning and category analysis
- Monthly financial summaries
- AI-powered financial insights
- Dashboard analytics
- SQLite/PostgreSQL ready
- Environment-based configuration

## Tech Stack
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Jinja2
- WTForms
- python-dotenv
- SQLite/PostgreSQL
- OpenAI or Google Gemini SDK

## Quick Start
1. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Copy environment variables:
   cp .env.example .env

4. Update `.env` with your secrets and database URL.

5. Run the app:
   python run.py

6. Open http://localhost:5000

## Environment Variables
- SECRET_KEY
- DATABASE_URL
- AI_PROVIDER (gemini or openai)
- GEMINI_API_KEY
- OPENAI_API_KEY

## Deployment
For public testing, expose the local app with Ngrok:

ngrok http 5000

## Disclaimer
AI-generated recommendations are informational only and are not professional financial advice.
