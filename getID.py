import sqlite3

#新聞用
def getNameData():
    stockID = ['5203', '6112', '6183', '6214']
    stockName = ['"訊連"' ,'"聚碩"' ,'"關貿"' ,'"精誠"']
    return stockID,stockName

def getName(id):
    stockID = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    stockName = ['2427三商電','2453凌群' ,'2468華經' ,'2471資通' ,'2480敦陽' ,'3029零壹' ,'3130一零四' ,'4994傳奇' ,'5203訊連' ,'6112聚碩' ,'6183關貿' ,'6214精誠']
    for i in range(len(stockID)):
        if id == stockID[i]:
            return stockName[i]

def check(idd):
    stockID = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    c = 1
    for i in range(len(stockID)):
        if idd == stockID[i]:
            c = 0
    return c

def checkTec(ty):
    typeID = ['rsi', 'kd', 'macd', 'bias']
    c = ['rsi', 0]
    for i in range(len(typeID)):
        if ty == typeID[i]:
            c[0] = typeID[i]
            c[1] = i
    return c

def checkCha(ty):
    typeID = ['30days', 'today']
    c = ['30days', 0]
    for i in range(len(typeID)):
        if ty == typeID[i]:
            c[0] = typeID[i]
            c[1] = i
    return c
    
def checkFin(ty):
    typeName = ['個股月營收', '成長性分析', '股利政策', '獲利能力分析(季)', '資本形成-股東權益(季)', '現金分析(年)', '償還能力分析(季)', '經營能力分析(年)']
    typeID = ['SymScore', 'GrowthAnly', 'Divpolicy', 'ProfitByQr', 'Capstreq', 'Cashratio', 'SolvencyBySym', 'Oper']
    c = ['SymScore', 0, '個股月營收']
    for i in range(len(typeID)):
        if ty == typeID[i]:
            c[0] = typeID[i]
            c[1] = i
            c[2] = typeName[i]
    return c

def checkPre(ty):
    typeID = ['pre', 'today']
    c = ['pre', 0]
    for i in range(len(typeID)):
        if ty == typeID[i]:
            c[0] = typeID[i]
            c[1] = i
    return c
    

#帳號管理
def getAcc():
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from account")
    re = []
    for rows in c.fetchall():
        re.append(rows)
    return re

def deleteAcc(uid):
    err = 0
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from account")
    for rows in c.fetchall():
        if uid == rows[0]:
            err = 1
    if err == 1:
        with sqlite3.connect("stock.db") as con:
            cur = con.cursor()
            cur.execute("delete from account where username = '" + uid + "'")
            con.commit()
        with sqlite3.connect("stock.db") as con:
            cur = con.cursor()
            cur.execute("delete from indexStock where username = '" + uid + "'")
            con.commit()
    return

def alterAcc(uid, n, ty):
    if ty == '0':
        err = 0
        conn = sqlite3.connect('stock.db')
        c =conn.cursor()
        c.execute("select * from account")
        for rows in c.fetchall():
            if n == rows[0]:
                return 0
        if err != 1:
            with sqlite3.connect("stock.db") as con:
                cur = con.cursor()
                cur.execute("update account set username = '" + n + "' where username = '" + uid + "'")
                con.commit()
    elif ty == '1':
        with sqlite3.connect("stock.db") as con:
            cur = con.cursor()
            cur.execute("update account set email = '" + n + "' where username = '" + uid + "'")
            con.commit()
    elif ty == '2':
        with sqlite3.connect("stock.db") as con:
            cur = con.cursor()
            cur.execute("update account set password = '" + n + "' where username = '" + uid + "'")
            con.commit()
    return 1