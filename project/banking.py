import csv

class Bank:
    def __init__(self, filename='bank.csv'):
        self.filename = filename
        self.customers = self.load_customers()

    def load_customers(self):
        customers = {}
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file, delimiter=';') 
                for row in reader:
                    if len(row) < 6 or row[0] == "account_id":
                        continue  
                    account_id, first_name, last_name, password, checking, savings = row
                    customers[account_id] = Customer(account_id, first_name, last_name, password, float(checking), float(savings))
        except FileNotFoundError:
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings"])
        return customers

    def save_customers(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')  
            writer.writerow(["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings"])
            for customer in self.customers.values():
                writer.writerow([customer.account_id, customer.first_name, customer.last_name, customer.password, customer.balance_checking, customer.balance_savings])

    def add_customer(self):
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        password = input("Enter Password: ")
        
        # Ask for the type of accounts and their balances
        account_id = str(10000 + len(self.customers) + 1)  
        
        
        account_type = input("Do you want a 'checking' account, 'savings' account, or 'both'? ").lower()

        if 'checking' in account_type:
            balance_checking = float(input("Enter initial balance for checking account: $"))
        
        if 'savings' in account_type:
            balance_savings = float(input("Enter initial balance for savings account: $"))

        if 'both' in account_type:
            balance_checking = float(input("Enter initial balance for checking account: $"))
            balance_savings = float(input("Enter initial balance for savings account: $"))


        new_customer = Customer(account_id, first_name, last_name, password, balance_checking, balance_savings)
        self.customers[account_id] = new_customer
        self.save_customers()
        print(f"Account created! Your ID: {account_id}")

    def authenticate(self):
        account_id = input("Enter Account ID: ")
        password = input("Enter Password: ")
        if account_id in self.customers and self.customers[account_id].password == password:
            print("Login successful!")
            return self.customers[account_id]
        print("Login failed!")
        return None

class Customer:
    def __init__(self, account_id, first_name, last_name, password, balance_checking=0.0, balance_savings=0.0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = balance_checking
        self.balance_savings = balance_savings

    def display_balance(self):
        print(f"Checking Balance: ${self.balance_checking:.2f}")
        print(f"Savings Balance: ${self.balance_savings:.2f}")

    def deposit(self, account_type, amount):
        if amount <= 0:
            print("Invalid deposit amount.")
            return
        if account_type == "checking":
            self.balance_checking += amount
        elif account_type == "savings":
            self.balance_savings += amount
        print(f"Successfully deposited ${amount:.2f} into {account_type}.")

    def withdraw(self, account_type, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
            return
        if account_type == "checking":
            if amount > self.balance_checking:
                print("Insufficient funds.")
                return
            self.balance_checking -= amount
        elif account_type == "savings":
            if amount > self.balance_savings:
                print("Insufficient funds.")
                return
            self.balance_savings -= amount
        print(f"Successfully withdrew ${amount:.2f} from {account_type}.")

class Transfer:
    def __init__(self, bank, user):
        self.bank = bank
        self.user = user

    def transfer_between_own_accounts(self):
        print("\nTransfer Between Your Own Accounts")
        from_account = input("Which account would you like to transfer from? (checking/savings): ").lower()
        to_account = input("Which account would you like to transfer to? (checking/savings): ").lower()

        if from_account not in ['checking', 'savings'] or to_account not in ['checking', 'savings']:
            print("Invalid account type. Please choose 'checking' or 'savings'.")
            return
        
        if from_account == to_account:
            print("You cannot transfer between the same account type.")
            return

        amount = float(input(f"Enter amount to transfer from {from_account} to {to_account}: $"))
        
        if amount <= 0:
            print("Transfer amount must be greater than 0.")
            return

        # Check if the user has sufficient funds in the source account
        if from_account == 'checking' and amount > self.user.balance_checking:
            print("Insufficient funds in checking account.")
            return
        if from_account == 'savings' and amount > self.user.balance_savings:
            print("Insufficient funds in savings account.")
            return

        # Perform the transfer
        if from_account == 'checking':
            self.user.balance_checking -= amount
        elif from_account == 'savings':
            self.user.balance_savings -= amount

        if to_account == 'checking':
            self.user.balance_checking += amount
        elif to_account == 'savings':
            self.user.balance_savings += amount

        print(f"Successfully transferred ${amount:.2f} from {from_account} to {to_account}.")
        self.bank.save_customers()

    def transfer_to_another_customer(self):
        print("\nTransfer to Another Customer")
        recipient_id = input("Enter the recipient's account ID: ")

        if recipient_id not in self.bank.customers:
            print("Recipient account not found.")
            return
        
        recipient = self.bank.customers[recipient_id]
        from_account = input("Which account would you like to transfer from? (checking/savings): ").lower()
        amount = float(input(f"Enter amount to transfer from your {from_account}: $"))

        if amount <= 0:
            print("Transfer amount must be greater than 0.")
            return

        # Check if the user has sufficient funds in the source account
        if from_account == 'checking' and amount > self.user.balance_checking:
            print("Insufficient funds in checking account.")
            return
        if from_account == 'savings' and amount > self.user.balance_savings:
            print("Insufficient funds in savings account.")
            return

        # Perform the transfer from the user's account to the recipient's account
        if from_account == 'checking':
            self.user.balance_checking -= amount
            recipient.balance_checking += amount
        elif from_account == 'savings':
            self.user.balance_savings -= amount
            recipient.balance_savings += amount

        print(f"Successfully transferred ${amount:.2f} to {recipient.first_name} {recipient.last_name}'s account.")
        self.bank.save_customers()

# Test
bank = Bank()

while True:
    print("\nWelcome to Rawan's Bank 😊 🏦")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        bank.add_customer()
    elif choice == "2":
        user = bank.authenticate()
        if user:
            transfer = Transfer(bank, user)  # Initialize the Transfer class with the logged-in user
            while True:
                print("\n1. View Balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Transfer Money")
                print("5. Logout")
                action = input("Choose an option: ")
                if action == "1":
                    user.display_balance()
                elif action == "2":
                    account_type = input("Deposit to checking or savings? ").lower()
                    amount = float(input("Enter amount to deposit: "))
                    user.deposit(account_type, amount)
                    bank.save_customers()
                elif action == "3":
                    account_type = input("Withdraw from checking or savings? ").lower()
                    amount = float(input("Enter amount to withdraw: "))
                    user.withdraw(account_type, amount)
                    bank.save_customers()
                elif action == "4":
                    print("\n1. Transfer Between Your Own Accounts")
                    print("2. Transfer to Another Customer")
                    transfer_choice = input("Choose a transfer option: ")

                    if transfer_choice == "1":
                        transfer.transfer_between_own_accounts()
                    elif transfer_choice == "2":
                        transfer.transfer_to_another_customer()
                    else:
                        print("Invalid option. Try again.")
                elif action == "5":
                    print("Logged out.")
                    break
                else:
                    print("Invalid choice. Try again.")
    elif choice == "3":
        print("Thank you for using Rawan's Bank 😊!")
        break
    else:
        print("Invalid option. Try again.")