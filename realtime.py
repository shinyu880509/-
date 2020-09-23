from urllib.request import urlopen
import requests
import time
import json
import pandas
import sched

s = sched.scheduler(time.time, time.sleep)

today_url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_6214.tw"
data = json.loads(urlopen(today_url).read())

a = 0

if a == 0:
    columns = ['t','z','tv','v','o','h','l']
    df = pandas.DataFrame(data['msgArray'], columns = columns)
    df.columns = ['時間','當盤成交價','當盤成交量','累積成交量','開盤價','最高價','最低價']
    df.to_csv('catStock/test.csv', index = False,encoding = 'utf_8_sig')
    a == 1
else:
    columns = ['t','z','tv','v','o','h','l']
    df = pandas.DataFrame(data['msgArray'], columns = columns)
    df.to_csv('catStock/test.csv', mode = 'a', index = False, header = False, encoding = 'utf_8_sig')
