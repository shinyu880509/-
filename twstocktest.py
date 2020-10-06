import time
import pandas
import sched
import twstock
import os
import datetime

s = sched.scheduler(time.time, time.sleep)

def catStocktoday():
    itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    global realtime
    a = True
    while a :
        try:
            realtime = twstock.realtime.get(itStock)
            if realtime['success'] == True:
                a = False
        except:
            pass
            

    print(realtime)

    date = time.strftime('%Y%m%d')
    now = datetime.datetime.now()
    nowtime = now.strftime('%H:%M:%S')
    print(nowtime)
        

    for i in range(len(itStock)):
        stockID = itStock[i]
        stock = {**realtime[stockID]['info'],**realtime[stockID]['realtime']}
        columns = ['time','latest_trade_price','trade_volume','accumulate_trade_volume','open','high','low']
        df = pandas.DataFrame([stock], columns = columns, index = [0])
        target_file = f'catToday/{date}-{stockID}.csv'
        if os.path.exists(target_file):
            if realtime[stockID]['realtime']['latest_trade_price'] != '-' and realtime[stockID]['realtime']['trade_volume'] != '-':
                df.to_csv('catToday/' + date + '-' + stockID + '.csv', mode='a',header=False , index = False,encoding = 'utf_8_sig')
        else:
            if realtime[stockID]['realtime']['latest_trade_price'] != '-' and realtime[stockID]['realtime']['trade_volume'] != '-':
                df.to_csv('catToday/' + date + '-' + stockID + '.csv' , index = False,encoding = 'utf_8_sig')

    start_time = datetime.datetime.strptime(str(now.date())+'09:30', '%Y-%m-%d%H:%M')
    end_time =  datetime.datetime.strptime(str(now.date())+'13:30', '%Y-%m-%d%H:%M')

    if now >= start_time and now <= end_time:
        s.enter(3, 0, catStocktoday, ())

s.enter(5, 0, catStocktoday, ())
s.run()
