import csv
import pandas as pd
import numpy as np
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
import keras
import datetime

def normalize(df):
    newdf= df.copy()
    min_max_scaler = preprocessing.MinMaxScaler()
    
    newdf['open'] = min_max_scaler.fit_transform(df.open.values.reshape(-1,1))
    newdf['low'] = min_max_scaler.fit_transform(df.low.values.reshape(-1,1))
    newdf['high'] = min_max_scaler.fit_transform(df.high.values.reshape(-1,1))
    newdf['Trading_turnover'] = min_max_scaler.fit_transform(df.Trading_turnover.values.reshape(-1,1))
    newdf['close'] = min_max_scaler.fit_transform(df.close.values.reshape(-1,1))
    newdf.drop(['date','stock_id','Trading_Volume','Trading_money','spread'], axis = 'columns', inplace = True)
    return newdf

def denormalize(df, norm_value):
    original_open = df['open'].values.reshape(-1,1)
    original_close = df['close'].values.reshape(-1,1)
    original_turnover = df['Trading_turnover'].values.reshape(-1,1)
    original_high = df['high'].values.reshape(-1,1)
    original_low = df['low'].values.reshape(-1,1)
    
    preopen = []
    preclose = []
    preturnover = []
    prehigh = []
    prelow = []
    
    for i in range(len(norm_value)):
        preopen.append(norm_value[i][0])
        preclose.append(norm_value[i][1])
        preturnover.append(norm_value[i][2])
        prehigh.append(norm_value[i][3])
        prelow.append(norm_value[i][4])
    
    pre_open = np.array(preopen)
    pre_close = np.array(preclose)
    pre_turnover = np.array(preturnover)
    pre_high = np.array(prehigh)
    pre_low = np.array(prelow)
    
    pre_open = pre_open.reshape(-1,1)
    pre_close = pre_close.reshape(-1,1)
    pre_turnover = pre_turnover.reshape(-1,1)
    pre_high = pre_high.reshape(-1,1)
    pre_low = pre_low.reshape(-1,1)
    
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_scaler.fit_transform(original_open)
    denorm_open = min_max_scaler.inverse_transform(pre_open)
    
    min_max_scaler.fit_transform(original_close)
    denorm_close = min_max_scaler.inverse_transform(pre_close)
    
    min_max_scaler.fit_transform(original_turnover)
    denorm_turnover = min_max_scaler.inverse_transform(pre_turnover)
    
    min_max_scaler.fit_transform(original_high)
    denorm_high = min_max_scaler.inverse_transform(pre_high)
    
    min_max_scaler.fit_transform(original_low)
    denorm_low = min_max_scaler.inverse_transform(pre_low)
    
    return denorm_open, denorm_close, denorm_turnover, denorm_high, denorm_low

def ex():
    stockid = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
    for a in range(len(stockid)):
        model = keras.models.load_model('test' + str(stockid[a]) + '.h5')
        data = pd.read_csv(str(stockid[a]) + '.csv')
        dataNor = normalize(data)
        day = 10
        d = 0
        if stockid[a] == "2480":
            day = 30
            
        #十天歷史資料
        for j in range(10):
            #print(j)
            if j == 0:
                cc = dataNor[-(day+1):]
            else:
                cc = dataNor[-(day+1+j):-j]
            dd = np.array(cc)
            errr = []
            rrr = []
            for i in range(30):
                inin = []
                inin.append(dd[i:-1].tolist())
                inin.append(dd[i+1:].tolist())
                aa = np.array(inin)

                pre = model.predict(aa)
                #print(pre)
                errr.append(pre[1].tolist())
                rrr.append(pre[0].tolist())
                z = []
                z = dd.tolist()
                z.append(pre[0].tolist())
                dd = np.array(z)
            den = denormalize(data, np.array(errr))
            en = denormalize(data, np.array(rrr))
            
            pr = []
            for k in range(len(den)):
                prr = []
                for i in range(len(den[0])):
                    aaaa = float((en[k][i] + den[k][i])/2)
                    if i%2 == 0:
                        prr.append(round(aaaa,2))
                    else:
                        prr.append(round(aaaa,2))
                
                pr.append(prr)
            
            re = []
            head = ['open', 'close', 'Trading_turnover', 'high', 'low']
            for i in range(30):
                aa = []
                for k in range(5):
                    aa.append(float(pr[k][i]))
                re.append(aa)
            #print(np.array(re))
            
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
            today = str(today).replace('-', '_')
            
            writerCSV = pd.DataFrame(columns = head, data=np.array(re))
            writerCSV.to_csv('preStock/'+ str(stockid[a]) + '/' + today +'.csv',encoding='utf-8', index = False)
    return