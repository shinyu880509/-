from flask import Flask, request, render_template
import pandas as pd
import csv
import numpy as np

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route("/")
def home():
    return render_template('index.html',datelist2 = datelist, closelist2 = closelist,re = re) 
   
itStock = ['2427']
stockID = itStock[0]
'''
stock = twstock.Stock(stockID)

stockFetch = stock.fetch_31()
stockDf = pd.DataFrame(stockFetch)
stockDf.set_index('date', inplace = True)
stockDf.to_csv(stockID+'.csv')
'''
table = pd.read_csv(stockID+'.csv')

date = np.array(table.date)
datelist = date.tolist()
close = np.array(table.close)
closelist = close.tolist()

capacity = np.array(table.capacity)
capacitylist = capacity.tolist()
turnover = np.array(table.turnover)
turnoverlist = turnover.tolist()
change = np.array(table.change)
changelist = change.tolist()
trans = np.array(table.transaction)
translist = trans.tolist()

re = []
a = sum(capacitylist)
re.append(str(a))
a = sum(turnoverlist)
re.append(str(a))
a = sum(translist)
re.append(str(a))
a = max(closelist)
re.append(str(a))
a = min(closelist)
re.append(str(a))
b = round(sum(changelist),2)
re.append(str(b))
b = round(sum(closelist)/len(closelist),2)
re.append(str(b))


if __name__ == "__main__":
    app.run()



