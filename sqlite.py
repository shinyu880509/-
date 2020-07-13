import sqlite3

#連結資料庫
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
