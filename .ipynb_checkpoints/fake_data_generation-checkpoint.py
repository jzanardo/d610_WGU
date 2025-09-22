import pandas as pd
from faker import Faker
import random
from datetime import date, datetime, timedelta
from collections import OrderedDict

fake = Faker('en_US')

# File 1: Customer demographics with 1% sparsity

def generate_customers(num_customers):

    customers = []

    num_customers_complete = round(num_customers * 0.99, 0)
    num_customers_incomplete = num_customers - num_customers_complete
    
    age_bins = [
    (18, 25), (26, 30), (31, 40), (41, 55), (56, 80)
    ]
    weights = [
    0.15, 0.20, 0.30, 0.20, 0.15
    ]

    states = OrderedDict([
        ('Texas', 0.4),
        ('Oklahoma', 0.2),
        ('Louisiana', 0.15),
        ('Arkansas', 0.1),
        ('Mississippi', 0.07),
        ('Alabama', 0.05),
        ('Georgia', 0.03)
    ])
    
    for _ in range(int(num_customers_complete)):
        # Generate core customer data
        first_name = fake.first_name()
        last_name = fake.last_name()

        age_range = random.choices(age_bins, weights=weights, k=1)[0]
        min_age, max_age = age_range

        start_date = date.today() - timedelta(days=max_age * 365)
        end_date = date.today() - timedelta(days=min_age * 365)

        customer_record = {
            # Personal Information
            'first_name': first_name,
            'last_name': last_name,
            'ssn': fake.unique.ssn(),
            'date_of_birth': fake.date_of_birth(minimum_age=min_age, maximum_age=max_age),
            'gender': random.choice(['Male', 'Female']),
            
            # Location Information
            'state': fake.random_element(states),
            
            # Banking Information
            'account_number': fake.unique.random_number(digits=10),
            'annual_income': round(random.uniform(35000.00, 500000.00), 0),
            
            # Contact Information
            'occupation': random.choice(['Retired or does not work', 'Military or public safety', 'Business owner', 'Executive', 'Healthcare provider', 'Technologist', 'Education provider', 'Government employee', 'Retail employee', 'Student', 'Other'])
        }
        customers.append(customer_record)

    for _ in range(int(num_customers_incomplete)):
        # Generate core customer data
        first_name = fake.first_name()
        last_name = fake.last_name()

        customer_record = {
            # Personal Information
            'first_name': first_name,
            'last_name': last_name,
                        
            # Location Information
            'state': fake.random_element(states),
            
            # Banking Information
            'account_number': fake.unique.random_number(digits=10)
        }   
        customers.append(customer_record)
    
    return customers

# File 2: Investment positions with 1% sparsity

def generate_investment_balances(account_numbers: list, number_positions) -> pd.DataFrame:

    all_positions = []

    products = OrderedDict([
        ('High Yeld Savings', 0.5),
        ('Stocks', 0.19),
        ('Mutual Funds', 0.2),
        ('Bonds', 0.1),
        ('', 0.01)
    ])

    for _ in range (number_positions):

         account_id = random.choice(account_numbers)
        
         position = {
             'account_number': account_id,
             'product_name': fake.random_element(products),
             'balance': round(random.uniform(1000.00, 1000000.00), 0)
         }
         all_positions.append(position)

    df = pd.DataFrame(all_positions)
    return df    

# File 3: Loan positions with 1% sparsity

def generate_loan_balances(account_numbers: list, number_positions) -> pd.DataFrame:

    all_positions = []

    products = OrderedDict([
        ('Mortgage Loan', 0.3),
        ('Student Loan', 0.3),
        ('Personal Loan', 0.09),
        ('Credit Card', 0.2),
        ('Auto Loan', 0.1),
        ('', 0.01)
    ])

    for _ in range (number_positions):

         account_id = random.choice(account_numbers)
                    
         position = {
             'account_number': account_id,
             'product_name': fake.random_element(products),
             'balance': round(random.uniform(5000.00, 500000.00), 0)
         }
         all_positions.append(position)

    df = pd.DataFrame(all_positions)
    return df    

# File 4: Transactions with 1% sparsity

def generate_transactions(account_numbers: list, number_transactions) -> pd.DataFrame:

    all_transactions = []

    start_date = datetime(2025, 6, 25)
    end_date = datetime(2025, 10, 1)
    
    transactions = OrderedDict([
        ('Cash Withdrawal', 0.2),
        ('Check Deposit', 0.1),
        ('Check Payment', 0.05),
        ('Cash Deposit', 0.05),
        ('Online Payment', 0.2),
        ('Wire Transfer', 0.07),
        ('Salary Payment', 0.3),
        ('International Transfer', 0.02),
        ('', 0.01)
    ])

    for _ in range (number_transactions):

         account_id = random.choice(account_numbers)
                    
         transaction = {
             'account_number': account_id,
             'transaction_name': fake.random_element(transactions),
             'transaction_date': fake.date_between_dates(date_start=start_date, date_end=end_date),
             'amount': round(random.uniform(10.00, 15000.00), 0)
         }
         all_transactions.append(transaction)

    df = pd.DataFrame(all_transactions)
    return df    

# File 5: Sign-up survey with 1% sparsity

def generate_survey(account_numbers: list) -> pd.DataFrame:

    all_answers = []

    services = OrderedDict([
        ('Mortgage Loan', 0.1),
        ('Student Loan', 0.1),
        ('Personal Loan', 0.04),
        ('Credit Card', 0.1),
        ('Auto Loan', 0.05),
        ('Investment', 0.3),
        ('Transaction', 0.3),
        ('', 0.01)
    ])

    for account_id in account_numbers:

         answer = {
             'account_number': account_id,
             'service_name': fake.random_element(services)
         }
         all_answers.append(answer)

    df = pd.DataFrame(all_answers)
    return df    

# Generate 100,000 fake customers (file 1)
fake_customer_data = generate_customers(100000)
df = pd.DataFrame(fake_customer_data)
df.to_csv('customers.csv', index=False)
print(df)

# Generate 30,000 investment positions (file 2)
df_sorted = df.sort_values(by='annual_income', ascending=False).head(60000).reset_index(drop=True).copy()
df_shuffled = df_sorted.sample(frac=1).reset_index(drop=True).copy()
df_investments = generate_investment_balances(df_shuffled.account_number, 30000)
df_investments.to_csv('investments.csv', index=False)
print(df_investments)

# Generate 20,000 loan positions (file 3)
df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
filtered_df = df[(df['date_of_birth'].dt.year >= 1970) & (df['date_of_birth'].dt.year < 2002)].reset_index(drop=True).copy()
df_shuffled = filtered_df.sample(frac=1).reset_index(drop=True).copy()
df_loans = generate_loan_balances(df_shuffled.account_number, 20000)
df_loans.to_csv('loans.csv', index=False)
print(df_loans)

# Generate 300,000 transactions (file 4)
filtered_df = df[(df['date_of_birth'].dt.year >= 1960)].reset_index(drop=True).copy()
df_shuffled = filtered_df.sample(frac=1).reset_index(drop=True).copy()
df_transactions = generate_transactions(df_shuffled.account_number, 300000)
df_transactions.to_csv('transactions.csv', index=False)
print(df_transactions)

# Generate 70,000 sign-up survey answers (file 5)
df_shuffled = df.sample(frac=0.7).reset_index(drop=True).copy()
df_survey = generate_survey(df_shuffled.account_number)
df_survey.to_csv('survey.csv', index=False)
print(df_survey)
