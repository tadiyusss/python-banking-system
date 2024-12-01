import mysql.connector
import getpass
import os
from hashlib import sha256
from colorama import Fore, Back
import string
import random

connection = mysql.connector.connect(
    host="mysql.development.home",
    user="root",
    password="Sktpawer123",
    database="banking_system",
    auth_plugin='mysql_native_password'
)

cursor = connection.cursor()
colors = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "clear": Fore.RESET
}

def random_string(length = 6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title(page = None):
    if page:
        print(f"Banking System - {page}\n")
    else:
        print("Banking System\n")

def system_message(message, color):
    input(f"{colors[color]}{message}{colors['clear']}")

def login():
    clear_screen()
    print_title("Login")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    hashed_password = sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cursor.fetchone()
    return user

def register():
    clear_screen()
    print_title("Register")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    hashed_password = sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, hashed_password))
    connection.commit()
    system_message("\nYou have successfully registered. Press enter to continue.", "green")

def create_account(user):
    clear_screen()
    print_title("Create Account")
    account_number = random_string(10)
    balance = 0
    cursor.execute("INSERT INTO accounts (user_id, account_number, balance) VALUES (%s, %s, %s)", (user[0], account_number, balance))
    connection.commit()
    system_message(f"\nYour account number is {account_number}. Press enter to continue.", "green")

def deposit(user):
    clear_screen()
    print_title("Deposit")

    cursor.execute("SELECT * FROM accounts WHERE user_id = %s", (user[0],))
    accounts = cursor.fetchall()

    if len(accounts) == 0:
        system_message("You don't have any account. Press enter to continue.", "red")
    else:
        print("Select an account to deposit to:")
        for index, account in enumerate(accounts):
            print(f"[{index + 1}] {account[3]} : {account[2]} PHP")
        choice = int(input("\nEnter your choice: ")) - 1
        amount = float(input("Enter the amount to deposit: "))
        if choice < 0 or choice >= len(accounts):
            system_message("\nInvalid account, Press enter to continue", "red")
        elif amount <= 0:
            system_message("\nInvalid amount. Press enter to continue.", "red")
        else:
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, accounts[choice][0]))
            connection.commit()
            system_message("\nDeposit successful. Press enter to continue.", "green")

        
def withdraw(user):
    clear_screen()
    print_title("Withdraw")

    cursor.execute("SELECT * FROM accounts WHERE user_id = %s", (user[0],))
    accounts = cursor.fetchall()

    if len(accounts) == 0:
        system_message("You don't have any account. Press enter to continue.", "red")
    else:
        print("Select an account to withdraw from:")
        for index, account in enumerate(accounts):
            print(f"[{index + 1}] {account[3]} : {account[2]} PHP")
        choice = int(input("\nEnter your choice: ")) - 1
        amount = float(input("Enter the amount to withdraw: "))
        if choice < 0 or choice >= len(accounts):
            system_message("\nInvalid account, Press enter to continue", "red")
        elif amount <= 0:
            system_message("\nInvalid amount. Press enter to continue.", "red")
        elif amount > accounts[choice][2]:
            system_message("\nInsufficient balance. Press enter to continue.", "red")
        else:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, accounts[choice][0]))
            connection.commit()
            system_message("\nWithdraw successful. Press enter to continue.", "green")
    
def balance(user):
    clear_screen()
    print_title("Balance")

    cursor.execute("SELECT * FROM accounts WHERE user_id = %s", (user[0],))
    accounts = cursor.fetchall()

    if len(accounts) == 0:
        system_message("You don't have any account. Press enter to continue.", "red")
    else:
        print("Accounts:")
        for account in accounts:
            print(f"{account[3]} : {account[2]} PHP")
        input("\nPress enter to continue.")

def transfer(user):
    clear_screen()
    print_title("Transfer")

    cursor.execute("SELECT * FROM accounts WHERE user_id = %s", (user[0],))
    accounts = cursor.fetchall()

    if len(accounts) == 0:
        system_message("You don't have any account. Press enter to continue.", "red")
    else:
        print("Select an account to transfer from:")
        for index, account in enumerate(accounts):
            print(f"[{index + 1}] {account[3]} : {account[2]} PHP")
        choice = int(input("\nEnter your choice: ")) - 1
        amount = float(input("Enter the amount to transfer: "))
        cursor.execute("SELECT account_number, account_id FROM accounts WHERE account_number = %s", (input("Enter account number to transfer to: "),))
        transfer_to = cursor.fetchone()
        if choice < 0 or choice >= len(accounts):
            system_message("\nInvalid account choosen, Press enter to continue", "red")
        elif amount <= 0:
            system_message("\nInvalid amount. Press enter to continue.", "red")
        elif amount > accounts[choice][2]:
            system_message("\nInsufficient balance. Press enter to continue.", "red")
        elif transfer_to == accounts[choice][3]:
            system_message("\nYou can't transfer to the same account. Press enter to continue.", "red")
        elif not transfer_to:
            system_message("\nThe account number you entered does not exist.. Press enter to continue.", "red")
        else:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, accounts[choice][0]))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, transfer_to[0]))
            cursor.execute("INSERT INTO transactions (sender_id, receiver_id, amount) VALUES (%s, %s, %s)", (accounts[choice][0], transfer_to[1], amount))
            connection.commit()
            system_message("\nTransfer successful. Press enter to continue.", "green")


def user_menu(user):
    while True:
        clear_screen()
        print_title("Main Menu")
        print(f"Welcome {user[1]}!")
        print("[C]reate Account")
        print("[D]eposit")
        print("[W]ithdraw")
        print("[B]alance")
        print("[T]ransfer")
        print("[E]xit")
        choice = input("\nEnter your choice: ").lower()
        if choice == 'c':
            create_account(user)
        elif choice == 'd':
            deposit(user)
        elif choice == 'w':
            withdraw(user)
        elif choice == 'b':
            balance(user)
        elif choice == 't':
            transfer(user)
        elif choice == 'e':
            break


while True:
    clear_screen()
    print_title()
    print("[L]ogin")
    print("[R]egister")
    print("[E]xit")
    choice = input("\nEnter your choice: ").lower()
    if choice == 'l':
        user = login()
        if user:
            user_menu(user)
        else:
            system_message("\nInvalid username or password. Press enter to continue.", "red")

    elif choice == 'r':
        register()
    elif choice == 'e':
        break