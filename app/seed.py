"""
Utility: populate the DB with the Kaggle McDonalds CSV so the front-end
has something to visualise immediately.

Place the downloaded file at data/mcdonalds.csv  (or change path).
"""
import pandas as pd, os, sys
from datetime import datetime
from . import create_app, db
from .models import User, Expense

CSV_PATH = os.getenv("CSV_PATH", "data/mcdonalds.csv")

def run():
    app = create_app()
    with app.app_context():
        # create a demo user
        user = User.query.filter_by(email="demo@demo.io").first() or \
               User.create("demo@demo.io", "demo123")

        df = pd.read_csv(CSV_PATH)
        # Assume the CSV has 'Date' and 'Open' columns.
        for _, row in df.iterrows():
            e = Expense(
                user_id=user.id,
                date=datetime.strptime(row['Date'], "%Y-%m-%d").date(),
                category="McDonalds",
                description="Imported line item",
                amount=float(row['Open'])        # treat 'Open' as amount
            )
            db.session.add(e)
        db.session.commit()
        print("Seed complete.")

if __name__ == "__main__":
    run()
