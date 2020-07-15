import sqlite3

conn = sqlite3.connect('stock.db')
c =conn.cursor()

#創建資料表

c.execute('''CREATE TABLE account
       (username  CHAR(50)  PRIMARY KEY     NOT NULL,
        email     CHAR(50)    NOT NULL,
        password  CHAR(50)     NOT NULL);''')

c.execute('''CREATE TABLE attention
       (username  CHAR(50)  PRIMARY KEY     NOT NULL,
        attention  CHAR(50)    NOT NULL);''')

c.execute('''CREATE TABLE verification
      (username  CHAR(50)  PRIMARY KEY     NOT NULL,
       email      CHAR(50)     NOT NULL,
       verification CHAR(50));''')

conn.commit()
conn.close()

#查詢
"""
c.execute("select * from account")

user = input("輸入帳號:")
password = input("輸入密碼")

for rows in c.fetchall():
       if user == rows[0] and password == rows[2]:
            print("成功登入")
            break
else:
       print("帳號密碼錯誤")   
"""