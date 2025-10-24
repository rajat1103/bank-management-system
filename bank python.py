import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rajat@2003",  # your password
        database="bank_db"
    )

# Create account
def create_account():
    acno = int(entry_acno.get())
    name = entry_name.get()
    acc_type = entry_type.get().upper()
    balance = int(entry_balance.get())

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO accounts (acno, name, type, balance) VALUES (%s, %s, %s, %s)",
                       (acno, name, acc_type, balance))
        conn.commit()
        messagebox.showinfo("Success", "Account Created Successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Account number already exists.")
    finally:
        conn.close()

# Display balance
def show_balance():
    acno = int(entry_acno.get())
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, type, balance FROM accounts WHERE acno = %s", (acno,))
    result = cursor.fetchone()
    conn.close()
    if result:
        name, acc_type, balance = result
        messagebox.showinfo("Account Details", f"Name: {name}\nType: {acc_type}\nBalance: ₹{balance}")
    else:
        messagebox.showerror("Error", "Account not found.")

# Deposit
def deposit_amount():
    acno = int(entry_acno.get())
    amount = int(entry_balance.get())

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE acno = %s", (amount, acno))
    if cursor.rowcount:
        conn.commit()
        messagebox.showinfo("Success", "Amount Deposited Successfully!")
    else:
        messagebox.showerror("Error", "Account not found.")
    conn.close()

# Withdraw
def withdraw_amount():
    acno = int(entry_acno.get())
    amount = int(entry_balance.get())

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE acno = %s", (acno,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        if balance >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE acno = %s", (amount, acno))
            conn.commit()
            messagebox.showinfo("Success", "Amount Withdrawn Successfully!")
        else:
            messagebox.showwarning("Warning", "Insufficient Balance!")
    else:
        messagebox.showerror("Error", "Account not found.")
    conn.close()

# Delete account
def delete_account():
    acno = int(entry_acno.get())
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE acno = %s", (acno,))
    if cursor.rowcount:
        conn.commit()
        messagebox.showinfo("Success", "Account Deleted Successfully!")
    else:
        messagebox.showerror("Error", "Account not found.")
    conn.close()

# Modify account
def modify_account():
    acno = int(entry_acno.get())
    name = entry_name.get()
    acc_type = entry_type.get().upper()
    balance = int(entry_balance.get())

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET name = %s, type = %s, balance = %s WHERE acno = %s",
                   (name, acc_type, balance, acno))
    if cursor.rowcount:
        conn.commit()
        messagebox.showinfo("Success", "Account Modified Successfully!")
    else:
        messagebox.showerror("Error", "Account not found.")
    conn.close()

# GUI
root = tk.Tk()
root.title("Bank Management System")
root.geometry("400x400")

tk.Label(root, text="Account No.").pack()
entry_acno = tk.Entry(root)
entry_acno.pack()

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Type (S/C)").pack()
entry_type = tk.Entry(root)
entry_type.pack()

tk.Label(root, text="Amount").pack()
entry_balance = tk.Entry(root)
entry_balance.pack()

tk.Button(root, text="Create Account", command=create_account).pack(pady=5)
tk.Button(root, text="Check Balance", command=show_balance).pack(pady=5)
tk.Button(root, text="Deposit", command=deposit_amount).pack(pady=5)
tk.Button(root, text="Withdraw", command=withdraw_amount).pack(pady=5)
tk.Button(root, text="Modify Account", command=modify_account).pack(pady=5)
tk.Button(root, text="Delete Account", command=delete_account).pack(pady=5)

root.mainloop()
