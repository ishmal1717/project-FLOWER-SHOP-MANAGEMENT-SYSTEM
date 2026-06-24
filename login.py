class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌸 Flower Shop Login")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Login")
        btn.clicked.connect(self.login)

        layout.addWidget(self.user)
        layout.addWidget(self.passw)
        layout.addWidget(btn)

    def login(self):
        conn = db()
        cur = conn.cursor()
        u = cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                        (self.user.text(), self.passw.text())).fetchone()
        conn.close()

        if u:
            self.d = Dashboard()
            self.d.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid login")

