import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk  # For handling images

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
    acno = entry_acno.get()
    pan = entry_pan.get()
    name = entry_name.get()
    acc_type = entry_type.get().upper()
    balance = entry_balance.get()
    
    if not (acno and pan and name and acc_type and balance):
        messagebox.showerror("Error", "Please fill all fields!")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO accounts (acno, pan, name, type, balance) VALUES (%s, %s, %s, %s, %s)",
                       (int(acno), pan, name, acc_type, int(balance)))
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
    pan = entry_pan.get()
    name = entry_name.get()
    acc_type = entry_type.get().upper()
    balance = int(entry_balance.get())

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET pan = %s, name = %s, type = %s, balance = %s WHERE acno = %s",
                   (pan, name, acc_type, balance, acno))
    if cursor.rowcount:
        conn.commit()
        messagebox.showinfo("Success", "Account Modified Successfully!")
    else:
        messagebox.showerror("Error", "Account not found.")
    conn.close()


# GUI Setup
root = tk.Tk()
root.title("Bank Management System")
root.geometry("500x500")

# Load the watermark image
try:
    wallet_img = Image.open(r"C:\Users\HP\BANK MANAGEMENT SYSTEM\wallet.png")
    wallet_img = wallet_img.resize((500, 500))  # Adjust size to fit the window
    wallet_img = wallet_img.convert("RGBA")  # Make sure it's an RGBA image
    alpha = 120  # Control transparency (255 is fully visible, lower is dimmed)
    wallet_img.putalpha(alpha)
    wallet_bg = ImageTk.PhotoImage(wallet_img)

    # Add the watermark as a background label
    bg_label = tk.Label(root, image=wallet_bg)
    bg_label.place(relwidth=1, relheight=1)  # Cover entire window
except Exception as e:
    print(f"Error loading wallet.png: {e}")

# Apply themed styling
style = ThemedStyle(root)
style.set_theme("radiance")

frame = ttk.Frame(root, padding=20)
frame.pack(pady=15)

ttk.Label(frame, text="Account No.", font=("Times New Roman", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
entry_acno = ttk.Entry(frame)
entry_acno.grid(row=0, column=1)

ttk.Label(frame, text="PAN Card No.", font=("Times New Roman", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
entry_pan = ttk.Entry(frame)
entry_pan.grid(row=1, column=1)

ttk.Label(frame, text="Name", font=("Times New Roman", 12, "bold")).grid(row=2, column=0, padx=5, pady=5)
entry_name = ttk.Entry(frame)
entry_name.grid(row=2, column=1)

ttk.Label(frame, text="Type (S/C)", font=("Times New Roman", 12, "bold")).grid(row=3, column=0, padx=5, pady=5)
entry_type = ttk.Entry(frame)
entry_type.grid(row=3, column=1)

ttk.Label(frame, text="Amount", font=("Times New Roman", 12, "bold")).grid(row=4, column=0, padx=5, pady=5)
entry_balance = ttk.Entry(frame)
entry_balance.grid(row=4, column=1)

# Buttons Frame
button_frame = ttk.Frame(root, padding=10)
button_frame.pack()

style.configure("TButton", font=("Times New Roman", 12), padding=5, background="#FFC107", foreground="black")

ttk.Button(button_frame, text="Create Account", command=create_account).pack(fill="x", pady=5)
ttk.Button(button_frame, text="Check Balance", command=show_balance).pack(fill="x", pady=5)
ttk.Button(button_frame, text="Deposit", command=deposit_amount).pack(fill="x", pady=5)
ttk.Button(button_frame, text="Withdraw", command=withdraw_amount).pack(fill="x", pady=5)
ttk.Button(button_frame, text="Modify Account", command=modify_account).pack(fill="x", pady=5)
ttk.Button(button_frame, text="Delete Account", command=delete_account).pack(fill="x", pady=5)

root.mainloop()
