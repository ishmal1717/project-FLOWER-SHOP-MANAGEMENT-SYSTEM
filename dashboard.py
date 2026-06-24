# DASHBOARD
# ─────────────────────────────
import sys
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QMessageBox
from PyQt5.QtGui import QFont
class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌸 Flower Shop Management System")
        self.resize(1200, 800)

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

        btn = QPushButton("Add Flower")
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
                    (self.f_name.text(), self.f_type.text(),
                     self.f_color.text(), 0, self.f_price.text(), today()))

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
