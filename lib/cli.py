import click
from model import User, Transaction, Category, session

@click.group()
def cli():
    """Personal Finance Tracker CLI"""
    pass


@cli.command()
@click.option('--username', prompt='Username', help='Username for the new user')
@click.option('--password', prompt='Password', hide_input=True, help='Password for the new user')
def create_user(username, password):
    """Create a new user."""
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        click.echo(f'User "{username}" already exists.')
    else:
        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()
        click.echo(f'User "{username}" created successfully.')

@cli.command()
@click.option('--date', prompt='Transaction date (YYYY-MM-DD)', help='Date of the transaction')
@click.option('--description', prompt='Description', help='Description of the transaction')
@click.option('--amount', prompt='Amount', type=float, help='Transaction amount')
@click.option('--category', prompt='Category', help='Transaction category')
@click.option('--username', prompt='Username', help='Username for the transaction')
def add_income(date, description, amount, category, username):
    """Add an income transaction."""
    user = session.query(User).filter_by(username=username).first()
    if user:
        category_obj = session.query(Category).filter_by(name=category).first()
        if category_obj:
            transaction = Transaction(
                date=date,
                description=description,
                amount=amount,
                category=category_obj,
                user=user
            )
            session.add(transaction)
            session.commit()
            click.echo(f'Added income transaction: {description} - ${amount}')
        else:
            click.echo(f'Category "{category}" not found.')
    else:
        click.echo(f'User "{username}" not found.')

@cli.command()
@click.option('--date', prompt='Transaction date (YYYY-MM-DD)', help='Date of the transaction')
@click.option('--description', prompt='Description', help='Description of the transaction')
@click.option('--amount', prompt='Amount', type=float, help='Transaction amount')
@click.option('--category', prompt='Category', help='Transaction category')
@click.option('--username', prompt='Username', help='Username for the transaction')
def add_expense(date, description, amount, category, username):
    """Add an expense transaction."""
    user = session.query(User).filter_by(username=username).first()
    if user:
        category_obj = session.query(Category).filter_by(name=category).first()
        if category_obj:
            transaction = Transaction(
                date=date,
                description=description,
                amount=-amount,  # Expenses are represented as negative amounts
                category=category_obj,
                user=user
            )
            session.add(transaction)
            session.commit()
            click.echo(f'Added expense transaction: {description} - ${amount}')
        else:
            click.echo(f'Category "{category}" not found. Existing categories:')
            existing_categories = session.query(Category).all()
            for existing_category in existing_categories:
                click.echo(existing_category.name)
    else:
        click.echo(f'User "{username}" not found.')

@cli.command()
@click.option('--name', prompt='Username', help='Username for listing transactions')
def list_transactions(name):
    """List all transactions for a user."""
    user = session.query(User).filter_by(username=name).first()
    print(user)
    if user:
        transactions = session.query(Transaction).filter_by(user=user).all()
        click.echo('Listing all transactions:')
        for transaction in transactions:
            click.echo(f'{transaction.date} - {transaction.description}: ${transaction.amount}')
    else:
        click.echo(f'User "{name}" not found.')

@cli.command()
@click.option('--username', prompt='Username', help='Username for viewing financial summary')
def view_summary(username):
    """View financial summary for a user."""
    user = session.query(User).filter_by(username=username).first()
    if user:
        transactions = session.query(Transaction).filter_by(user=user).all()
        total_income = sum(transaction.amount for transaction in transactions if transaction.amount > 0)
        total_expenses = sum(transaction.amount for transaction in transactions if transaction.amount < 0)
        available_budget = total_income + total_expenses
        click.echo(f'Financial Summary for {username}:')
        click.echo(f'Total Income: ${total_income}')
        click.echo(f'Total Expenses: ${total_expenses}')
        click.echo(f'Available Budget: ${available_budget}')
    else:
        click.echo(f'User "{username}" not found.')

if __name__ == '__main__':
    cli()






