import pandas as pd
import csv
import numpy as np

def getData(a):
    table = pd.read_csv("catStock/"+a+'.csv')
   

    date = np.array(table.date)
    datelist = date.tolist()
  
    close = np.array(table.close)
    closelist = close.tolist()

    capacity = np.array(table.Trading_Volume)
    capacitylist = capacity.tolist()
    turnover = np.array(table.Trading_money)
    turnoverlist = turnover.tolist()
    change = np.array(table.spread)
    changelist = change.tolist()
    trans = np.array(table.Trading_turnover)
    translist = trans.tolist()

  

    re = []
    mou = -30
    a = sum(capacitylist[mou:])
    re.append(str(a))
    a = sum(turnoverlist[mou:])
    re.append(str(a))
    a = sum(translist[mou:])
    re.append(str(a))
    a = max(closelist[mou:])
    re.append(str(a))
    a = min(closelist[mou:])
    re.append(str(a))
    b = round(sum(changelist[mou:]),2)
    re.append(str(b))
    b = round(sum(closelist[mou:])/len(closelist[mou:]),2)
    re.append(str(b))
    return datelist[mou:],closelist[mou:],translist[mou:],re