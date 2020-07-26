import sqlite3
conn = sqlite3.connect('stock.db')
c =conn.cursor()
c.execute("select * from account")
for rows in c.fetchall():
    print(rows)