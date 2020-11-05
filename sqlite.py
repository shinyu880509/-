import sqlite3

conn = sqlite3.connect('stock.db')
c =conn.cursor()
c.execute('''drop table replyArticle''')
c.execute('''CREATE TABLE replyArticle
       (username  CHAR(50)  NOT NULL,
        stockId  CHAR(50)    NOT NULL,
        article  CHAR(50)    NOT NULL,
        floor  CHAR(50)    NOT NULL,
        aText  CHAR(50)    NOT NULL,
        aTime  CHAR(50)    NOT NULL);''')
#創建資料表
"""
c.execute('''drop table replyArticle''')
c.execute('''CREATE TABLE replyArticle
       (username  CHAR(50)  NOT NULL,
        stockId  CHAR(50)    NOT NULL,
        article  CHAR(50)    NOT NULL,
        floor  CHAR(50)    NOT NULL,
        aText  CHAR(50)    NOT NULL,
        aTime  CHAR(50)    NOT NULL);''')

c.execute('''drop table postArticle''')
c.execute('''CREATE TABLE postArticle
       (username  CHAR(50)  NOT NULL,
        stockId  CHAR(50)    NOT NULL,
        article  CHAR(50)    NOT NULL,
        floor  CHAR(50)    NOT NULL,
        aTitle  CHAR(50)    NOT NULL,
        aText  CHAR(50)    NOT NULL,
        aLike  CHAR(50)    NOT NULL,
        aDislike  CHAR(50)    NOT NULL,
        aTime  CHAR(50)    NOT NULL);''')

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

c.execute('''CREATE TABLE indexStock
       (username  CHAR(50)  PRIMARY KEY     NOT NULL,
        ind  INT(50)    NOT NULL);''')
"""
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