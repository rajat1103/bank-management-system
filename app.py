import streamlit as st
import mysql.connector

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rajat@2003",
        database="bank_db"
    )

st.set_page_config(page_title="Bank Management System", page_icon="🏦", layout="centered")

st.title("🏦 Bank Management System")

menu = ["Create Account", "Check Balance", "Deposit", "Withdraw", "Modify Account", "Delete Account"]
choice = st.sidebar.selectbox("Select Action", menu)

# Create account
if choice == "Create Account":
    st.subheader("Create New Account")
    acno = st.number_input("Account Number", min_value=1, step=1)
    pan = st.text_input("PAN Card No.")
    name = st.text_input("Name")
    acc_type = st.selectbox("Account Type", ["S", "C"])
    balance = st.number_input("Opening Balance", min_value=0, step=100)

    if st.button("Create Account"):
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO accounts (acno, pan, name, type, balance) VALUES (%s, %s, %s, %s, %s)",
                           (acno, pan, name, acc_type, balance))
            conn.commit()
            st.success("✅ Account Created Successfully!")
        except mysql.connector.IntegrityError:
            st.error("❌ Account number already exists.")
        finally:
            conn.close()

# Check balance
elif choice == "Check Balance":
    st.subheader("Check Balance")
    acno = st.number_input("Enter Account Number", min_value=1, step=1)
    if st.button("Show Balance"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, type, balance FROM accounts WHERE acno = %s", (acno,))
        result = cursor.fetchone()
        conn.close()
        if result:
            st.info(f"**Name:** {result[0]}\n\n**Type:** {result[1]}\n\n**Balance:** ₹{result[2]}")
        else:
            st.error("Account not found.")

# Deposit
elif choice == "Deposit":
    st.subheader("Deposit Amount")
    acno = st.number_input("Account Number", min_value=1, step=1)
    amount = st.number_input("Amount", min_value=1, step=100)
    if st.button("Deposit"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE acno = %s", (amount, acno))
        if cursor.rowcount:
            conn.commit()
            st.success("✅ Amount Deposited Successfully!")
        else:
            st.error("Account not found.")
        conn.close()

# Withdraw
elif choice == "Withdraw":
    st.subheader("Withdraw Amount")
    acno = st.number_input("Account Number", min_value=1, step=1)
    amount = st.number_input("Amount", min_value=1, step=100)
    if st.button("Withdraw"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE acno = %s", (acno,))
        result = cursor.fetchone()
        if result and result[0] >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE acno = %s", (amount, acno))
            conn.commit()
            st.success("✅ Amount Withdrawn Successfully!")
        else:
            st.error("❌ Insufficient Balance or Account not found.")
        conn.close()

# Modify account
elif choice == "Modify Account":
    st.subheader("Modify Account Details")
    acno = st.number_input("Account Number", min_value=1, step=1)
    pan = st.text_input("New PAN")
    name = st.text_input("New Name")
    acc_type = st.selectbox("New Account Type", ["S", "C"])
    balance = st.number_input("New Balance", min_value=0, step=100)
    if st.button("Modify"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET pan=%s, name=%s, type=%s, balance=%s WHERE acno=%s",
                       (pan, name, acc_type, balance, acno))
        if cursor.rowcount:
            conn.commit()
            st.success("✅ Account Modified Successfully!")
        else:
            st.error("❌ Account not found.")
        conn.close()

# Delete account
elif choice == "Delete Account":
    st.subheader("Delete Account")
    acno = st.number_input("Account Number", min_value=1, step=1)
    if st.button("Delete"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE acno=%s", (acno,))
        if cursor.rowcount:
            conn.commit()
            st.success("✅ Account Deleted Successfully!")
        else:
            st.error("❌ Account not found.")
        conn.close()
