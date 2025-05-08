# ------------- file check ----------------

import os

#-------------- curent date and time ------

from datetime import datetime

#-------------- File paths ----------------

ACCOUNTS_FILE = 'accounts.txt'             # ---- account details ------
TRANSACTIONS_FILE = 'transactions.txt'     # ---- transaction details --
FEEDBACK_FILE = 'feedback.txt'             # ---- transaction details --

#-------------- Admin credentials ---------

ADMIN_USERNAME = 'admin' #--- hard coded --
ADMIN_PASSWORD = '1234'  #--- hard coded --

#-------------  Ensure data files exist ---

for file in [ACCOUNTS_FILE, TRANSACTIONS_FILE, FEEDBACK_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            pass

#-------------- Helper functions ----------

def read_accounts():
    accounts = {}
    with open(ACCOUNTS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                acc_num, name, acc_type, balance, password = line.strip().split('|')
                accounts[acc_num] = {'name': name, 'type': acc_type, 'balance': float(balance), 'password': password}
    return accounts

def write_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        for acc_num, info in accounts.items():
            f.write(f"{acc_num}|{info['name']}|{info['type']}|{info['balance']:.2f}|{info['password']}\n")

def append_transaction(acc_num, trans_type, amount):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(TRANSACTIONS_FILE, 'a') as f:
        f.write(f"{acc_num}|{trans_type}|{amount:.2f}|{date}\n")

def append_feedback(acc_num, feedback):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(FEEDBACK_FILE, 'a') as f:
        f.write(f"{acc_num}|{feedback}|{date}\n")

#-------------- Account operations -----------

def create_account():
    accounts = read_accounts()
    acc_num = input("Enter new Account Number: ")
    if acc_num in accounts:
        print("Account number already exists.")
        return
    name = input("Enter Account Holder Name: ")
    acc_type = input("Enter Account Type (Savings/Current): ")
    balance = float(input("Enter Initial Balance: "))
    password = input("Set Account Password: ")
    accounts[acc_num] = {'name': name, 'type': acc_type, 'balance': balance, 'password': password}
    write_accounts(accounts)
    print("Account created successfully.")

def view_account(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        info = accounts[acc_num]
        print(f"Account Number: {acc_num}")
        print(f"Holder Name: {info['name']}")
        print(f"Account Type: {info['type']}")
        print(f"Balance: {info['balance']:.2f}")
    else:
        print("Account not found.")

def modify_account(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        name = input("Enter new Holder Name: ")
        acc_type = input("Enter new Account Type (Savings/Current): ")
        accounts[acc_num]['name'] = name
        accounts[acc_num]['type'] = acc_type
        write_accounts(accounts)
        print("Account modified successfully.")
    else:
        print("Account not found.")

def delete_account(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        del accounts[acc_num]
        write_accounts(accounts)
        print("Account deleted successfully.")
    else:
        print("Account not found.")

#--------------- Transaction operations -------------------------

def deposit(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        amount = float(input("Enter amount to deposit: "))
        accounts[acc_num]['balance'] += amount
        write_accounts(accounts)
        append_transaction(acc_num, 'Deposit', amount)
        print("Deposit successful.")
    else:
        print("Account not found.")

def withdraw(acc_num):
    accounts = read_accounts()
    if acc_num in accounts:
        amount = float(input("Enter amount to withdraw: "))
        if accounts[acc_num]['balance'] >= amount:
            accounts[acc_num]['balance'] -= amount
            write_accounts(accounts)
            append_transaction(acc_num, 'Withdrawal', amount)
            print("Withdrawal successful.")
        else:
            print("Insufficient balance.")
    else:
        print("Account not found.")

#---------------------- Feedback ---------------------

def submit_feedback(acc_num):
    feedback = input("Enter your feedback: ")
    append_feedback(acc_num, feedback)
    print("Thank you for your feedback.")

#--------------------- Admin panel -------------------

def admin_panel():
    while True:
        print("\n-------- Admin Panel --------")
        print("🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹")
        print("1. View All Accounts        🔹")
        print("2. View All Transactions    🔹")
        print("3. View All Feedback        🔹")
        print("4. Create New Account       🔹")
        print("5. Delete Account           🔹")
        print("6. Logout                   🔹")
        print("🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n ")
        choice = input("Enter your choice: ")
        if choice == '1':
            accounts = read_accounts()
            for acc_num, info in accounts.items():
                print(f"{acc_num} | {info['name']} | {info['type']} | {info['balance']:.2f}")
        elif choice == '2':
            with open(TRANSACTIONS_FILE, 'r') as f:
                for line in f:
                    print(line.strip())
        elif choice == '3':
            with open(FEEDBACK_FILE, 'r') as f:
                for line in f:
                    print(line.strip())
        elif choice == '4':
            create_account()
        elif choice == '5':
            acc_num = input("Enter Account Number to delete: ")
            delete_account(acc_num)
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

#--------------------- Customer panel ----------------------------

def customer_panel(acc_num):
    while True:
        print(f"\n--- Welcome, {acc_num} ---")
        print("🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹 ")
        print("1. View Account           🔹")
        print("2. Deposit                🔹")
        print("3. Withdraw               🔹")
        print("4. Submit Feedback        🔹")
        print("5. Logout                 🔹")
        print("🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n ")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_account(acc_num)
        elif choice == '2':
            deposit(acc_num)
        elif choice == '3':
            withdraw(acc_num)
        elif choice == '4':
            submit_feedback(acc_num)
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

#-------------------- Login functions ----------------------

def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Admin login successful.")
        admin_panel()
    else:
        print("Invalid admin credentials.")

def customer_login():
    accounts = read_accounts()
    acc_num = input("Enter Account Number: ")
    password = input("Enter Password: ")
    if acc_num in accounts and accounts[acc_num]['password'] == password:
        print("Customer login successful.")
        customer_panel(acc_num)
    else:
        print("Invalid account number or password.")

# -------------------- Main menu ----------------------------

def main():
    while True:
        print("\n--💲- Mini Banking System -💲--")
        print("🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹")
        print("1. Admin Login                🔹")
        print("2. Customer Login             🔹")
        print("3. Exit                       🔹")
        print("🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n ")
        choice = input("Enter your choice: ")
        if choice == '1':
            admin_login()
        elif choice == '2':
            customer_login()
        elif choice == '3':
            print("Thank you for using the Mini Banking System.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

