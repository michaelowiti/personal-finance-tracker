

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User, Transaction, Category  # Import your database models

# Create an SQLAlchemy engine and session
engine = create_engine('sqlite:///finance_tracker.db')  # Change the database URL as needed
Session = sessionmaker(bind=engine)
session = Session()

# Sample data for users
sample_users = [
    {"username": "john_doe", "password": "hashed_password1"},
    {"username": "jane_smith", "password": "hashed_password2"},
]

# Sample data for categories
sample_categories = [
    {"name": "Salary"},
    {"name": "Rent"},
    {"name": "Groceries"},
    {"name": "Utilities"},
    {"name": "Entertainment"},
]

#Sample data for transactions
sample_transactions = [
    {"date": "2023-09-01", "description": "Monthly Salary", "amount": 5000.00, "category_name": "Salary", "user_id": 1},
    {"date": "2023-09-05", "description": "Rent Payment", "amount": -1200.00, "category_name": "Rent", "user_id": 1},
    {"date": "2023-09-10", "description": "Grocery Shopping", "amount": -200.00, "category_name": "Groceries", "user_id": 2},
    {"date": "2023-09-15", "description": "Electricity Bill", "amount": -100.00, "category_name": "Utilities", "user_id": 2},
    {"date": "2023-09-20", "description": "Movie Tickets", "amount": -50.00, "category_name": "Entertainment", "user_id": 1},
]



# Function to add users to the database
def add_users():
    for user_data in sample_users:
        user = User(**user_data)
        session.add(user)
    session.commit()

# Function to add categories to the database
def add_categories():
    for category_data in sample_categories:
        category = Category(**category_data)
        session.add(category)
    session.commit()

#Function to add transactions to the database


def add_transactions():
    for transaction_data in sample_transactions:
        category_name = transaction_data["category_name"] 
        category = session.query(Category).filter_by(name=category_name).first()
        if category:
            transaction_data["category_id"] = category.id
            # Remove 'category_name' from transaction_data
            del transaction_data["category_name"]
            transaction = Transaction(**transaction_data)
            session.add(transaction)
    
    # Commit all transactions outside the loop
    session.commit()



    # Commit all transactions outside the loop
    session.commit()

if __name__ == '__main__':
    #add_users()
    #add_categories()
    add_transactions()
    print("Seed data has been added to the database.")




