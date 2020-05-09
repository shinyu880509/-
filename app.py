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
    datatoday = getData.getTodayCsv(stockID)
    dataTec = getData.getAll(stockID)
    #print(data)
    return render_template('homepage.html',re = data, name = name, tec = dataTec, stock = itStock, today = datatoday) 

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
    datatoday = getData.getTodayCsv(stockID)
    dataTec = getData.getAll(stockID)
    return render_template('homepage.html',re = data, name = name, tec = dataTec, today = datatoday, err = err) 

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
    datatoday = getData.getTodayCsv(stockID)
    dataTec = getData.getAll(stockID)
    return render_template('index.html', re = data, name = name, tec = dataTec, today = datatoday, err = err) 

@app.route("/technical/<cType>/<stId>")
def technical(cType,stId):
    global stockID
    print(stId)
    err = getID.check(stId)
    chart = getID.checkType(cType)
    if err == 0:
        stockID = stId
    dataTec = getData.getAll(stockID)
    data = getData.getData(stockID)
    name = []
    name.append(getID.getName(stockID))
    name.append(cType)
    return render_template('technical.html', re = data, name = name, tec = dataTec, cType = chart, err = err) 



if __name__ == "__main__":
    app.run()