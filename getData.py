import pandas as pd
import csv
import numpy as np
import datetime
import time

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

def getLive(a):
    date = time.strftime('%Y%m%d')
    try:
        table = pd.read_csv("catToday/"+ date +"-"+ a +'.csv')
        date = np.array(table.time)
        datelist = date.tolist()
        for i in range(len(date)):
            aa = datelist[i].split(" ")
            datelist[i] = aa[1]
        price = np.array(table.latest_trade_price)
        pricelist = price.tolist()
        trans = np.array(table.trade_volume)
        translist = trans.tolist()
        high = np.array(table.high)
        high = high.tolist()
        low = np.array(table.low)
        low = low.tolist()
        op = np.array(table.open)
        op = op.tolist()
        aaa = []
        aaa.append(op[len(op)-1])
        aaa.append(high[len(high)-1])
        aaa.append(low[len(low)-1])
        aaa.append(pricelist[len(pricelist)-1])
        aaa.append(translist[len(translist)-1])
        aaa.append(datelist[len(datelist)-1])
        print("aaa")
        return datelist, pricelist, translist, aaa

    except:
        print("vvv")
        return "error"
    

def getToday():
    return datetime.date.today()

def getNewsS(a,i):
    table = pd.read_csv("news/"+ a +'.csv')
    table = table.sort_values(by=['日期'], ascending=False)
    table = table.reset_index(drop=True)
    return table.head(i)

def getNews(a):
    table = pd.read_csv("news/"+ a +'.csv')
    table = table.sort_values(by=['日期'], ascending=False)
    table = table.reset_index(drop=True)
    return table

def getDay(a):
    startday = a
    day = []
    d = 0
    for i in range(30):
        z = startday + datetime.timedelta(days=d)
        day.append(str(z).replace("-", "-"))
        if z.weekday() == 4:
            d += 3
        else:
            d += 1
        
    return day
'''zz = getDay(datetime.date.today())
print(zz)'''

def getPreDate(today, ago):
    d = 0
    re = []
    for i in range(ago):
        today = datetime.date.today() - datetime.timedelta(days=d)
        wee = today.weekday()
        if wee == 0:
            d+=3
        elif wee == 6:
            d+=2
        else:
            d+=1
        today = datetime.date.today() - datetime.timedelta(days=d)
        wee = today.weekday()
        re.append(today)
    return re

#股票代碼
def getPre(a, data, date):
    #table = pd.read_csv("preStock/"+ a + "/" + str(data) +'.csv')######################################################
    table = pd.read_csv("preStock/"+ a + "/2020_10_05.csv")
    date = getDay(date)
    #print(date)
    #date = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
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

def getPreByDay(a, date):
    
    preDataDate = getPreDate(getToday(), date)
    print(type(preDataDate))
    re = []
    ree = []
    for i in range(len(preDataDate)):
        s = str(preDataDate[i]).replace("-", "_")
        dat = getPre(a, s, preDataDate[i])
        re.append(dat)
        ree.append(getRecommend(a,dat, i, preDataDate[i]))
    return re, ree
#for i in range(10):
#print(getPreByDay("2427", 5))

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

def getPreKD(a):
    csv = getCsv(a)
    clo = csv[1][-10:]
    hi = csv[5][-19:]
    lo = csv[6][-39:]
    aa = getPre(a)
    clo = clo + aa[1]
    hi = hi + aa[2]
    lo = lo + aa[3]
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
    return dif[-30:],macd[-30:]

def getPreMACD(a):
    csv = getCsv(a)
    clo = csv[1][-34:]
    aa = getPre(a, 0)
    clo = clo + aa[1]
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
    return dif[-30:],macd[-30:]

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

def getPreBIAS(a, long):
    csv = getCsv(a)
    days = [6,12,24,72]
    clo = csv[1][-(days[long]-1):]
    aa = getPre(a)
    clo = clo + aa[1]
    bias = []
    re = []

    for i in range(len(aa[1])):
        ema30 = ema(clo[i:days[long]+i],days[long])
        zbias = ((clo[days[long]-1+i]-ema30)/ema30)*100
        bias.append(round(zbias,2))
        z = []
        if long == 3 and (bias[i] <= -11 or bias[i] >= 11):
            z = [clo[days[long]-1+i],bias[i]]
            re.append(z)
        elif long == 2 and (bias[i] <= -7 or bias[i] >= 8):
            z = [clo[days[long]-1+i],bias[i]]
            re.append(z)
        elif long == 1 and (bias[i] <= -4.5 or bias[i] >= 5):
            z = [clo[days[long]-1+i],bias[i]]
            re.append(z)
        elif long == 0 and (bias[i] <= -3 or bias[i] >= 3.5):
            z = [clo[days[long]-1+i],bias[i]]
            re.append(z)
    return bias,re

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
def getPreRSI(a, date, ago):
    csv = getCsv(a)
    days = 30
    if ago == 0:
        clo = csv[1][-(days):]
    else:
        clo = csv[1][-(days + ago):-ago]
    aa = date[1]
    clo = clo + aa
    change = []
    rsi = []

    for i in range(len(clo)-1):
        z = clo[i+1] - clo[i]
        change.append(z)
    for i in range(len(aa)):
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
#print(getPreRSI('2427',30))
#print(getRSI('2453',30,30))

def getRecommend(a, data, ago, date):
    pre = getPreRSI(a, data, ago)
    increase = []
    decrease = []
    no = []
    re = ""
    nd = []
    nnd = []
    rnd = ""
    nc = []
    nnc = []
    rnc = ""
    for i in range(len(pre)):
        day = getDay(date)
        if pre[i]>70:
            decrease.append(str(pre[i]))
            nd.append(i)
            nnd.append(day[i])
        elif pre[i]<30:
            increase.append(str(pre[i]))
            nc.append(i)
            nnc.append(day[i])
        else:
            no.append(str(pre[i]))
    
    for i in range(len(nd)):
        if i == 0:
            rnd = str(nnd[i])
        elif nd[i]-nd[i-1] > 3:
            rnd += "、" + str(nnd[i])
    for i in range(len(nc)):
        if i == 0:
            rnc = str(nnc[i])
        elif nc[i]-nc[i-1] > 3:
            rnc += "、" + str(nnc[i])

    if len(no) > len(pre)-5:
        re += "未來股價的漲跌幅幅度較小，若要考慮進場或出場可以再觀望一到二個星期"
    elif len(no) <= len(pre)-5:
        re += "未來股價的高低點陣動相對較大，建議近期如要交易可多加關注每日的股市資訊"

    if len(decrease) > 0:
        if len(decrease) > len(increase):
            re += "，預計會於" + rnd + "的前後股價將可能開始回溫，持續下跌的機會較低"
            if len(increase) > 0:
                re += "，而" + rnc + "則可能為近期內價格成長的巔峰"
        elif len(decrease) < len(increase):
            re += "，在" + rnc + "附近的日子裡，將會出現近期內股價的高點，很難再有新的突破，而在" + rnd + "則可能是股價停指下跌的信號"
        elif len(decrease) == len(increase):
            re += "，由於漲跌幅的陣動很大，股價較不穩定，進出場的風險較高，於" + rnc + "附近會出現高點，" + rnd + "會出現低點"

    if len(increase) > 0:
        if len(increase) > len(decrease):
            re += "，預測表示" + rnc + "前後股價將會來到高點，之後下跌的機會相較於上漲還要高"
            if len(decrease) > 0:
                re += "，而" + rnd + "則可能會是價格開始上漲的起點"
        elif len(increase) < len(decrease):
            re += "，在" + rnc + "附近的日子裡，將會出現近期內股價的低點，比起下跌更有上漲的機會，而在" + rnc + "則是這段時間內的股價巔峰"
        elif len(decrease) == len(increase):
            re += "，由於漲跌幅的陣動很大，股價較不穩定，進出場的風險較高，於" + rnc + "附近會出現高點，" + rnd + "會出現低點"

    re += "，可從近期的成交價格與技術指標來決定將來的投資策略。"
    return re, pre
#print(getRecommend("2427", 30))

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
    data = []
    head = []
    for i in range(len(table.columns)):
        z = table.columns[i]
        head.append(z)
        small = []
        for j in range(len(table[z])):
            zz = str(table[z][j])
            zz = zz.split('%')
            if str(table[z][j])=='nan':
                small.append(0)
            elif len(zz) == 2:
                small.append(zz[0])
            else:
                small.append(table[z][j])
        data.append(small)
    for i in range(8-len(data)):
        aa = []
        data.append(aa)
    for i in range(8-len(head)):
        aa = []
        head.append(aa)
    return head, data
'''aa = getFin(2427,0)
print(aa[1][1])
print(len(aa))'''

def getAllFin(sid):
    re = []
    for i in range(8):
        re.append( getFin(sid,i))
    return re
#aa = getAllFin("2427")

print(len(getPreByDay("2427", 10)[1][0]))