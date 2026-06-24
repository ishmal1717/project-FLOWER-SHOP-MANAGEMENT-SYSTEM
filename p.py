import sys
import sqlite3
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpinBox
)

from PyQt5.QtGui import QFont


DB = "flowershop.db"

# ─────────────────────────────
# DATABASE
# ─────────────────────────────
def db():
    return sqlite3.connect(DB)

def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def init_db():
    conn = db()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS flowers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        flower_type TEXT,
        color TEXT,
        stem REAL,
        price REAL,
        status TEXT,
        added_date TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        joined_date TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        customer TEXT,
        amount REAL,
        sale_date TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        qty INTEGER,
        price REAL,
        updated TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS bills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_no TEXT,
        customer TEXT,
        phone TEXT,
        total REAL,
        date TEXT
    )""")

    cur.execute("INSERT OR IGNORE INTO users(username,password) VALUES('admin','admin')")

    conn.commit()
    conn.close()


# ─────────────────────────────
# LOGIN
# ─────────────────────────────
class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌸 Blossom Flower Login 🌸")
        self.setFixedSize(400, 300)

        self.setStyleSheet("""
        QWidget {
            background-color: #fff0f6;
        }
        QLineEdit {
            padding: 10px;
            border: 2px solid #f8c8dc;
            border-radius: 10px;
        }
        QPushButton {
            background-color: #ff69b4;
            color: white;
            padding: 10px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #ff85c1;
        }
        """)

        layout = QVBoxLayout(self)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Login 🌸")
        btn.clicked.connect(self.login)

        layout.addWidget(self.user)
        layout.addWidget(self.passw)
        layout.addWidget(btn)

    def login(self):
        conn = db()
        cur = conn.cursor()

        u = cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (self.user.text(), self.passw.text())
        ).fetchone()

        conn.close()

        if u:
            self.d = Dashboard()
            self.d.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid login")


# ─────────────────────────────
# DASHBOARD
# ─────────────────────────────
class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌸 Blossom Flower Shop System 🌸")
        self.resize(1200, 800)

        self.setStyleSheet("""
        QMainWindow {
            background-color: #fff0f6;
        }
        QTabWidget::pane {
            border: 1px solid #f8c8dc;
            background: #fff5fa;
        }
        QTabBar::tab {
            background: #f8c8dc;
            padding: 10px;
            border-radius: 8px;
            margin: 2px;
        }
        QTabBar::tab:selected {
            background: #ff69b4;
            color: white;
        }
        QLineEdit {
            padding: 8px;
            border: 2px solid #f8c8dc;
            border-radius: 10px;
        }
        QPushButton {
            background-color: #ff69b4;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #ff85c1;
        }
        QTableWidget {
            background-color: white;
            border: 1px solid #f8c8dc;
        }
        """)

        tabs = QTabWidget()

        tabs.addTab(self.flowers_tab(), "🌸 Flowers")
        tabs.addTab(self.customers_tab(), "👤 Customers")
        tabs.addTab(self.sales_tab(), "💰 Sales")
        tabs.addTab(self.inventory_tab(), "📦 Inventory")
        tabs.addTab(self.billing_tab(), "🧾 Billing")

        self.setCentralWidget(tabs)

    # ───────── FLOWERS
    def flowers_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        self.f_name = QLineEdit(); self.f_name.setPlaceholderText("Flower Name")
        self.f_type = QLineEdit(); self.f_type.setPlaceholderText("Type")
        self.f_color = QLineEdit(); self.f_color.setPlaceholderText("Color")
        self.f_price = QLineEdit(); self.f_price.setPlaceholderText("Price")

        btn = QPushButton("🌸 Add Flower")
        btn.clicked.connect(self.add_flower)

        self.table_f = QTableWidget()

        layout.addWidget(self.f_name)
        layout.addWidget(self.f_type)
        layout.addWidget(self.f_color)
        layout.addWidget(self.f_price)
        layout.addWidget(btn)
        layout.addWidget(self.table_f)

        self.load_flowers()
        return w

    def add_flower(self):
        conn = db()
        cur = conn.cursor()

        cur.execute("""INSERT INTO flowers(name,flower_type,color,stem,price,status,added_date)
                       VALUES(?,?,?,?,?,'Available',?)""",
                    (self.f_name.text(),
                     self.f_type.text(),
                     self.f_color.text(),
                     0,
                     self.f_price.text(),
                     today()))

        conn.commit()
        conn.close()
        self.load_flowers()

    def load_flowers(self):
        conn = db()
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM flowers").fetchall()
        conn.close()

        self.table_f.setRowCount(len(rows))
        self.table_f.setColumnCount(6)

        for r, row in enumerate(rows):
            for c, val in enumerate(row[:6]):
                self.table_f.setItem(r, c, QTableWidgetItem(str(val)))

    # ───────── CUSTOMERS
    def customers_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        self.c_name = QLineEdit(); self.c_name.setPlaceholderText("Name")
        self.c_phone = QLineEdit(); self.c_phone.setPlaceholderText("Phone")

        btn = QPushButton("Add Customer")
        btn.clicked.connect(self.add_customer)

        self.table_c = QTableWidget()

        layout.addWidget(self.c_name)
        layout.addWidget(self.c_phone)
        layout.addWidget(btn)
        layout.addWidget(self.table_c)

        self.load_customers()
        return w

    def add_customer(self):
        conn = db()
        cur = conn.cursor()

        cur.execute("INSERT INTO customers(name,phone,joined_date) VALUES(?,?,?)",
                    (self.c_name.text(), self.c_phone.text(), today()))

        conn.commit()
        conn.close()
        self.load_customers()

    def load_customers(self):
        conn = db()
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM customers").fetchall()
        conn.close()

        self.table_c.setRowCount(len(rows))
        self.table_c.setColumnCount(3)

        for r, row in enumerate(rows):
            for c, val in enumerate(row[:3]):
                self.table_c.setItem(r, c, QTableWidgetItem(str(val)))

    # ───────── SALES
    def sales_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        self.s_item = QLineEdit(); self.s_item.setPlaceholderText("Item")
        self.s_cust = QLineEdit(); self.s_cust.setPlaceholderText("Customer")
        self.s_amt = QLineEdit(); self.s_amt.setPlaceholderText("Amount")

        btn = QPushButton("Add Sale")
        btn.clicked.connect(self.add_sale)

        self.table_s = QTableWidget()

        layout.addWidget(self.s_item)
        layout.addWidget(self.s_cust)
        layout.addWidget(self.s_amt)
        layout.addWidget(btn)
        layout.addWidget(self.table_s)

        self.load_sales()
        return w

    def add_sale(self):
        conn = db()
        cur = conn.cursor()

        cur.execute("INSERT INTO sales(item,customer,amount,sale_date) VALUES(?,?,?,?)",
                    (self.s_item.text(),
                     self.s_cust.text(),
                     self.s_amt.text(),
                     today()))

        conn.commit()
        conn.close()
        self.load_sales()

    def load_sales(self):
        conn = db()
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM sales").fetchall()
        conn.close()

        self.table_s.setRowCount(len(rows))
        self.table_s.setColumnCount(4)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table_s.setItem(r, c, QTableWidgetItem(str(val)))

    # ───────── INVENTORY
    def inventory_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        self.i_name = QLineEdit(); self.i_name.setPlaceholderText("Product")
        self.i_qty = QSpinBox()
        self.i_price = QLineEdit()

        btn = QPushButton("Add Stock")
        btn.clicked.connect(self.add_stock)

        self.table_i = QTableWidget()

        layout.addWidget(self.i_name)
        layout.addWidget(self.i_qty)
        layout.addWidget(self.i_price)
        layout.addWidget(btn)
        layout.addWidget(self.table_i)

        self.load_inventory()
        return w

    def add_stock(self):
        conn = db()
        cur = conn.cursor()

        cur.execute("INSERT INTO inventory(product,qty,price,updated) VALUES(?,?,?,?)",
                    (self.i_name.text(),
                     self.i_qty.value(),
                     self.i_price.text(),
                     today()))

        conn.commit()
        conn.close()
        self.load_inventory()

    def load_inventory(self):
        conn = db()
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM inventory").fetchall()
        conn.close()

        self.table_i.setRowCount(len(rows))
        self.table_i.setColumnCount(4)

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table_i.setItem(r, c, QTableWidgetItem(str(val)))

    # ───────── BILLING
    def billing_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        self.b_cust = QLineEdit(); self.b_cust.setPlaceholderText("Customer")
        self.b_phone = QLineEdit(); self.b_phone.setPlaceholderText("Phone")
        self.b_amt = QLineEdit(); self.b_amt.setPlaceholderText("Total")

        btn = QPushButton("Save Bill")
        btn.clicked.connect(self.save_bill)

        self.table_b = QTableWidget()

        layout.addWidget(self.b_cust)
        layout.addWidget(self.b_phone)
        layout.addWidget(self.b_amt)
        layout.addWidget(btn)
        layout.addWidget(self.table_b)

        self.load_bills()
        return w

    def save_bill(self):
        conn = db()
        cur = conn.cursor()

        cur.execute("""INSERT INTO bills(bill_no,customer,phone,total,date)
                       VALUES(?,?,?,?,?)""",
                    (f"B-{datetime.now().timestamp()}",
                     self.b_cust.text(),
                     self.b_phone.text(),
                     self.b_amt.text(),
                     today()))

        conn.commit()
        conn.close()
        self.load_bills()

    def load_bills(self):
        conn = db()
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM bills").fetchall()
        conn.close()

        self.table_b.setRowCount(len(rows))
        self.table_b.setColumnCount(5)

        for r, row in enumerate(rows):
            for c, val in enumerate(row[:5]):
                self.table_b.setItem(r, c, QTableWidgetItem(str(val)))


# ─────────────────────────────
if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    w = Login()
    w.show()

    sys.exit(app.exec_())