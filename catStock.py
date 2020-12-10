from FinMind.Data import Load
import requests
import csv
import pandas as pd
import urllib.request
import json,requests
#BeautifulSoup4 html5lib

def catStock():
    url = "https://api.finmindtrade.com/api/v3/data"
    dat = '2015-01-01'
    itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    for i in range(len(itStock)):
        parameter = {
            "dataset": "TaiwanStockPrice",
            "stock_id": itStock[i],
            "date": dat
        }
        stockID = itStock[i]
        resp = requests.get(url, params=parameter)
        data = resp.json()
        data = pd.DataFrame(data["data"])

        data['high'] = data['max']
        data['low'] = data['min']
        data.drop(['max','min'], axis = 'columns', inplace = True)

        stockDf = pd.DataFrame(data)
        stockDf.set_index('date', inplace = True)
        stockDf.to_csv('catStock/' + stockID + '.csv')
        
        csvfile = open('catStock/' + stockID +'.csv','r')
        jsonfile = open('catStock/' + stockID +'.json','w')
        namesss= pd.read_csv('catStock/' + stockID +'.csv')
        fieldnames1=namesss.columns

        aaaa=tuple(fieldnames1)
        reader = csv.DictReader(csvfile,aaaa)
        for row in reader:
            json.dump(row,jsonfile)
            jsonfile.write('\n')
        jsonfile.close()
        csvfile.close()
    return

def catStocktoday():
    itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    for i in range(len(itStock)):
        stockID = itStock[i]
        url =f"https://tw.stock.yahoo.com/q/ts?s={stockID}&t=50"
        stocktoday = pd.read_html(url, encoding='big-5')[3]
        stocktoday.to_csv('catStock/' + stockID + 'today.csv', header = 0 , index = 0, encoding = 'utf_8_sig')

        csvfile = open('catStock/' + stockID + 'today.csv','r', encoding = 'utf_8_sig')
        jsonfile = open('catStock/' + stockID + 'today.json','w', encoding = 'utf_8_sig')
        namesss= pd.read_csv('catStock/' + stockID + 'today.csv', encoding = 'utf_8_sig')
        fieldnames1=namesss.columns

        aaaa=tuple(fieldnames1)
        reader = csv.DictReader(csvfile,aaaa)
        for row in reader:
            json.dump(row,jsonfile)
            jsonfile.write('\n')
        jsonfile.close()
        csvfile.close()
    return

def catFin():
    itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    for a in range(len(itStock)):
        fin = [f"https://www.above.tw/json/TProStkFinance/CsRevenueChart?sym={itStock[a]}",
        f"https://www.above.tw/json/TProStkFinance/GrowupAbility?sym={itStock[a]}&s=YearQuarter:d",
        f"https://www.above.tw/json/TProStkFinance/DividendOverview?sym={itStock[a]}&s=Year:d",
        f"https://www.above.tw/json/TProStkFinance/ProfitBySym?sym={itStock[a]}&finance_type=YQ",
        f"https://www.above.tw/json/TProStkFinance/Capstreq?sym={itStock[a]}",
        f"https://www.above.tw/json/TProStkFinance/CashFlows?sym={itStock[a]}&s=YearQuarter:d",
        f"https://www.above.tw/json/TProStkFinance/SolvencyBySym?sym={itStock[a]}&finance_type=YQ",
        f"https://www.above.tw/json/TProStkFinance/Management?sym={itStock[a]}&s=YearQuarter:d"]
        #個股月營收 成長性分析 股利政策 獲利能力分析(季) 資本形成-股東權益(季) 現金分析(年) 償還能力分析(季) 經營能力分析(年)
        for b in range(len(fin)):
            url = fin[b]
            r = requests.get(url)
            l = r.json()
            head = l['cheaders']
            data = l['data']

            writerCSV = pd.DataFrame(columns = head, data=data)
            writerCSV.to_csv('catFin/'+ str(itStock[a]) + str(b) + '.csv',encoding='utf-8', index = False)

            csvfile = open('catFin/'+ str(itStock[a]) + str(b) + '.csv','r',encoding='utf-8')
            jsonfile = open('catFin/'+ str(itStock[a]) + str(b) + '.json','w',encoding='utf-8')
            namesss= pd.read_csv('catFin/'+ str(itStock[a]) + str(b) + '.csv',encoding='utf-8')
            fieldnames1=namesss.columns
            aaaa=tuple(fieldnames1)
            reader = csv.DictReader(csvfile,aaaa)
            for row in reader:
                json.dump(row,jsonfile)
                jsonfile.write('\n')
            jsonfile.close()
            csvfile.close()

def catAll():
    catFin()
    catStock()
    catStocktoday()