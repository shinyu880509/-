from FinMind.Data import Load
import csv
import pandas as pd
import urllib.request
import json,requests
#BeautifulSoup4 html5lib

def catStock():
    dat = '2015-01-01'
    itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    for i in range(len(itStock)):
        stockID = itStock[i]
        TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
        data = Load.FinData(dataset = 'TaiwanStockPrice',select = stockID,date = dat)

        data['high'] = data['max']
        data['low'] = data['min']
        data.drop(['max','min'], axis = 'columns', inplace = True)

        stockDf = pd.DataFrame(data)
        stockDf.set_index('date', inplace = True)
        stockDf.to_csv('catStock/' + stockID + '.csv')
    return

def catStocktoday():
    itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    for i in range(len(itStock)):
        stockID = itStock[i]
        url =f"https://tw.stock.yahoo.com/q/ts?s={stockID}&t=50"
        stocktoday = pd.read_html(url, encoding='big-5')[3]
        stocktoday.to_csv('catStock/' + stockID + 'today.csv', header = 0 , index = 0, encoding = 'utf_8_sig')
    return
def catFin():
    itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    for a in range(len(itStock)):
        fin = [f"https://www.above.tw/json/StocksFinance_sym_score?&sym={itStock[a]}&psize=10&p=1&show=YM_Date;CsMRevenue;CsMOM_pct;CsQOQ_pct;CsYOY_pct;AccsYOY_pct",
        f"https://www.above.tw/json/StocksFinance_GrowthAnly?&sym={itStock[a]}&psize=10&p=1&show=Date;CsMRevenue;CsMOM_pct;CsYOY_pct;AccsYOY_pct",
        f"https://www.above.tw/json/StocksFinance_Divpolicy?&sym={itStock[a]}&psize=10&p=1&show=Date;NetProfit;DistrNetProfit;CashDiv_Earn;TotalCashDivAmt;StkDiv_CapInc_Earn;StkDiv_LegalReserve_CapSurplus;TotalStkDivShare",
        f"https://www.above.tw/json/StocksFinance_ProfitByQr?&sym={itStock[a]}&psize=10&p=1&show=Date;Revenue;GrossMarginPer;OpearatingMarginPer;PretaxProfitMargin;ProfitMargin",
        f"https://www.above.tw/json/StocksFinance_Capstreq?&sym={itStock[a]}&psize=10&p=1&show=Date;ShareCap;CapSurplus;RetainedEarning",
        f"https://www.above.tw/json/StocksFinance_Cashratio?&sym={itStock[a]}&psize=10&p=1&show=Date;CashFlowRatio;CashFlowAdequacyRatio;CashReinvestmentRatio",
        f"https://www.above.tw/json/StocksFinance_SolvencyBySym?&sym={itStock[a]}&psize=10&p=1&show=Date;RatFlow;RatSpd",
        f"https://www.above.tw/json/StocksFinance_Oper?&sym={itStock[a]}&psize=10&p=1&show=Date;AvgCollectionDays"]
        #個股月營收 成長性分析 股利政策 獲利能力分析(季) 資本形成-股東權益(季) 現金分析(年) 償還能力分析(季) 經營能力分析(年)
        for b in range(len(fin)):
            url = fin[b]
            r = requests.get(url)
            l = r.json()
            head = l['cheaders']
            data = l['data']
            writerCSV = pd.DataFrame(columns = head, data=data)
            writerCSV.to_csv('catFin/'+ str(itStock[a]) + str(b) + '.csv',encoding='utf-8', index = False)