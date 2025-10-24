#include <iostream>
#include <iomanip>
#include <string>
#include <mysql/mysql.h>
using namespace std;

class BankAccount {
    int acno;
    string name;
    int deposit;
    char type;

public:
    void create_account();
    void show_account() const;
    void modify();
    void dep(int);
    void draw(int);
    int get_acno() const { return acno; }
    int get_deposit() const { return deposit; }
    char get_type() const { return type; }
    string get_name() const { return name; }
};

void BankAccount::create_account() {
    system("CLS");
    cout << "\n\t\t\tEnter the Account No. : ";
    cin >> acno;
    cout << "\n\n\t\t\tEnter the Name of the Account holder : ";
    cin.ignore();
    getline(cin, name);
    cout << "\n\t\t\tEnter Type of the Account (C/S) : ";
    cin >> type;
    type = toupper(type);
    cout << "\n\t\t\tEnter The Initial amount : ";
    cin >> deposit;
    cout << "\n\n\t\t\tAccount Created..";
}

void BankAccount::show_account() const {
    cout << "\n\t\t\tAccount No. : " << acno;
    cout << "\n\t\t\tAccount Holder Name : " << name;
    cout << "\n\t\t\tType of Account : " << type;
    cout << "\n\t\t\tBalance amount : " << deposit;
}

void BankAccount::modify() {
    cout << "\n\t\t\tModify Account Holder Name : ";
    cin.ignore();
    getline(cin, name);
    cout << "\n\t\t\tModify Type of Account : ";
    cin >> type;
    type = toupper(type);
    cout << "\n\t\t\tModify Balance amount : ";
    cin >> deposit;
}

void BankAccount::dep(int x) { deposit += x; }
void BankAccount::draw(int x) { deposit -= x; }

MYSQL* connect_db() {
    MYSQL* conn = mysql_init(NULL);
    if (!mysql_real_connect(conn, "localhost", "root", "Rajat@2003", "bankdb", 3306, NULL, 0)) {
        cerr << "MySQL connection failed: " << mysql_error(conn) << endl;
        exit(1);
    }
    return conn;
}

void write_account(MYSQL* conn) {
    BankAccount ac;
    ac.create_account();

    string query = "INSERT INTO accounts (acno, name, deposit, type) VALUES (" +
                   to_string(ac.get_acno()) + ", '" + ac.get_name() + "', " +
                   to_string(ac.get_deposit()) + ", '" + ac.get_type() + "')";

    if (mysql_query(conn, query.c_str()) != 0) {
        cerr << "Insert failed: " << mysql_error(conn) << endl;
    } else {
        cout << "\n\n\t\t\tAccount Created.. (in DB)";
    }
}

void display_sp(MYSQL* conn, int n) {
    string query = "SELECT * FROM accounts WHERE acno = " + to_string(n);
    if (mysql_query(conn, query.c_str()) == 0) {
        MYSQL_RES* res = mysql_store_result(conn);
        if (mysql_num_rows(res) == 0) {
            cout << "\n\n\t\t\tAccount number does not exist";
        } else {
            MYSQL_ROW row = mysql_fetch_row(res);
            cout << "\n\t\t\tAccount No. : " << row[0];
            cout << "\n\t\t\tName        : " << row[1];
            cout << "\n\t\t\tType        : " << row[3];
            cout << "\n\t\t\tBalance     : " << row[2];
        }
        mysql_free_result(res);
    } else {
        cerr << "Query failed: " << mysql_error(conn) << endl;
    }
}

void delete_account(MYSQL* conn, int n) {
    string query = "DELETE FROM accounts WHERE acno = " + to_string(n);
    if (mysql_query(conn, query.c_str()) == 0 && mysql_affected_rows(conn) > 0)
        cout << "\n\nRecord Deleted ..";
    else
        cout << "\n\nRecord Not Found ..";
}

void modify_account(MYSQL* conn, int n) {
    string select = "SELECT * FROM accounts WHERE acno = " + to_string(n);
    if (mysql_query(conn, select.c_str()) == 0) {
        MYSQL_RES* res = mysql_store_result(conn);
        if (mysql_num_rows(res) == 0) {
            cout << "\n\nRecord Not Found";
            mysql_free_result(res);
            return;
        }
        mysql_free_result(res);
    } else {
        cerr << "Select failed: " << mysql_error(conn) << endl;
        return;
    }

    BankAccount ac;
    ac.modify();

    string query = "UPDATE accounts SET name='" + ac.get_name() + "', type='" +
                   ac.get_type() + "', deposit=" + to_string(ac.get_deposit()) +
                   " WHERE acno=" + to_string(n);

    if (mysql_query(conn, query.c_str()) != 0) {
        cerr << "Update failed: " << mysql_error(conn) << endl;
    } else {
        cout << "\n\nRecord Updated";
    }
}

void display_all(MYSQL* conn) {
    string query = "SELECT * FROM accounts";
    if (mysql_query(conn, query.c_str()) == 0) {
        MYSQL_RES* res = mysql_store_result(conn);
        MYSQL_ROW row;

        cout << "\n\n\t\tACCOUNT HOLDER LIST\n\n";
        cout << "====================================================\n";
        cout << "A/c no.\tNAME\tType\tBalance\n";
        cout << "====================================================\n";

        while ((row = mysql_fetch_row(res))) {
            cout << row[0] << "\t" << row[1] << "\t" << row[3] << "\t" << row[2] << endl;
        }
        mysql_free_result(res);
    } else {
        cerr << "Query failed: " << mysql_error(conn) << endl;
    }
}

void deposit_withdraw(MYSQL* conn, int n, int option) {
    string select = "SELECT deposit FROM accounts WHERE acno = " + to_string(n);
    if (mysql_query(conn, select.c_str()) == 0) {
        MYSQL_RES* res = mysql_store_result(conn);
        if (mysql_num_rows(res) == 0) {
            cout << "\n\nRecord Not Found";
            mysql_free_result(res);
            return;
        }

        MYSQL_ROW row = mysql_fetch_row(res);
        int current = stoi(row[0]);
        mysql_free_result(res);

        int amt;
        if (option == 1) {
            cout << "\n\n\t\t\tEnter The amount to be deposited: ";
            cin >> amt;
            current += amt;
        } else {
            cout << "\n\n\t\t\tEnter The amount to be withdraw: ";
            cin >> amt;
            if (current - amt < 0) {
                cout << "\n\nInsufficient balance";
                return;
            }
            current -= amt;
        }

        string update = "UPDATE accounts SET deposit=" + to_string(current) +
                         " WHERE acno=" + to_string(n);
        if (mysql_query(conn, update.c_str()) == 0)
            cout << "\n\nRecord Updated";
        else
            cerr << "Update failed: " << mysql_error(conn) << endl;
    }
}

int main() {
    MYSQL* conn = connect_db();

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
            case '1': write_account(conn); break;
            case '2': cout << "\n\t\t\tEnter The account No. : "; cin >> num; deposit_withdraw(conn, num, 1); break;
            case '3': cout << "\n\t\t\tEnter The account No. : "; cin >> num; deposit_withdraw(conn, num, 2); break;
            case '4': cout << "\n\t\t\tEnter The account No. : "; cin >> num; display_sp(conn, num); break;
            case '5': display_all(conn); break;
            case '6': cout << "\n\t\t\tEnter The account No. : "; cin >> num; delete_account(conn, num); break;
            case '7': cout << "\n\t\t\tEnter The account No. : "; cin >> num; modify_account(conn, num); break;
            case '8': system("CLS"); cout << "\n\n\t\t\tBrought To You By code-projects.org"; break;
            default: cout << "\a";
        }
        cin.ignore();
        cin.get();
    } while (ch != '8');

    mysql_close(conn);
    return 0;
}
