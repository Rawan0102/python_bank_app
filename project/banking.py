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

# Test Unit
customers = BankFileHandler.load_customers()
if customers:
    print("✅ Customers loaded successfully!\n")
    for customer in customers:
        print(f"ID: {customer['account_id']}, Name: {customer['first_name']} {customer['last_name']}, Checking: ${customer['checking_balance']}, Savings: ${customer['savings_balance']}")
else:
    print("❌ Error: No customer data found!")

class Customer:
    def __init__(self, account_id, first_name, last_name, password, checking_balance=0, savings_balance=0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking_account = CheckingAccount(self, checking_balance)
        self.savings_account = SavingsAccount(self, savings_balance)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def verify_password(self, password):
        return self.password == password

    def __str__(self):
        return f"Customer: {self.get_full_name()} (ID: {self.account_id})"

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner  
        self.balance = float(balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"✅ Deposited ${amount:.2f} into {self.__class__.__name__}. New balance: ${self.balance:.2f}")
        else:
            print("❌ Deposit amount must be positive!")

    def withdraw(self, amount):
        if amount > self.balance:
            print("❌ Insufficient funds!")
        elif amount <= 0:
            print("❌ Withdrawal amount must be positive!")
        else:
            self.balance -= amount
            print(f"✅ Withdrawn ${amount:.2f}. New balance: ${self.balance:.2f}")

    def transfer(self, target_account, amount):
        if self.balance >= amount and amount > 0:
            self.balance -= amount
            target_account.balance += amount
            print(f"✅ Transferred ${amount:.2f} to {target_account.__class__.__name__}.")
        else:
            print("❌ Transfer failed. Check balance or amount!")

    def __str__(self):
        return f"{self.__class__.__name__}: ${self.balance:.2f}"

class CheckingAccount(Account):
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance)

class SavingsAccount(Account):
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance)

# Testing customer and acount

# Create a new customer with accounts
customer1 = Customer("10001", "suresh", "sigera", "juagw362", 1000, 10000)

print(customer1)
print(customer1.checking_account)
print(customer1.savings_account)

customer1.checking_account.deposit(500)

customer1.savings_account.withdraw(200)

customer1.checking_account.transfer(customer1.savings_account, 300)

class Bank:
    def __init__(self):
        self.customers = BankFileHandler.load_customers()
        self.logged_in_customer = None

    def login_customer(self, account_id, password):
        """Logs in a customer by verifying credentials."""
        for customer in self.customers:
            if customer['account_id'] == account_id and customer['password'] == password:
                self.logged_in_customer = customer
                print(f"✅ Welcome, {customer['first_name']}! You are now logged in.")
                return customer
        print("❌ Invalid login credentials.")
        return None

    def logout_customer(self):
        """Logs out the current customer."""
        if self.logged_in_customer:
            print(f"👋 Goodbye, {self.logged_in_customer.get_full_name()}!")
            self.logged_in_customer = None
        else:
            print("❌ No user is currently logged in.")

#Testing Login 
# bank = Bank()
# customer = bank.login_customer("10001", "juagw362")  
# if customer:
#     print(customer)  
#     print(customer.checking_account)  
#     print(customer.savings_account)  
#     customer.checking_account.deposit(200)
#     customer.savings_account.withdraw(500)
#     customer.checking_account.transfer(customer.savings_account, 300)

# bank.logout_customer()

# bank.login_customer("10001", "wrongpassword")