import sqlite3
import random
import datetime

#驗證碼
def generate_verification_code(len=6):
    code_list = [] 
    for i in range(10): # 0-9
        code_list.append(str(i))
    for i in range(65, 91): # A-Z
        code_list.append(chr(i))
    for i in range(97, 123): # a-z
        code_list.append(chr(i))
    myslice = random.sample(code_list, len)
    verification_code = ''.join(myslice)
    return verification_code

#帳號信箱寫入驗證表
def verification(username,useremail):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("select * from verification")
    for rows in cur.fetchall():
        if useremail == rows[1]:
            print("已存在")
            return rows[2]
    cur.execute("select * from account")
    for rows in cur.fetchall():
        if username == rows[0]:
            a = generate_verification_code()
            cur.execute("insert into verification(username,email,verification) values('{}','{}','{}');".format(username,useremail,a))
            conn.commit()
            conn.close
            return a
    return "1"


'''username = input("user:")
useremail = input("email:")

print(verification(username, useremail))

conn = sqlite3.connect('stock.db')
c =conn.cursor()
c.execute("select * from verification")
for rows in c.fetchall():
    print(rows)
print("\n")'''


#修改密碼
def revisePw(password,verification):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("select * from verification")
    for rows in cur.fetchall():
        if verification == rows[2]:
            cur.execute("update account set password ='{}' where username = '{}';".format(password,rows[0]))
            cur.execute("delete from verification where verification = '{}';".format(verification))
            conn.commit()
            conn.close()
            return "1"
    return "0"


'''verification = input("verification:")
password = input("password:")

revisePw(password,verification)
conn = sqlite3.connect('stock.db')
c =conn.cursor()
c.execute("select * from verification")
for rows in c.fetchall():
    print(rows)
print("\n")
conn = sqlite3.connect('stock.db')
c =conn.cursor()
c.execute("select * from account")
for rows in c.fetchall():
    print(rows)'''

#新增順序
'''conn = sqlite3.connect('stock.db')
c =conn.cursor()
c.execute("select * from indexStock")
for rows in c.fetchall():
    print(rows)
    con = sqlite3.connect('stock.db')
    cc = con.cursor()
    con.execute("update indexStock set ind ='{}' where username = '{}';".format("0-1-2-3-4",rows[0]))
    con.commit()
    con.close()'''

#取得順序
def getIde(username):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("select * from indexStock where username = '{}';".format(username))
    a = cur.fetchall()
    conn.commit()
    conn.close()
    re = a[0][1].split("-")
    re = list(map(int, re))
    return re
#print(getIde("10646021")[0])

#更改順序
def revIde(username, ind):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("update indexStock set ind ='{}' where username = '{}';".format(ind,username))
    conn.commit()
    conn.close()
    return

#關注寫入
def like(username,stockID):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("insert into attention(username,attention) values('{}','{}');".format(username,stockID))
    conn.commit()
    conn.close()
    return

#關注移除
def dislike(username):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("delete from attention where username = '{}';".format(username))
    conn.commit()
    conn.close()
    return

def getlike(username):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("select * from attention where username = '{}';".format(username))
    try:
        a = str(cur.fetchall()[0][1])
        a = a.split("-")
    except Exception:
        conn.commit()
        conn.close()
        return []
    conn.commit()
    conn.close()
    return a
#print(getlike("10646021"))

#新增順序
'''conn = sqlite3.connect('stock.db')
c =conn.cursor()
c.execute("insert into postArticle(username,stockId,article,floor,aTitle,aText,aLike,aDislike,aTime) values('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format("10646021","2427","03","0","test","test\r\n123133","1","1","2020/11/3 2:33"))
conn.commit()
conn.close()'''

def getArtcile(stid):
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from postArticle where stockId = '{}';".format(stid))
    re = []
    for rows in c.fetchall():
        aa = []
        for i in range(len(rows)):
            aa.append(rows[i])
        re.append(aa)
    return re
#print(getArtcile("2427"))

def postArtcile(userid, stid, title, text):
    time = datetime.datetime.today()

    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from postArticle where stockId = '{}';".format(stid))
    artList = c.fetchall()
    artNum = int(artList[len(artList)-1][2])+1
    conn.close

    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("insert into postArticle(username,stockId,article,floor,aTitle,aText,aLike,aDislike,aTime) values('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(userid, stid, artNum, "0", title, text,"0","0",time))
    conn.commit()
    conn.close()