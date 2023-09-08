from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create an SQLAlchemy engine and session
engine = create_engine('sqlite:///finance_tracker.db', echo=True)  # Change the database URL as needed
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()

# Define the User table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)  # For simplicity, store hashed passwords in a real project

    # Establish a one-to-many relationship between User and Transaction
    transactions = relationship('Transaction', back_populates='user')

# Define the Category table
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    # Establish a one-to-many relationship between Category and Transaction
    transactions = relationship('Transaction', back_populates='category')

# Define the Transaction table
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(String(10), nullable=False)  # You can use DateTime for actual dates
    description = Column(String(255))
    amount = Column(Float, nullable=False)

    # Define foreign keys to User and Category tables
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # Establish many-to-one relationships with User and Category
    user = relationship('User', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')
        

# Create the database tables
Base.metadata.create_all(engine)
