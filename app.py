from flask import Flask, request, render_template , redirect , url_for, flash
from flask_mail import Mail,Message
import pandas as pd
import csv
import numpy as np
import getData, catStock, getID, revise
import click
import datetime
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user 

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
a = 0
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#一頁新聞數量
n = 15

#登入管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

#信箱設置
app.config.update(
    DEBUG=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=('admin', 'jjfj3750@gmail.com'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='jjfj3750@gmail.com',
    MAIL_PASSWORD=''
)
mail = Mail(app)

#寄驗證信
@app.route("/message/<ema>/<acc>")
def mesage(acc,ema):
    aa = revise.verification(acc, ema)
    if aa == "1":
        flash("訊帳號不存在")
        flash("使" + acc)
        flash("信" + ema)
        return redirect(url_for('forget'))
    else:
        msg_title = '驗證信'
        msg_recipients = [ema]
        msg_body = '驗證碼:' + aa + '\r\n系統時間：' + str(datetime.datetime.now())
        msg = Message(msg_title,recipients=msg_recipients)
        msg.body = msg_body
        mail.send(msg)
        flash("訊驗證信已送出，請確認信箱")
        return redirect(url_for('reviseB'))

#驗證修改密碼
@app.route("/revise/<va>/<pw>")
def reviseA(pw,va):
    aa = revise.revisePw(pw, va)
    if aa == "0":
        flash("訊驗證碼錯誤")
        flash("密" + pw)
        return redirect(url_for('reviseB'))
    elif aa == "1":
        flash("訊密碼變更成功")
        return redirect(url_for('login'))

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login")
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('index'))
    return render_template('login.html') 

#登入
@app.route("/userLogin/<userId>/<userPasswd>")
def userLogin(userId, userPasswd):
    a = getID.checkLoginAcc(userId, userPasswd)
    if a:
        user = User()
        user.id = userId
        login_user(user)
        return redirect(url_for('index'))
    else:
        flash("誤")
        flash("帳" + userId)
        return redirect(url_for('login'))

#登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#管理帳號
@app.route('/manage')
def manage():
    acc = getID.getAcc()
    return render_template('manage.html', acc = acc, n = len(acc)) 

#刪除帳號
@app.route('/deleteAcc/<a>')
def deleteAcc(a):
    getID.deleteAcc(a)
    return redirect(url_for('manage'))

#修改帳號
@app.route('/alterAcc/<a>/<n>/<t>')
def alterAcc(a,n,t):
    aaa = getID.alterAcc(a,n,t)
    if aaa == 0:
        flash("帳號名稱重複")
    return redirect(url_for('manage'))

@app.route("/index")
def index():
    return redirect(url_for('indexId', stId = "2427"))

@app.route("/index/<stId>")
def indexId(stId):
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    name = getID.getName(stId)
    data = getData.getData(stId)
    datatoday = getData.getTodayCsv(stId)
    dataTec = getData.getAll(stId)
    dataFin = getData.getAllFin(stId)
    dataPre = getData.getPreByDay(stId, 10)
    dataNews = getData.getNewsS(stId, n)
    dataFav = revise.getlike(current_user.id)
    return render_template('index.html', stock = stId, name = name, re = data, today = datatoday, tec = dataTec, fin = dataFin, pre = dataPre, news = dataNews, n = n, reFav = dataFav)  

@app.route("/newFav/<typeA>/<stId>/<fav>")
def newFav(fav, typeA, stId):
    revise.dislike(str(current_user.id))
    if fav != "non":
        revise.like(str(current_user.id), fav)
    if typeA == "index":
        return redirect(url_for('indexId', stId = stId))
    elif typeA == "news":
        return redirect(url_for('news', stId = stId))
    elif typeA == "logout":
        return redirect(url_for('logout'))

@app.route("/news/<stId>")
def news(stId):
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    name = getID.getName(stId)
    dataNews = getData.getNews(stId)
    dataFav = revise.getlike(current_user.id)
    return render_template('news.html', stock = stId, name = name, news = dataNews, n = len(dataNews), reFav = dataFav)  

@app.route("/account")
def account():
    return render_template('account.html')
    
#註冊帳號寫進資料庫
@app.route("/registeCheck/<userId>/<userPasswd>/<userEmail>")
def registers(userId, userPasswd, userEmail):
    err = 0
    try:
        conn = sqlite3.connect('stock.db')
        c =conn.cursor()
        c.execute("select * from account")
        for rows in c.fetchall():
            if userId == rows[0]:
                err = 1
        if err != 1:
            with sqlite3.connect("stock.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO account (username,email,password) VALUES (?,?,?)", (userId,userEmail,userPasswd))
                con.commit()
                con.close()
    finally:
        if err == 0:
            return redirect(url_for('login'))
        else:
            flash("帳" + userId)
            flash("信" + userPasswd)
            flash("密" + userEmail)
            flash("誤")
            return redirect(url_for('account'))

@app.route("/forget")
def forget():
    return render_template('forget.html')

@app.route("/revise")
def reviseB():
    return render_template('revise.html')

@app.cli.command("refresh")
def refresh():
    catStock.catStock()

#查詢功能 + 重新導向
@app.route("/chart/<cType>",methods=['POST'])
def searchCha(cType):
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    chart = getID.checkCha(cType)
    if err == 0:
        stockID = ID
    return redirect(url_for('chart', stId = stockID, cType = chart[0]))

@app.route("/technical/<cType>",methods=['POST'])
def searchTec(cType):
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    chart = getID.checkTec(cType)
    if err == 0:
        stockID = ID
    return redirect(url_for('technical', stId = stockID, cType = chart[0]))

@app.route("/financial/<cType>",methods=['POST'])
def searchFin(cType):
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    chart = getID.checkFin(cType)
    if err == 0:
        stockID = ID
    return redirect(url_for('financial', stId = stockID, cType = chart[0]))

@app.route("/predict/<cType>",methods=['POST'])
def searchPre(cType):
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    chart = getID.checkPre(cType)
    if err == 0:
        stockID = ID
    return redirect(url_for('predict', stId = stockID, cType = chart[0]))    
    

#進入30日圖表 /chart/30days/2427
#進入當日圖表 /chart/today/2427
@app.route("/chart/<cType>/<stId>")
def chart(cType,stId):
    global stockID
    print(stId)
    print(cType)
    err = getID.check(stId)
    chart = getID.checkCha(cType)
    if err == 0:
        stockID = stId
    name = getID.getName(stockID)
    data = getData.getData(stockID)
    datatoday = getData.getTodayCsv(stockID)
    return render_template('index.html', re = data, name = name, today = datatoday, cType = chart, err = err, stock = stockID) 

#進入技術指標 /technical/rsi/2427 
@app.route("/technical/<cType>/<stId>")
def technical(cType,stId):
    global stockID
    print(stId)
    err = getID.check(stId)
    chart = getID.checkTec(cType)
    if err == 0:
        stockID = stId
    dataTec = getData.getAll(stockID)
    data = getData.getData(stockID)
    name = getID.getName(stockID)
    return render_template('technical.html', re = data, name = name, tec = dataTec, cType = chart, err = err, stock = stockID) 

#進入技術指標 /financial/SymScore/2427 
@app.route("/financial/<cType>/<stId>")
def financial(cType,stId):
    global stockID
    print(stId)
    err = getID.check(stId)
    chart = getID.checkFin(cType)
    if err == 0:
        stockID = stId
    dataFin = getData.getFin(stockID, chart[1])
    name = getID.getName(stockID)
    return render_template('financial.html', name = name, fin = dataFin, cType = chart, err = err, stock = stockID) 

#進入技術指標 /predict/pre/2427 
@app.route("/predict/<cType>/<stId>")
def predict(cType,stId):
    global stockID
    print(stId)
    err = getID.check(stId)
    chart = getID.checkPre(cType)
    if err == 0:
        stockID = stId
    dataPre = getData.getPre(stockID, 0)
    print(dataPre)
    name = getID.getName(stockID)
    return render_template('predict.html', name = name, pre = dataPre, cType = chart, err = err, stock = stockID)     

#設置登入系統
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(uid):
    a = getID.checkLoginAccID(uid)
    if a == False:
        return
    user = User()
    user.id = uid
    return user

@login_manager.request_loader
def request_loader(request):
    uid = request.form.get('username')
    a = getID.checkLoginAccID(uid)
    if a == False:
        return
    user = User()
    user.id = uid

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    a = getID.checkLoginAcc(uid, request.form['password'])
    user.is_authenticated = a
    return user


if __name__ == "__main__":
    app.run(debug=True)