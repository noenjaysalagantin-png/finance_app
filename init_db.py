import sqlite3

conn = sqlite3.connect("finance.db")
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  category TEXT,
  amount REAL,
  payment_method TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS sales (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  description TEXT,
  amount REAL,
  type TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS bills (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  category TEXT,
  amount REAL,
  due_date TEXT,
  status TEXT
);

CREATE TABLE IF NOT EXISTS budgets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT UNIQUE,
  monthly_budget REAL
);

CREATE TABLE IF NOT EXISTS inventory (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT,
  item_name TEXT,
  category TEXT,
  beginning_qty INTEGER,
  purchased_qty INTEGER,
  sold_qty INTEGER,
  cost REAL,
  price REAL
);
""")

conn.commit()
conn.close()
print("Database created successfully.")
