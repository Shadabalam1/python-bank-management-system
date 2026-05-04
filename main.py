import json
import random
import string
from pathlib import Path


class Bank:

    database = 'data.json'
    data = []

    # Load existing data
    try:
        if Path(database).exists():
            with open(database, 'r') as file:
                loaded = json.load(file)
                data = loaded if isinstance(loaded, list) else []
        else:
            print("No data file found. Starting fresh.")
    except Exception as err:
        print(f"Error loading data: {err}")
        data = []

    # Private method to update file

    @staticmethod
    def __update(data):
        try:
            with open(Bank.database, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as err:
            print(f"Error updating data: {err}")

    # Generate random account number

    @staticmethod
    def generate_account_number():
        return ''.join(random.choices(string.digits, k=10))

    # Find account by account number + PIN
    def __find_account(self, account_number, pin):
        for account in self.data:
            if account["account_number"] == account_number and account["pin"] == pin:
                return account
        return None

    # Find account index
    def __find_index(self, account_number):
        for i, account in enumerate(self.data):
            if account["account_number"] == account_number:
                return i
        return -1

    # Create account
    def create_account(self):
        info = {
            "name": input("Enter your name: "),
            "age": int(input("Enter your age: ")),
            "email": input("Enter your email: "),
            "pin": int(input("Enter your 4-digit PIN: ")),
            "account_number": Bank.generate_account_number(),
            "balance": 0
        }

        # Validation
        if info["age"] < 18 or len(str(info["pin"])) != 4:
            print("Invalid age or PIN. Account not created.")
            return

        print("\nCreating account...\n")
        for key, value in info.items():
            print(f"{key}: {value}")

        print("\n  Please save your account number for future use!")

        # Save data
        self.data.append(info)
        self.__update(self.data)
        print("\n Account created successfully!\n")

    # Deposit money
    def deposit(self):
        account_number = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))

        account = self.__find_account(account_number, pin)
        if not account:
            print(" Account not found or incorrect PIN.")
            return

        try:
            amount = float(input("Enter amount to deposit: "))
        except ValueError:
            print(" Invalid amount.")
            return

        if amount <= 0:
            print(" Deposit amount must be greater than zero.")
            return

        idx = self.__find_index(account_number)
        self.data[idx]["balance"] += amount
        self.__update(self.data)

        print(f"\n✅ ₹{amount:.2f} deposited successfully!")
        print(f"   New balance: ₹{self.data[idx]['balance']:.2f}\n")

    # Withdraw money
    def withdraw(self):
        account_number = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))

        account = self.__find_account(account_number, pin)
        if not account:
            print(" Account not found or incorrect PIN.")
            return

        try:
            amount = float(input("Enter amount to withdraw: "))
        except ValueError:
            print(" Invalid amount.")
            return

        if amount <= 0:
            print(" Withdrawal amount must be greater than zero.")
            return

        if amount > account["balance"]:
            print(" Insufficient balance.")
            return

        idx = self.__find_index(account_number)
        self.data[idx]["balance"] -= amount
        self.__update(self.data)

        print(f"\n ₹{amount:.2f} withdrawn successfully!")
        print(f"   Remaining balance: ₹{self.data[idx]['balance']:.2f}\n")

    # Check balance
    def check_balance(self):
        account_number = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))

        account = self.__find_account(account_number, pin)
        if not account:
            print(" Account not found or incorrect PIN.")
            return

        print(f"\n👤 Account Holder : {account['name']}")
        print(f"   Account Number : {account['account_number']}")
        print(f"   Balance        : ₹{account['balance']:.2f}\n")

    # Update account
    def update_account(self):
        account_number = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))

        account = self.__find_account(account_number, pin)
        if not account:
            print(" Account not found or incorrect PIN.")
            return

        idx = self.__find_index(account_number)

        print("\nWhat would you like to update?")
        print("  1. Name")
        print("  2. Email")
        print("  3. PIN")

        try:
            field_choice = int(input("Enter choice: "))
        except ValueError:
            print(" Invalid input.")
            return

        if field_choice == 1:
            self.data[idx]["name"] = input("Enter new name: ")
        elif field_choice == 2:
            self.data[idx]["email"] = input("Enter new email: ")
        elif field_choice == 3:
            try:
                new_pin = int(input("Enter new 4-digit PIN: "))
            except ValueError:
                print(" Invalid PIN.")
                return
            if len(str(new_pin)) != 4:
                print(" PIN must be exactly 4 digits.")
                return
            self.data[idx]["pin"] = new_pin
        else:
            print(" Invalid choice.")
            return

        self.__update(self.data)
        print("\n Account updated successfully!\n")

    # Delete account
    def delete_account(self):
        account_number = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))

        account = self.__find_account(account_number, pin)
        if not account:
            print(" Account not found or incorrect PIN.")
            return

        confirm = input(f"Are you sure you want to delete account {account_number}? (yes/no): ")
        if confirm.lower() != "yes":
            print(" Deletion cancelled.")
            return

        idx = self.__find_index(account_number)
        self.data.pop(idx)
        self.__update(self.data)

        print("\n Account deleted successfully!\n")



user = Bank()

print("\n====== 🏦 Welcome to PyBank ======")
print("1. Create Account")
print("2. Deposit Money")
print("3. Withdraw Money")
print("4. Check Balance")
print("5. Update Account")
print("6. Delete Account")
print("==================================\n")

try:
    choice = int(input("Enter your choice: "))
except ValueError:
    print(" Invalid input")
    exit()

if choice == 1:
    user.create_account()
elif choice == 2:
    user.deposit()
elif choice == 3:
    user.withdraw()
elif choice == 4:
    user.check_balance()
elif choice == 5:
    user.update_account()
elif choice == 6:
    user.delete_account()
else:
    print("❌ Invalid choice")
