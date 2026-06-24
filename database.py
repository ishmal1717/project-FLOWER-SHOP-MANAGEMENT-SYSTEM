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
        email TEXT,
        address TEXT,
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
        items TEXT,
        subtotal REAL,
        tax REAL,
        discount REAL,
        total REAL,
        date TEXT
    )""")

    cur.execute("INSERT OR IGNORE INTO users(username,password) VALUES('admin','admin')")
    conn.commit()
    conn.close()