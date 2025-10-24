#include <iostream>
#include <iomanip>
#include <mysqlx/xdevapi.h>
#include <cstring>
using namespace std;
using namespace mysqlx;

class Bank_account {
    int acno;
    char name[50];
    int deposit;
    char type;

public:
    void create_account();
    void show_account() const;
    void modify();
    void dep(int);
    void draw(int);
    void report() const;
    int retacno() const;
    int retdeposit() const;
    char rettype() const;
};

// Create a new account
void Bank_account::create_account() {
    system("CLS");
    cout << "\n\t\t\tEnter the Account No. : ";
    cin >> acno;
    cout << "\n\n\t\t\tEnter the Name of the Account holder : ";
    cin.ignore();
    cin.getline(name, 50);
    cout << "\n\t\t\tEnter Type of the Account (C/S) : ";
    cin >> type;
    type = toupper(type);
    cout << "\n\t\t\tEnter The Initial amount : ";
    cin >> deposit;
    cout << "\n\n\t\t\tAccount Created..";
}

// Display account details
void Bank_account::show_account() const {
    cout << "\n\t\t\tAccount No. : " << acno;
    cout << "\n\t\t\tAccount Holder Name : " << name;
    cout << "\n\t\t\tType of Account : " << type;
    cout << "\n\t\t\tBalance amount : " << deposit;
}

// Modify account details
void Bank_account::modify() {
    cout << "\n\t\t\tAccount No. : " << acno;
    cout << "\n\t\t\tModify Account Holder Name : ";
    cin.ignore();
    cin.getline(name, 50);
    cout << "\n\t\t\tModify Type of Account : ";
    cin >> type;
    type = toupper(type);
    cout << "\n\t\t\tModify Balance amount : ";
    cin >> deposit;
}

// Deposit amount
void Bank_account::dep(int x) {
    deposit += x;
}

// Withdraw amount
void Bank_account::draw(int x) {
    deposit -= x;
}

// Display account report (for list of all accounts)
void Bank_account::report() const {
    cout << acno << setw(10) << " " << name << setw(10) << " " << type << setw(6) << deposit << endl;
}

// Get account number
int Bank_account::retacno() const {
    return acno;
}

// Get account balance
int Bank_account::retdeposit() const {
    return deposit;
}

// Get account type
char Bank_account::rettype() const {
    return type;
}

// Write new account to MySQL database
void write_account() {
    Bank_account ac;
    ac.create_account();

    try {
        Session session("localhost", 33060, "root", "Rajat@2003");
        Schema db = session.getSchema("BANKK");
        Table table = db.getTable("accounts");

        table.insert("acno", "name", "deposit", "type")
            .values(ac.retacno(), ac.name, ac.retdeposit(), string(1, ac.rettype()))
            .execute();

        session.close();
        cout << "\n\n\t\t\tAccount Created.. (in DB)";
    } catch (const mysqlx::Error &err) {
        cerr << "MySQL Error: " << err.what() << endl;
    }
}

// Display specific account details
void display_sp(int n) {
    try {
        Session session("localhost", 33060, "root", "Rajat@2003");
        Schema db = session.getSchema("BANKK");
        Table table = db.getTable("accounts");

        RowResult res = table.select("acno", "name", "type", "deposit")
                             .where("acno = :acno")
                             .bind("acno", n)
                             .execute();

        if (res.count() == 0) {
            cout << "\n\n\t\t\tAccount number does not exist";
        } else {
            Row row = res.fetchOne();
            cout << "\n\t\t\tAccount No. : " << row[0] << endl;
            cout << "\t\t\tName        : " << row[1].get<string>() << endl;
            cout << "\t\t\tType        : " << row[2].get<string>() << endl;
            cout << "\t\t\tBalance     : " << row[3] << endl;
        }

        session.close();
    } catch (const mysqlx::Error &err) {
        cerr << "Error: " << err.what() << endl;
    }
}

// Modify account details
void modify_account(int n) {
    try {
        Session session("localhost", 33060, "root", "Rajat@2003");
        Schema db = session.getSchema("BANKK");
        Table table = db.getTable("accounts");

        RowResult res = table.select("acno", "name", "type", "deposit")
                             .where("acno = :acno")
                             .bind("acno", n)
                             .execute();

        if (res.count() == 0) {
            cout << "\n\n\t\t\tAccount number does not exist";
        } else {
            Row row = res.fetchOne();
            cout << "\n\t\t\tAccount No. : " << row[0] << endl;
            cout << "\n\t\t\tModify Account Holder Name : ";
            cin.ignore();
            cin.getline(ac.name, 50);
            cout << "\n\t\t\tModify Type of Account : ";
            cin >> ac.type;
            cout << "\n\t\t\tModify Balance amount : ";
            cin >> ac.deposit;

            table.update()
                 .set("name", ac.name)
                 .set("type", string(1, ac.type))
                 .set("deposit", ac.retdeposit())
                 .where("acno = :acno")
                 .bind("acno", n)
                 .execute();
            session.close();
            cout << "\n\n\t\t\tRecord Updated";
        }
    } catch (const mysqlx::Error &err) {
        cerr << "Error: " << err.what() << endl;
    }
}

// Delete account
void delete_account(int n) {
    try {
        Session session("localhost", 33060, "root", "Rajat@2003");
        Schema db = session.getSchema("BANKK");
        Table table = db.getTable("accounts");

        table.remove().where("acno = :acno").bind("acno", n).execute();

        session.close();
        cout << "\n\nRecord Deleted ..";
    } catch (const mysqlx::Error &err) {
        cerr << "Error: " << err.what() << endl;
    }
}

// Display all accounts
void display_all() {
    try {
        Session session("localhost", 33060, "root", "Rajat@2003");
        Schema db = session.getSchema("BANKK");
        Table table = db.getTable("accounts");

        RowResult res = table.select("acno", "name", "type", "deposit").execute();

        cout << "\n\n\t\tACCOUNT HOLDER LIST\n\n";
        cout << "====================================================\n";
        cout << "A/c no. NAME Type Balance\n";
        cout << "====================================================\n";
        while (res.next()) {
            cout << res[0] << setw(10) << res[1].get<string>() << setw(10) << res[2].get<string>() << setw(6) << res[3] << endl;
        }

        session.close();
    } catch (const mysqlx::Error &err) {
        cerr << "Error: " << err.what() << endl;
    }
}

// Main function with menu
int main() {
    char ch;
    int num;
    do {
        system("CLS");
        cout << "\n\n\t\t\t\t======================\n";
        cout << "\t\t\t\tBANK MANAGEMENT SYSTEM";
        cout << "\n\t\t\t\t======================\n";
        cout << "\t\t\t\t ::MAIN MENU::\n";
        cout << "\n\t\t\t\t1. NEW ACCOUNT";
        cout << "\n\t\t\t\t2. DEPOSIT AMOUNT";
        cout << "\n\t\t\t\t3. WITHDRAW AMOUNT";
        cout << "\n\t\t\t\t4. BALANCE ENQUIRY";
        cout << "\n\t\t\t\t5. ALL ACCOUNT HOLDER LIST";
        cout << "\n\t\t\t\t6. CLOSE AN ACCOUNT";
        cout << "\n\t\t\t\t7. MODIFY AN ACCOUNT";
        cout << "\n\t\t\t\t8. EXIT";
        cout << "\n\n\t\t\t\tSelect Your Option (1-8): ";
        cin >> ch;
        switch (ch) {
            case '1':
                write_account();
                break;
            case '2':
                system("CLS");
                cout << "\n\n\t\t\tEnter The account No. : "; cin >> num;
                display_sp(num);
                break;
            case '3':
                system("CLS");
                cout << "\n\n\t\t\tEnter The account No. : "; cin >> num;
                display_sp(num);
                break;
            case '4':
                system("CLS");
                cout << "\n\n\t\t\tEnter The account No. : "; cin >> num;
                display_sp(num);
                break;
            case '5':
                display_all();
                break;
            case '6':
                system("CLS");
                cout << "\n\n\t\t\tEnter The account No. : "; cin >> num;
                delete_account(num);
                break;
            case '7':
                system("CLS");
                cout << "\n\n\t\t\tEnter The account No. : "; cin >> num;
                modify_account(num);
                break;
            case '8':
                system("CLS");
                cout << "\n\n\t\t\tBrought To You By code-projects.org";
                break;
            default:
                cout << "\a";
        }
        cin.ignore();
        cin.get();
    } while (ch != '8');
    return 0;
}
