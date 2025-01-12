import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import json

# Load the .env file
load_dotenv()

# Load environment variables
SIMPLEFIN_BASE_URL = os.getenv("SIMPLEFIN_URL")
SIMPLEFIN_USERNAME = os.getenv("SIMPLEFIN_USERNAME")
SIMPLEFIN_PASSWORD = os.getenv("SIMPLEFIN_PASSWORD")
JSON_OUTPUT_FILE = os.getenv("JSON_OUTPUT_FILE")
ACCOUNTS_OUTPUT_FILE = os.getenv("ACCOUNTS_OUTPUT_FILE")
TRANSACTIONS_OUTPUT_FILE = os.getenv("TRANSACTIONS_OUTPUT_FILE")
DEBUG_MODE = bool(os.getenv("DEBUG_MODE"))

# Helper functions
def fetch_account_data(URL):
    """
    Fetch all accounts and their transactions in a single API call from SimpleFIN.
    """
    try:
        response = requests.get(
            url=URL,
            auth=(SIMPLEFIN_USERNAME, SIMPLEFIN_PASSWORD),
        )
        if response.status_code == 200:
            print(f'Good response to GET!')
            data = response.json()
            if DEBUG_MODE is True:
                # Write the JSON data to a file (for debugging)
                print("Writing response to json...")
                with open(f"{JSON_OUTPUT_FILE}_{datetime.now().strftime('%Y%m%d')}.json", "w") as file:
                    json.dump(data, file, indent=4)
            return data
        else:
            print(f"Error fetching account data: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error connecting to SimpleFIN API: {e}")
        return []

def process_account_data(account_data):
    """
    Process the account data to extract transactions into a unified DataFrame.
    Each transaction includes account-specific information for clarity.
    """

    accounts = []

    for account in account_data['accounts']:
        account_name = account['name']
        account_currency = account['currency']
        account_balance = account['balance']

        accounts.append({
            "Account type": "Depository",
            "Name": account_name,
            "balance": account_balance.replace("[,$]", ""),
            "Currency": account_currency
        })

    # Convert the accounts into a DataFrame
    return pd.DataFrame(accounts)

def process_transaction_data(account_data):
    """
    Process the account data to extract transactions into a unified DataFrame.
    Each transaction includes account-specific information for clarity.
    """

    transactions = []

    for account in account_data['accounts']:
        account_name = account['name']
        account_currency = account['currency']
        for transaction in account['transactions']:
            transactions.append({
                "date": datetime.fromtimestamp(transaction["transacted_at"]).strftime('%m/%d/%Y') if transaction["transacted_at"] else None,
                "amount": transaction['amount'],
                "name": transaction['description'],
                "currency": account_currency,
                "category": "",
                "tags": "",
                "account": account_name,
                "notes" : ""
            })

    # Convert the transactions into a DataFrame
    return pd.DataFrame(transactions)

def clean_and_transform(filtered_df):
    
    # Remove currency symbols
    filtered_df["amount"] = filtered_df["amount"].replace("[,$]", "")
    
    return filtered_df[[  # Final cleaned and transformed DataFrame
        "date", "amount", "name", "currency", "category", "tags", "account", "notes"
    ]]

def export_csv(name, df, mode):

    # Export the cleaned and transformed data to a CSV file.
    filename = f"{name}_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

# Main script
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process and transform financial transactions.")
    parser.add_argument(
        "mode", 
        choices=["Daily", "Monthly", "All"], 
        help="Specify whether to fetch transactions from the last day or month."
    )
    args = parser.parse_args()

    if args.mode == "Monthly":
        # First second of the current day
        start_date = str(int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()))
    elif args.mode == "Daily":
        # First second of the first day of the current month
        start_date = str(int(datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()))
    else:
        # Defaults to start date of 1 / 1 / 2000
        start_date = str(int(datetime(2000, 1, 1, 0, 0, 0).timestamp()))
    
    print(start_date)
    SIMPLEFIN_FORMATTED_URL = f'{SIMPLEFIN_BASE_URL}?start-date={start_date}&balances-only=0'

    # Fetch all account data and transactions
    account_data = fetch_account_data(SIMPLEFIN_FORMATTED_URL)
    if not account_data:
        print("No account data retrieved from SimpleFIN.")
    else:
        # Process accounts and transactions into a unified DataFrame
        transactions = process_transaction_data(account_data)
        accounts = process_account_data(account_data)
        if accounts.empty:
            print("No accounts found.")
        else:
            print("Writing accounts to csv...")
            export_csv(ACCOUNTS_OUTPUT_FILE, accounts, args.mode)
            if transactions.empty:
                print("No transactions found.")
            else:
                # Filter transactions based on mode
                # filtered_transactions = filter_transactions_by_mode(transactions, args.mode)
                filtered_transactions = transactions
                if filtered_transactions.empty:
                    print(f"No transactions found for the specified {args.mode} period.")
                else:
                    # Clean and transform the data
                    transformed = clean_and_transform(filtered_transactions)
                    # Export to CSV
                    print("Writing transactions to csv...")
                    export_csv(TRANSACTIONS_OUTPUT_FILE, transformed, args.mode)
                    
