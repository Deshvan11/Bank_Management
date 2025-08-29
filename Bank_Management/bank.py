import json
import random
import string
from pathlib import Path


class Bank:
    database = 'data.json'
    data = []

    # Load data from file at initialization
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.load(fs)
        else:
            data = []
    except Exception as err:
        print(f"Error loading DB: {err}")
        data = []

    @staticmethod
    def __update():
        with open(Bank.database, 'w') as fs:
            json.dump(Bank.data, fs, indent=4)

    @classmethod
    def __account_generate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices(string.punctuation, k=1)
        account_id = alpha + num + spchar
        random.shuffle(account_id)
        return ''.join(account_id)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return None, "You are not eligible to open an account"
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": cls.__account_generate(),
            "balance": 0,
        }
        cls.data.append(info)
        cls.__update()
        return info, "Account created successfully"

    @classmethod
    def deposit(cls, accnumber, pin, amount):
        userdata = [i for i in cls.data if i['accountNo'] == accnumber and i['pin'] == pin]
        if not userdata:
            return None, "Invalid account number or pin"
        if amount <= 0 or amount > 10000:
            return None, "Amount should be between 1 and 10000"
        userdata[0]['balance'] += amount
        cls.__update()
        return userdata[0], f"Deposited {amount}. New balance: {userdata[0]['balance']}"

    @classmethod
    def withdraw(cls, accnumber, pin, amount):
        userdata = [i for i in cls.data if i['accountNo'] == accnumber and i['pin'] == pin]
        if not userdata:
            return None, "Invalid account number or pin"
        if amount <= 0 or amount > userdata[0]['balance']:
            return None, "Insufficient balance or invalid amount"
        userdata[0]['balance'] -= amount
        cls.__update()
        return userdata[0], f"Withdrawn {amount}. New balance: {userdata[0]['balance']}"

    @classmethod
    def show_details(cls, accnumber, pin):
        userdata = [i for i in cls.data if i['accountNo'] == accnumber and i['pin'] == pin]
        if not userdata:
            return None, "Invalid account number or pin"
        return userdata[0], "Account details fetched successfully"

    @classmethod
    def update_details(cls, accnumber, pin, field, new_value):
        userdata = [i for i in cls.data if i['accountNo'] == accnumber and i['pin'] == pin]
        if not userdata:
            return None, "Invalid account number or pin"
        if field not in ["name", "email", "pin"]:
            return None, "Invalid field"
        if field == "pin" and len(str(new_value)) != 4:
            return None, "Pin should be 4 digits"
        userdata[0][field] = new_value
        cls.__update()
        return userdata[0], f"{field} updated successfully"

    @classmethod
    def delete_account(cls, accnumber, pin):
        userdata = [i for i in cls.data if i['accountNo'] == accnumber and i['pin'] == pin]
        if not userdata:
            return None, "Invalid account number or pin"
        cls.data.remove(userdata[0])
        cls.__update()
        return None, "Account deleted successfully"
