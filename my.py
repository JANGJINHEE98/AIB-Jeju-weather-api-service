import joblib
from os import name
from flask import Flask, render_template, request
import pandas as pd
import sqlite3


print("----------------------------")

mmdd = '1011'
day = 'Tuesday'

# 모델 가져오기 
model = joblib.load('pickled_model.pkl')
# X 만들기 (predict(X)) 테이블명 weather_predict
con = sqlite3.connect("/Users/zhenxi/Desktop/for_git/third_project/AIB-Jeju-weather-api-service/last_db.db")
cur = con.cursor()
weather_predict = pd.read_sql(f"SELECT * FROM weather_predict wp WHERE MD = {mmdd}", con, index_col=None)
weather_predict
weather_predict = weather_predict.assign(day_Tuesday=[0], day_Monday=[0], day_Sunday=[0], day_Saturday=[0], day_Friday=[0], day_Thursday=[0], day_Wednesday=[0])
days = ['Tuesday', 'Monday', 'Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday']	
for i in days :
    if day == i :
        weather_predict[f'day_{i}'][0] = 1

m = int(mmdd[:2])
d = int(mmdd[2:])

weather_predict['M'] = weather_predict['M'][0] = m
weather_predict['D'] = weather_predict['D'][0] = d

weather_predict = weather_predict.reindex(columns = ['averageTemperature', 'lowestTemperature',	'lowestTemperatureTime', 'highestTemperature', 'highestTemperatureTime', 'dailyRainfall', 'maximumWindSpeed',	'maximumWindSpeedTime', 'averageWindSpeed',	'maximumWindSpeedDirection', 'day_Tuesday',	'day_Monday', 'day_Sunday',	'day_Saturday', 'day_Friday', 'day_Thursday', 'day_Wednesday', 'M', 'D', 'MD'])

weather_predict['MD'] = weather_predict['MD'].apply(pd.to_numeric)

pred = model.predict(weather_predict)
print(pred)
