import sqlite3
conn = sqlite3.connect('stock.db')
c =conn.cursor()
#c.execute("delete from verification where username = '{}';".format("10646021"))
c.execute("select * from verification")
for rows in c.fetchall():
    print(rows)