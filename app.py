from flask import Flask, request, render_template
import pandas as pd
import csv
import numpy as np
import twstock
import getData, catStock, getID

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
stockID = '2427'

@app.route("/")
def home():
    name = getID.getName(stockID)
    data = getData.getData(stockID)
    return render_template('index.html',datelist2 = data[0], closelist2 = data[1],translist2 = data[2],re = data[3], name = name) 

@app.route("/",methods=['POST'])
def search():
    if request.method == 'POST':
        ID = str(request.values['stock_id'])
        if getID.check(ID) == 1:
            stockID = ID
    name = getID.getName(stockID)
    data = getData.getData(stockID)
    return render_template('index.html',datelist2 = data[0], closelist2 = data[1],translist2 = data[2],re = data[3], name = name) 


#catStock.catStock() 更新股票資料 會跑1分鐘

if __name__ == "__main__":
    app.run()