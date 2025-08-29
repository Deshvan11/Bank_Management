import streamlit as st
from bank import Bank

st.set_page_config(page_title="Bank Management System", layout="centered")

st.title("🏦 Bank Management System")

menu = ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Details", "Delete Account"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=1)
    email = st.text_input("Enter your email")
    pin = st.text_input("Enter 4 digit PIN", type="password")

    if st.button("Create"):
        if not pin.isdigit() or len(pin) != 4:
            st.error("PIN must be 4 digits")
        else:
            account, msg = Bank.create_account(name, age, email, int(pin))
            if account:
                st.success(msg)
                st.json(account)
            else:
                st.error(msg)

elif choice == "Deposit Money":
    st.subheader("Deposit")
    accnumber = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    amount = st.number_input("Enter amount", min_value=1)

    if st.button("Deposit"):
        _, msg = Bank.deposit(accnumber, int(pin), amount)
        st.info(msg)

elif choice == "Withdraw Money":
    st.subheader("Withdraw")
    accnumber = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    amount = st.number_input("Enter amount", min_value=1)

    if st.button("Withdraw"):
        _, msg = Bank.withdraw(accnumber, int(pin), amount)
        st.info(msg)

elif choice == "Show Details":
    st.subheader("Account Details")
    accnumber = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Show"):
        details, msg = Bank.show_details(accnumber, int(pin))
        if details:
            st.success(msg)
            st.json(details)
        else:
            st.error(msg)

elif choice == "Update Details":
    st.subheader("Update Account Info")
    accnumber = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    field = st.selectbox("Select field", ["name", "email", "pin"])
    new_value = st.text_input(f"Enter new {field}")

    if st.button("Update"):
        if field == "pin" and (not new_value.isdigit() or len(new_value) != 4):
            st.error("PIN must be 4 digits")
        else:
            _, msg = Bank.update_details(accnumber, int(pin), field, new_value if field != "pin" else int(new_value))
            st.info(msg)

elif choice == "Delete Account":
    st.subheader("Delete Account")
    accnumber = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Delete"):
        _, msg = Bank.delete_account(accnumber, int(pin))
        st.warning(msg)
