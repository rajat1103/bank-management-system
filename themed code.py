import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from ttkthemes import ThemedStyle

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rajat@2003",
        database="bank_db"
    )

# Create account function
def create_account():
    acno, name, acc_type, balance = entry_acno.get(), entry_name.get(), entry_type.get().upper(), entry_balance.get()
    if not (acno and name and acc_type and balance):
        messagebox.showerror("Error", "Please fill all fields!")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO accounts (acno, name, type, balance) VALUES (%s, %s, %s, %s)",
                       (int(acno), name, acc_type, int(balance)))
        conn.commit()
        messagebox.showinfo("Success", "Account Created Successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Account number already exists.")
    finally:
        conn.close()

# Display balance function
def show_balance():
    acno = entry_acno.get()
    if not acno:
        messagebox.showerror("Error", "Please enter an account number!")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, type, balance FROM accounts WHERE acno = %s", (int(acno),))
    result = cursor.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Account Details", f"Name: {result[0]}\nType: {result[1]}\nBalance: ₹{result[2]}")
    else:
        messagebox.showerror("Error", "Account not found.")

# Deposit function
def deposit_amount():
    acno, amount = entry_acno.get(), entry_balance.get()
    if not (acno and amount):
        messagebox.showerror("Error", "Please enter account number and amount!")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE acno = %s", (int(amount), int(acno)))
    if cursor.rowcount:
        conn.commit()
        messagebox.showinfo("Success", "Amount Deposited Successfully!")
    else:
        messagebox.showerror("Error", "Account not found.")
    conn.close()

# Withdraw function
def withdraw_amount():
    acno, amount = entry_acno.get(), entry_balance.get()
    if not (acno and amount):
        messagebox.showerror("Error", "Please enter account number and amount!")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE acno = %s", (int(acno),))
    result = cursor.fetchone()

    if result and result[0] >= int(amount):
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE acno = %s", (int(amount), int(acno)))
        conn.commit()
        messagebox.showinfo("Success", "Amount Withdrawn Successfully!")
    else:
        messagebox.showerror("Error", "Insufficient Balance or Account not found.")
    conn.close()

# GUI Setup
root = tk.Tk()
root.title("Bank Management System")
root.geometry("500x500")
root.configure(bg="#2C3E50")  # Dark mode background

# Apply themed styling
style = ThemedStyle(root)
style.set_theme("plastik")

frame = ttk.Frame(root, padding=20)
frame.pack(pady=15)

ttk.Label(frame, text="Account No.", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
entry_acno = ttk.Entry(frame)
entry_acno.grid(row=0, column=1)

ttk.Label(frame, text="Name", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
entry_name = ttk.Entry(frame)
entry_name.grid(row=1, column=1)

ttk.Label(frame, text="Type (S/C)", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5)
entry_type = ttk.Entry(frame)
entry_type.grid(row=2, column=1)

ttk.Label(frame, text="Amount", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=5, pady=5)
entry_balance = ttk.Entry(frame)
entry_balance.grid(row=3, column=1)

# Buttons Frame with modern colors
button_frame = ttk.Frame(root, padding=10)
button_frame.pack()

style.configure("TButton", font=("Arial", 12), padding=5)

ttk.Button(button_frame, text="Create Account", command=create_account).pack(fill="x", pady=5)
ttk.Button(button_frame, text="Check Balance", command=show_balance).pack(fill="x", pady=5)
ttk.Button(button_frame, text="Deposit", command=deposit_amount).pack(fill="x", pady=5)
ttk.Button(button_frame, text="Withdraw", command=withdraw_amount).pack(fill="x", pady=5)

root.mainloop()