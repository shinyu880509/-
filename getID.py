def getName(id):
    stockID = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    stockName = ['2427三商電','2453凌群' ,'2468華經' ,'2471資通' ,'2480敦陽' ,'3029零壹' ,'3130一零四' ,'4994傳奇' ,'5203訊連' ,'6112聚碩' ,'6183關貿' ,'6214精誠']
    for i in range(len(stockID)):
        if id == stockID[i]:
            return stockName[i]

def check(idd):
    stockID = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    c = 0
    for i in range(len(stockID)):
        if idd == stockID[i]:
            c = 1
    return c
