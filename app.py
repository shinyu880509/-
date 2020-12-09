from flask import Flask, request, render_template , redirect , url_for, flash, send_file
from flask_mail import Mail,Message
import pandas as pd
import csv
import numpy as np
import getData, catStock, getID, accountSql
import click
import datetime
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user 

from livereload import Server
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
a = 0
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#一頁新聞數量
n = 3

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
    MAIL_PASSWORD='<a1s2d3f4>'
)
mail = Mail(app)

#寄驗證信
@app.route("/message/<ema>/<acc>")
def mesage(acc,ema):
    aa = accountSql.verification(acc, ema)
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

#寄關注信
@app.route("/messagedaily/<stid>")
def messagedaily(stid):
    conn = sqlite3.connect('stock.db')
    cur = conn.cursor()
    cur.execute("select * from setDaliyMail")
    for rows in cur.fetchall():
        curr = conn.cursor()
        curr.execute("select * from account where username = '{}';".format(rows[0]))
        for ro in curr.fetchall():
            ema = ro[1]
            print(rows[0] + ro[1])
            cu = conn.cursor()
            cu.execute("select * from attention where username = '{}';".format(rows[0]))
            intent = ""
            for r in cu.fetchall():
                stockid = r[1].split("-")
                for i in stockid:
                    a = getData.getPreByDay(i, 1)
                    intent += i + "\r\n" + a[1][0][0] + "\r\n\r\n"
            print(intent)

            ti = datetime.datetime.now()
            msg_title = str(ti.month) + '/' + str(ti.day) + '關注股票之預測分析'
            msg_recipients = [ema]
            msg_body = intent + '\r\n系統時間：' + str(datetime.datetime.now())
            msg = Message(msg_title,recipients=msg_recipients)
            msg.body = msg_body
            mail.send(msg)

    return redirect(url_for('indexId', stId = stid))

#驗證修改密碼
@app.route("/revise/<va>/<pw>")
def reviseA(pw,va):
    aa = accountSql.revisePw(pw, va)
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
    a = accountSql.checkLoginAcc(userId, userPasswd)
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

#修改密碼
@app.route('/changePasswd')
def changePasswd():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    return render_template('changePasswd.html') 
@app.route('/changePasswd/<oddPd>/<newPd>')
def changePasswdDo(oddPd, newPd):
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    a = accountSql.changePw(current_user.id, oddPd, newPd)
    print(type(a))
    if a == "0":
        flash("訊舊密碼錯誤，請再確認")
        return redirect(url_for('changePasswd'))
    elif a == "1":
        flash("訊密碼修改成功")
        return redirect(url_for('accountSetting'))

#修改信箱
@app.route('/changeMail')
def changeMail():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    return render_template('changeMail.html') 
@app.route('/changeMail/<oddMail>/<newMail>')
def changeMailDo(oddMail, newMail):
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    a = accountSql.changeMail(current_user.id, oddMail, newMail)
    print(type(a))
    if a == "0":
        flash("訊舊信箱錯誤，請再確認")
        return redirect(url_for('changeMail'))
    elif a == "1":
        flash("訊信箱修改成功")
        return redirect(url_for('accountSetting'))

@app.route("/index")
def index():
    return redirect(url_for('indexId', stId = "2427"))

@app.route("/index/<stId>")
def indexId(stId):
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    aa = stId.split("-")
    name = getID.getName(aa[0])
    data = getData.getData(aa[0])
    datatoday = getData.getTodayCsv(aa[0])
    datalive = getData.getLive(aa[0])
    dataTec = getData.getAll(aa[0])
    dataFin = getData.getAllFin(aa[0])
    dataPre = getData.getPreByDay(aa[0], 10)
    dataNews = getData.getNewsS(aa[0], n)
    dataFav = accountSql.getlike(current_user.id)
    dataInd = accountSql.getIde(current_user.id)
    dataArt = accountSql.getArtcile(aa[0])
    dataReArt = accountSql.getReArtcile(aa[0])
    lenArt = len(dataArt)
    toArt = "0"
    inArt = "0"
    if len(aa) == 2:
        toArt = aa[1]
    elif len(aa) == 3:
        toArt = aa[1]
        inArt = aa[2]
    return render_template('index.html', stock = aa[0], name = name, re = data, today = datatoday, tec = dataTec, fin = dataFin, pre = dataPre, news = dataNews, n = n, reFav = dataFav, live = datalive, ind = dataInd, art = dataArt, lenArt = lenArt, reArt = dataReArt, toArt = toArt, inArt = inArt)  

@app.route("/newFav/<typeA>/<stId>/<fav>")
def newFav(fav, typeA, stId):
    accountSql.dislike(str(current_user.id))
    if fav != "non":
        accountSql.like(str(current_user.id), fav)
    if typeA == "index":
        return redirect(url_for('indexId', stId = stId))
    elif typeA == "news":
        return redirect(url_for('news', stId = stId))
    elif typeA == "logout":
        return redirect(url_for('logout'))
    elif typeA == "setting":
        return redirect(url_for('accountSetting'))

@app.route("/news/<stId>")
def news(stId):
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    name = getID.getName(stId)
    dataNews = getData.getNews(stId)
    dataFav = accountSql.getlike(current_user.id)
    return render_template('news.html', stock = stId, name = name, news = dataNews, n = len(dataNews), reFav = dataFav)  

#發文
@app.route("/postArt/<stId>", methods=['GET', 'POST'])
def postArt(stId):
    if request.method == 'POST':
        title = request.form.get('secTitle') + request.form.get('postTitle')
        text = request.form.get('postText')
        text = text.replace("\r\n", "<br>")
        accountSql.postArtcile(current_user.id, stId, title, text)
        stId += "-1"
        return redirect(url_for('indexId', stId = stId))

@app.route("/delart/<stId>/<art>")
def delart(stId, art):
    accountSql.delArtcile(stId,art)
    return redirect(url_for('indexId', stId = stId))

#留言
@app.route("/postReArt/<stId>", methods=['GET', 'POST'])
def postReArt(stId):
    if request.method == 'POST':
        text = request.form.get('inputCom')
        artNum = request.form.get('artNum')
        accountSql.postReArtcile(current_user.id, stId, artNum, text)
        stId += "-2"
        return redirect(url_for('indexId', stId = stId))

@app.route("/saveGd/<stId>/<artNum>/<num>")
def saveGd(stId, artNum, num):
    print(stId, artNum)
    a = accountSql.setGood(current_user.id, stId, artNum)
    stId += "-3-" + num
    if a == 1:
        flash("訊這篇文章已經點過喜歡或不喜歡了")
    return redirect(url_for('indexId', stId = stId))

@app.route("/saveBd/<stId>/<artNum>/<num>")
def saveBd(stId, artNum, num):
    a = accountSql.setBad(current_user.id, stId, artNum)
    stId += "-3-" + num
    if a == 1:
        flash("訊這篇文章已經點過喜歡或不喜歡了")
    return redirect(url_for('indexId', stId = stId))

#個人化設定
@app.route("/setting")
def accountSetting():
    if current_user.is_authenticated == False:
        return redirect(url_for('index'))
    ind = accountSql.getIde(current_user.id)
    aa = accountSql.getDailyMail(current_user.id)
    return render_template('accountSetting.html', ind = ind, aa = aa) 

#個人化設定儲存--順序
@app.route("/savInd/<ind>")
def savIndex(ind):
    accountSql.revIde(current_user.id, ind)
    return redirect(url_for('accountSetting'))

#個人化設定儲存--Mail
@app.route("/dailyMail/<how>")
def dailyMail(how):
    if how == "1":
        accountSql.dailyMailDel(current_user.id)
    elif how == "0":
        accountSql.dailyMail(current_user.id)
    return redirect(url_for('accountSetting'))

#註冊
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
            con = sqlite3.connect('stock.db')
            cc = con.cursor()
            cc.execute("insert into indexStock(username,ind) values('{}','{}');".format(userId,"0-1-2-3-4"))
            con.commit()
            con.close()
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
    catStock.catAll()

@app.route("/refresh/<stid>")
def refreshData(stid):
    catStock.catAll()
    return redirect(url_for('indexId', stId = stid))

#設置登入系統
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(uid):
    a = accountSql.checkLoginAccID(uid)
    if a == False:
        return
    user = User()
    user.id = uid
    return user

@login_manager.request_loader
def request_loader(request):
    uid = request.form.get('username')
    a = accountSql.checkLoginAccID(uid)
    if a == False:
        return
    user = User()
    user.id = uid

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    a = accountSql.checkLoginAcc(uid, request.form['password'])
    user.is_authenticated = a
    return user

if __name__ == "__main__":
    #live_server = Server(app.wsgi_app)
    #live_server.watch("catToday/*.*")
    #live_server.serve(open_url_delay=True)
    app.run(debug=True)