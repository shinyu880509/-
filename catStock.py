from FinMind.Data import Load
import csv
import pandas as pd

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