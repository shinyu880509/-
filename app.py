from flask import Flask, request, render_template
import pandas as pd
import csv
import numpy as np
import getData, catStock, getID

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
stockID = '2427'
itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
a = 0
@app.route("/")
def home():
    name = getID.getName(stockID)
    data = getData.getData(stockID)
    dataTec = getData.getAll(stockID)
    #print(data)
    return render_template('index.html',re = data, name = name, tec = dataTec, stock = itStock) 

#查詢功能
@app.route("/",methods=['POST'])
def search():
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    if err == 0:
        stockID = ID
    name = getID.getName(stockID)
    data = getData.getData(stockID)
    dataTec = getData.getAll(stockID)
    return render_template('index.html',re = data, name = name, tec = dataTec, err = err) 

#輸入網址進入對應股票
@app.route("/stockpd<stId>")
def searchB(stId):
    global stockID
    print(stId)
    err = getID.check(stId)
    if err == 0:
        stockID = stId
    name = getID.getName(stockID)
    data = getData.getData(stockID)
    dataTec = getData.getAll(stockID)
    return render_template('index.html',re = data, name = name, tec = dataTec, err = err) 


#catStock.catStock() 更新股票資料 會跑1分鐘

if __name__ == "__main__":
    app.run()