import sqlite3

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
    
def checkLoginAcc(uid, pwd):
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from account")
    for rows in c.fetchall():
        if uid == rows[0] and pwd == rows[2]:
            print("登入成功")
            return True

    print("登入失敗")
    return False

def checkLoginAccID(uid):
    conn = sqlite3.connect('stock.db')
    c =conn.cursor()
    c.execute("select * from account")
    for rows in c.fetchall():
        if uid == rows[0]:
            print("帳號存在")
            return True

    print("帳號不存在")
    return False