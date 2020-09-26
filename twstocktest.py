import time
import pandas
import sched
import twstock


#s = sched.scheduler(time.time, time.sleep)

itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
realtime = twstock.realtime.get(itStock)

for i in range(len(itStock)):
    stockID = itStock[i]
    stock = {**realtime[stockID]['info'],**realtime[stockID]['realtime']}
    columns = ['time','latest_trade_price','trade_volume','accumulate_trade_volume','open','high','low']
    df = pandas.DataFrame([stock], columns = columns, index = [0])
    df.to_csv('catStock/' + stockID + 'test.csv', index = False,encoding = 'utf_8_sig')

#time.sleep(5)

