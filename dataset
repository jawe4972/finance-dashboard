import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker to generate fake data
fake = Faker()

# --- Configuration ---
NUM_RECORDS = 500000
START_DATE = datetime.now() - timedelta(days=5*365) # 5 years ago
END_DATE = datetime.now()
OUTPUT_FILENAME = 'financial_transactions.csv'

# Define realistic categories and account types
CATEGORIES = [
    'Groceries', 'Dining', 'Transportation', 'Utilities', 'Rent/Mortgage',
    'Shopping', 'Entertainment', 'Health', 'Travel', 'Income', 'Transfers'
]
ACCOUNTS = ['Checking', 'Savings', 'Credit Card A', 'Credit Card B']

# --- Data Generation ---
print(f"Generating {NUM_RECORDS} records...")

transactions = []
for _ in range(NUM_RECORDS):
    # Choose a random category and determine if it's an expense or income
    category = random.choice(CATEGORIES)
    if category == 'Income':
        # Income amounts are positive
        amount = round(random.uniform(500.0, 5000.0), 2)
    else:
        # Expense amounts are negative
        amount = -round(random.uniform(5.0, 800.0), 2)

    # Generate a random timestamp within the 5-year window
    timestamp = fake.date_time_between(start_date=START_DATE, end_date=END_DATE)

    # Generate a plausible description
    description = fake.company() if random.random() > 0.3 else fake.bs()

    # Choose a random account
    account = random.choice(ACCOUNTS)

    transactions.append({
        'timestamp': timestamp,
        'description': description,
        'amount': amount,
        'category': category,
        'account': account
    })

# --- Create and Save DataFrame ---
# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(transactions)

# Sort by timestamp for a more realistic transaction log
df = df.sort_values(by='timestamp').reset_index(drop=True)

# Save the DataFrame to a CSV file
df.to_csv(OUTPUT_FILENAME, index=False)

print(f"Successfully created '{OUTPUT_FILENAME}' with {len(df)} records.")
print("File saved in the current directory.")
