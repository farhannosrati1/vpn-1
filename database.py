import sqlite3
db=sqlite3.connect('shop.db')
cur=db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
username TEXT,
plan TEXT,
price INTEGER,
status TEXT,
delivery TEXT)''')
db.commit()
