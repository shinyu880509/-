from flask import Flask, request, render_template
import pandas as pd
import csv
import numpy as np
import twstock
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
    print(data)
    return render_template('index.html',re = data, name = name, tec = dataTec, stock = itStock) 

@app.route("/",methods=['POST'])
def search():
    global stockID
    print(stockID)
    err = 1
    if request.method == 'POST':
        ID = str(request.values['stock_id'])
        for i in range(len(itStock)):
            if ID == itStock[i]:
                stockID = ID
                err = 0
                

    name = getID.getName(stockID)
    data = getData.getData(stockID)
    dataTec = getData.getAll(stockID)
    return render_template('index.html',re = data, name = name, tec = dataTec, err = err) 


#catStock.catStock() 更新股票資料 會跑1分鐘

if __name__ == "__main__":
    app.run()