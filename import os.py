import os
import pickle

class BankAccount:
    def __init__(self):
        self.acno = 0
        self.name = ""
        self.deposit = 0
        self.type = ""

    def create_account(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.acno = int(input("\n\t\t\tEnter the Account No. : "))
        self.name = input("\n\n\t\t\tEnter the Name of the Account holder : ")
        self.type = input("\n\t\t\tEnter Type of the Account (C/S) : ").upper()
        self.deposit = int(input("\n\t\t\tEnter The Initial amount : "))
        print("\n\n\t\t\tAccount Created..")

    def show_account(self):
        print("\n\t\t\tAccount No. :", self.acno)
        print("\t\t\tAccount Holder Name :", self.name)
        print("\t\t\tType of Account :", self.type)
        print("\t\t\tBalance amount :", self.deposit)

    def modify(self):
        print("\n\t\t\tModify Account Holder Name : ")
        self.name = input()
        print("\t\t\tModify Type of Account : ")
        self.type = input().upper()
        print("\t\t\tModify Balance amount : ")
        self.deposit = int(input())

    def dep(self, x):
        self.deposit += x

    def draw(self, x):
        self.deposit -= x

    def report(self):
        print(f"{self.acno:<10}{self.name:<15}{self.type:<6}{self.deposit:<10}")

    def retacno(self):
        return self.acno

    def retdeposit(self):
        return self.deposit

    def rettype(self):
        return self.type

def write_account():
    ac = BankAccount()
    ac.create_account()
    with open("account.dat", "ab") as f:
        pickle.dump(ac, f)

def display_sp(n):
    found = False
    try:
        with open("account.dat", "rb") as f:
            while True:
                ac = pickle.load(f)
                if ac.retacno() == n:
                    print("\n\t\t\tBALANCE DETAILS\n")
                    ac.show_account()
                    found = True
                    break
    except (EOFError, FileNotFoundError):
        pass
    if not found:
        print("\n\n\t\t\tAccount number does not exist")

def modify_account(n):
    found = False
    accounts = []
    try:
        with open("account.dat", "rb") as f:
            while True:
                ac = pickle.load(f)
                if ac.retacno() == n:
                    print("\n\t\t\tCurrent Account Details:")
                    ac.show_account()
                    print("\n\t\t\tEnter The New Details of account")
                    ac.modify()
                    found = True
                accounts.append(ac)
    except EOFError:
        pass

    with open("account.dat", "wb") as f:
        for ac in accounts:
            pickle.dump(ac, f)

    if found:
        print("\n\n\t\t\tRecord Updated")
    else:
        print("\n\n\t\t\tRecord Not Found ")

def delete_account(n):
    accounts = []
    found = False
    try:
        with open("account.dat", "rb") as f:
            while True:
                ac = pickle.load(f)
                if ac.retacno() != n:
                    accounts.append(ac)
                else:
                    found = True
    except EOFError:
        pass

    with open("account.dat", "wb") as f:
        for ac in accounts:
            pickle.dump(ac, f)

    if found:
        print("\n\n\t\t\tRecord Deleted ..")
    else:
        print("\n\n\t\t\tAccount number not found")

def display_all():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\n\t\tACCOUNT HOLDER LIST\n")
    print("====================================================")
    print("A/c no.    NAME           Type  Balance")
    print("====================================================")
    try:
        with open("account.dat", "rb") as f:
            while True:
                ac = pickle.load(f)
                ac.report()
    except EOFError:
        pass
    except FileNotFoundError:
        print("File could not be open !! Press any Key...")

def deposit_withdraw(n, option):
    found = False
    accounts = []
    try:
        with open("account.dat", "rb") as f:
            while True:
                ac = pickle.load(f)
                if ac.retacno() == n:
                    ac.show_account()
                    if option == 1:
                        amt = int(input("\n\n\t\t\tEnter The amount to be deposited: "))
                        ac.dep(amt)
                    elif option == 2:
                        amt = int(input("\n\n\t\t\tEnter The amount to withdraw: "))
                        if ac.retdeposit() - amt < 0:
                            print("Insufficient balance")
                        else:
                            ac.draw(amt)
                    print("\n\n\t\t\tRecord Updated")
                    found = True
                accounts.append(ac)
    except EOFError:
        pass
    except FileNotFoundError:
        print("File could not be open !! Press any Key...")
        return

    with open("account.dat", "wb") as f:
        for ac in accounts:
            pickle.dump(ac, f)

    if not found:
        print("\n\n\t\t\tRecord Not Found ")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\n\t\t\t\t======================")
        print("\t\t\t\tBANK MANAGEMENT SYSTEM")
        print("\t\t\t\t======================")
        print("\t\t\t\t ::MAIN MENU::")
        print("\n\t\t\t\t1. NEW ACCOUNT")
        print("\t\t\t\t2. DEPOSIT AMOUNT")
        print("\t\t\t\t3. WITHDRAW AMOUNT")
        print("\t\t\t\t4. BALANCE ENQUIRY")
        print("\t\t\t\t5. ALL ACCOUNT HOLDER LIST")
        print("\t\t\t\t6. CLOSE AN ACCOUNT")
        print("\t\t\t\t7. MODIFY AN ACCOUNT")
        print("\t\t\t\t8. EXIT")
        ch = input("\n\n\t\t\t\tSelect Your Option (1-8): ")

        if ch == '1':
            write_account()
        elif ch == '2':
            num = int(input("\n\n\t\t\tEnter The account No. : "))
            deposit_withdraw(num, 1)
        elif ch == '3':
            num = int(input("\n\n\t\t\tEnter The account No. : "))
            deposit_withdraw(num, 2)
        elif ch == '4':
            num = int(input("\n\n\t\t\tEnter The account No. : "))
            display_sp(num)
        elif ch == '5':
            display_all()
        elif ch == '6':
            num = int(input("\n\n\t\t\tEnter The account No. : "))
            delete_account(num)
        elif ch == '7':
            num = int(input("\n\n\t\t\tEnter The account No. : "))
            modify_account(num)
        elif ch == '8':
            print("\n\n\t\t\tBrought To You By code-projects.org")
            break
        else:
            print("Invalid choice!")
        input("\n\nPress Enter to continue...")

if __name__ == "__main__":
    main()
