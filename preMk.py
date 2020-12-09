import os
import csv
import pandas as pd
import numpy as np
from FinMind.Data import Load
from sklearn import preprocessing
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
import keras
import matplotlib.pyplot as plt

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

def data_helper(df, time_frame):
    number_features = len(df.columns)
    datavalue = df
    datavalue = datavalue.values
    result = []

    for index in range( len(datavalue) - (time_frame+1) ):
        result.append(datavalue[index: index + (time_frame+1) ]) 

    result = np.array(result)
    number_train = round(result-30)
    x_train = result[:int(number_train), :-1] 
    y_train = result[:int(number_train), -1] 
    x_test = result[int(number_train):, :-1]
    y_test = result[int(number_train):, -1]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], number_features))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], number_features))  
    return [x_train, y_train, x_test, y_test]

def build_model(input_length, input_dim):
    d = 0.3
    model = Sequential()

    model.add(LSTM(32, input_shape=(input_length, input_dim), return_sequences=True))
    model.add(Dropout(d))
    model.add(LSTM(8, return_sequences=True))
    model.add(Dropout(d))
    model.add(LSTM(8, return_sequences=True))
    model.add(Dropout(d))
    model.add(LSTM(8, return_sequences=False))
    model.add(Dropout(d))
    
    model.add(Dense(8,kernel_initializer="uniform",activation='relu'))
    model.add(Dense(5,kernel_initializer="uniform",activation='linear'))

    model.compile(loss='mse',optimizer='adam', metrics=['accuracy'])

    return model

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

data = pd.read_csv('6214.csv')
day = 10

#正規化
foxconndf_norm= normalize(data)

#分割訓練資料
X_train, y_train, X_test, y_test = data_helper(foxconndf_norm, day)

#建立模型
model = build_model(day, 5)

#開始訓練
model.fit( X_train, y_train, batch_size=128, epochs=100, validation_split=0.1, verbose=1)

#儲存模型
model.save('test6214.h5')

#預測
pred = model.predict(X_test)

#還原
pred = model.predict(X_test)
denorm_pred = denormalize(data, pred)
denorm_ytest = denormalize(data, y_test)
denorm_X_test = denormalize(data, X_test)
cc = foxconndf_norm[-(day+1+30):-30]
dd = np.array(cc)
print(denormalize(data,dd))
errr = []
rrr = []
for i in range(30):
    inin = []
    inin.append(dd[i:-1].tolist())
    inin.append(dd[i+1:].tolist())
    aa = np.array(inin)
    
    pre = model.predict(aa)
    print(pre)
    errr.append(pre[1].tolist())
    rrr.append(pre[0].tolist())
    z = []
    z = dd.tolist()
    z.append(pre[0].tolist())
    dd = np.array(z)
den = denormalize(data, np.array(errr))
en = denormalize(data, np.array(rrr))

#圖表比較
for i in range(5):
    plt.plot(den[i],color='red', label='Prediction')
    plt.plot(en[i],color='orange', label='Prediction')
    plt.plot(denorm_ytest[i],color='blue', label='Answer')
    plt.plot(denorm_pred[i],color='green', label='Prediction')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()