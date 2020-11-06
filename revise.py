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

#修改密碼
def changePw(uid, odd, new):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("select * from account where username = '{}';".format(uid))
    for rows in cur.fetchall():
        if odd == rows[2]:
            cur.execute("update account set password ='{}' where username = '{}';".format(new,uid))
            conn.commit()
            conn.close()
            return "1"
    return "0"

#修改Mail
def changeMail(uid, odd, new):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("select * from account where username = '{}';".format(uid))
    for rows in cur.fetchall():
        if odd == rows[1]:
            cur.execute("update account set email ='{}' where username = '{}';".format(new,uid))
            conn.commit()
            conn.close()
            return "1"
    return "0"

#每日送信
def getDailyMail(uid):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("select * from setDaliyMail where username = '{}';".format(uid))
    if cur.fetchall() == []:
        return "0"
    else:
        return "1"
def dailyMail(uid):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("insert into setDaliyMail(username) values('{}');".format(uid))
    conn.commit()
    conn.close()
    return "0"
def dailyMailDel(uid):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("delete from setDaliyMail where username = '{}';".format(uid))
    conn.commit()
    conn.close()
    return "0"
dailyMailDel("10646021")
print(getDailyMail("10646021"))

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
'''
conn = sqlite3.connect('stock.db')
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
#print(getIde("10646021"))

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

#取得文章
def getArtcile(stid):
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from postArticle where stockId = '{}';".format(stid))
    re = []
    for rows in c.fetchall():
        aa = []
        for i in range(len(rows)):
            if i == 6 or i == 7:
                gd = rows[i].split("-")
                if gd!=[""]:
                    aa.append(len(gd))
                else:
                    aa.append("0")
            else:
                aa.append(rows[i])
        re.append(aa)
    re.sort(key=lambda x:x[8], reverse=True)
    return re
#print(getArtcile("2427"))

#發文
def postArtcile(userid, stid, title, text):
    time = datetime.datetime.today()
    artNum = 0
    try:
        conn = sqlite3.connect('stock.db')
        c =conn.cursor()
        c.execute("select * from postArticle where stockId = '{}';".format(stid))
        artList = c.fetchall()
        artNum = int(artList[len(artList)-1][2])+1
        conn.close
    except Exception:
        artNum = 0
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("insert into postArticle(username,stockId,article,floor,aTitle,aText,aLike,aDislike,aTime) values('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(userid, stid, artNum, "0", title, text,"","",time))
    conn.commit()
    conn.close()
    return

#del發文
def delArtcile(stid, art):
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("delete from postArticle where stockId = '{}' and  article = '{}';".format(stid, art))
    print(c.fetchall())
    conn.commit()
    conn.close()
    return

#回覆
def postReArtcile(userid, stid, artNum, text):
    time = datetime.datetime.today()
    floor = 0
    try:
        conn = sqlite3.connect('stock.db')
        c =conn.cursor()
        c.execute("select * from replyArticle where stockId = '{}' and article = '{}';".format(stid, artNum))
        artList = c.fetchall()
        floor = int(artList[len(artList)-1][2])+1
        conn.close
    except Exception:
        floor = 0

    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("insert into replyArticle(username,stockId,article,floor,aText,aTime) values('{}','{}','{}','{}','{}','{}');".format(userid, stid, artNum, floor, text, time))
    conn.commit()
    conn.close()
    
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("update postArticle set aTime ='{}' where stockId = '{}' and article = '{}';".format(time, stid, artNum))
    conn.commit()
    conn.close()
    return

#取得回覆
def getReArtcile(stid):
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from replyArticle")
    re = []
    for rows in c.fetchall():
        aa = []
        for i in range(len(rows)):
            aa.append(rows[i])
        re.append(aa)
    return re
#print(getReArtcile("2427", "02"))

def setGood(userid, stid, artNum):
    good = ""
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from postArticle where stockId = '{}' and article = '{}';".format(stid, artNum))
    a = c.fetchall()[0]
    if a[6] == "":
        good = userid
    else:
        che = a[6].split("-")
        check = 0
        for i in range(len(che)):
            if che[i] == userid:
                check = 1
        if check == 0:
            good = a[6] + "-" + userid
        else:
            good = a[6]
    conn.close()

    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("update postArticle set aLike ='{}' where stockId = '{}' and article = '{}';".format(good, stid, artNum))
    conn.commit()
    conn.close()
    return

def setBad(userid, stid, artNum):
    Bad = ""
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from postArticle where stockId = '{}' and article = '{}';".format(stid, artNum))
    a = c.fetchall()[0]

    checkG = 0
    if a[6] != "":
        cheG = a[6].split("-")
        for i in range(len(cheG)):
            if cheG[i] == userid:
                checkG = 1

    if a[7] == "" and checkG == 0:
        Bad = userid
    elif checkG == 0:
        che = a[7].split("-")
        check = 0
        for i in range(len(che)):
            if che[i] == userid:
                check = 1
        if check == 0:
            Bad = a[7] + "-" + userid
        else:
            Bad = a[7]
    print(Bad)
    conn.close()

    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("update postArticle set aDislike ='{}' where stockId = '{}' and article = '{}';".format(Bad, stid, artNum))
    conn.commit()
    conn.close()
    return
#setGood("10646021", "2427", "1")
#print(getArtcile("2427"))