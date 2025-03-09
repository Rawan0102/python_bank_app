import csv

class BankFileHandler:
    FILE_NAME = "bank.csv"

    @staticmethod
    def load_customers():
        """Loads customer data from bank.csv"""
        customers = []
        try:
            with open(BankFileHandler.FILE_NAME, "r") as file:
                reader = csv.reader(file, delimiter=";") 
                for row in reader:
                    account_id, first_name, last_name, password, checking_balance, savings_balance = row
                    customers.append({
                        "account_id": account_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "password": password,
                        "checking_balance": float(checking_balance),
                        "savings_balance": float(savings_balance)
                    })
        except FileNotFoundError:
            print(" ❌ Error: bank.csv file not found!")
        return customers

    @staticmethod
    def save_customers(customers):
        """Writes updated customer data back to bank.csv"""
        with open(BankFileHandler.FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            for customer in customers:
                writer.writerow([
                    customer["account_id"],
                    customer["first_name"],
                    customer["last_name"],
                    customer["password"],
                    customer["checking_balance"],
                    customer["savings_balance"]
                ])

