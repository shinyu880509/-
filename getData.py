import pandas as pd
import csv
import numpy as np

#股票代碼
def getCsv(a):
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
    high = np.array(table.high)
    high = high.tolist()
    low = np.array(table.low)
    low = low.tolist()
    return datelist,closelist,capacitylist,turnoverlist,changelist,high,low,translist
    
#股票代碼
def getPre(a):
    table = pd.read_csv("preStock/"+a+'.csv')
    date = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
    opena = np.array(table.open)
    openlist = opena.tolist()
    close = np.array(table.close)
    closelist = close.tolist()
    trans = np.array(table.Trading_turnover)
    translist = trans.tolist()
    high = np.array(table.high)
    high = high.tolist()
    low = np.array(table.low)
    low = low.tolist()
    return openlist,closelist,high,low,translist,date

def getTodayCsv(a):
    table = pd.read_csv("catStock/"+a+'today.csv')
    columns = ['time','open','high','low','close','upanddown','transaction']
    table.columns = columns
    table = table.sort_index(ascending=False)

    time = np.array(table.time)
    timelist = time.tolist()
    opena = np.array(table.open)
    openlist = opena.tolist()
    high = np.array(table.high)
    highlist = high.tolist()
    low = np.array(table.low)
    lowlist = low.tolist()
    close = np.array(table.close)
    closelist = close.tolist()
    transaction = np.array(table.transaction)
    translist = transaction.tolist()

    re = []
    re.append(openlist[-1])
    z = max(highlist)
    re.append(str(z))
    z = min(lowlist)
    re.append(str(z))
    re.append(closelist[1])
    z = sum(translist)
    re.append(str(z))
    return timelist,closelist,translist,re

#股票代碼
def getData(a):
    csv = getCsv(a)
    re = []
    mou = -30
    z = sum(csv[2][mou:])
    re.append(str(z))
    z = sum(csv[3][mou:])
    re.append(str(z))
    z = sum(csv[7][mou:])
    re.append(str(z))
    z = max(csv[1][mou:])
    re.append(str(z))
    z = min(csv[1][mou:])
    re.append(str(z))
    b = round(sum(csv[4][mou:]),2)
    re.append(str(b))
    b = round(sum(csv[1][mou:])/len(csv[1][mou:]),2)
    re.append(str(b))
    re.append(csv[0][mou:])
    re.append(csv[1][mou:])
    re.append(csv[7][mou:])
    return re

#股票代碼
def getKD(a):
    csv = getCsv(a)
    clo = csv[1][-40:]
    hi = csv[5][-49:]
    lo = csv[6][-49:]
    rsv = []
    k = [50]
    d = [50]

    for i in range(len(clo)):
        zr = (clo[i] - min(lo[i:10 + i]))/(max(hi[i:10 + i]) - min(lo[i:10 + i]))
        zr *= 100
        rsv.append(round(zr,2))

        zk = (rsv[i]/3) + (k[i]/3*2)
        k.append(round(zk,2))
        zd = (k[i]/3) + (d[i]/3*2)
        d.append(round(zd,2))
    return k[-30:],d[-30:]

#平均
def ema(a,d):
    return sum(a)/d

#股票代碼
def getMACD(a):
    csv = getCsv(a)
    clo = csv[1][-64:]
    dif = []
    macd = []

    for i in range(39):
        ema12 = ema(clo[14+i:26+i],12)
        ema26 = ema(clo[i:26+i],26)
        zdif = ema12-ema26
        dif.append(round(zdif,2))
        if i > 7:
            zmacd = sum(dif[i-8:i+1])/9
            macd.append(round(zmacd,2))
    return dif,macd

#股票代碼,平均的天數,列出幾天
def getBIAS(a, long, dd):
    csv = getCsv(a)
    days = [6,12,24,72]
    clo = csv[1][-(days[long]+dd-1):]
    bias = []
    
    for i in range(dd):
        ema30 = ema(clo[i:days[long]+i],days[long])
        zbias = ((clo[days[long]-1+i]-ema30)/ema30)*100
        bias.append(round(zbias,2))
        '''可投資
        if long == 3 and (bias[i] <= -11 or bias[i] >= 11):
            print(clo[days[long]-1+i],bias[i])
        elif long == 2 and (bias[i] <= -7 or bias[i] >= 8):
            print(clo[days[long]-1+i],bias[i])
        elif long == 1 and (bias[i] <= -4.5 or bias[i] >= 5):
            print(clo[days[long]-1+i],bias[i])
        elif long == 0 and (bias[i] <= -3 or bias[i] >= 3.5):
            print(clo[days[long]-1+i],bias[i])
        '''
    return bias

#股票代碼,平均的天數,列出幾天
def getRSI(a, long, dd):
    csv = getCsv(a)
    days = long
    clo = csv[1][-(days+dd):]
    change = []
    rsi = []

    for i in range(len(clo)-1):
        z = clo[i+1] - clo[i]
        change.append(z)
    for i in range(dd):
        hi = []
        lo = []
        for j in range(days):
            if change[i+j] > 0:
                hi.append(change[i+j])
            elif change[i+j] < 0:
                lo.append(change[i+j])
        aHi = ema(hi,days)
        aLo = ema(lo,days)
        zrsi = (aHi/(aHi-aLo))*100
        rsi.append(round(zrsi,2))
    return rsi

def getAll(a):
    kd = getKD(a)
    ma = getMACD(a)
    return getRSI(a,30,30), kd[0], kd[1], ma[0], ma[1], getBIAS(a,2,30)
#print(getBIAS('2427',2,30))
#print(getRSI('2427',30,30))
#print(getMACD('2427'))
#print(getKD('2427'))

#代碼
def getFin(sid,a):
    table = pd.read_csv("catFin/"+str(sid) + str(a) +'.csv')
    table.columns
    data = []
    head = []
    for i in range(len(table.columns)):
        z = table.columns[i]
        head.append(z)
        small = []
        for j in range(len(table[z])):
            small.append(table[z][j])
        data.append(small)
    for i in range(8-len(data)):
        aa = []
        data.append(aa)
    for i in range(8-len(head)):
        aa = []
        head.append(aa)
    return head, data
#aa = getFin(2427,2)
#print(aa[1])
#print(len(aa[1]))