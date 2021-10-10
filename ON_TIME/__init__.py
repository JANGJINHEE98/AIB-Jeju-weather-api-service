from os import name
from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import joblib

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# <>안에 변수형을 정의하지 않으면 string 
@app.route('/result/<mmdd>/<day>')
def result(mmdd, day):
    # 모델 가져오기 
    model = joblib.load('pickled_model.pkl')
    # X 만들기 (predict(X)) 테이블명 weather_predict
    
    # 먼저 날씨데이터를 가져옵니다. (그날에 어떤 날씨일지 통계를 바탕으로 추출)
    con = sqlite3.connect("/Users/zhenxi/Desktop/for_git/third_project/AIB-Jeju-weather-api-service/last_db.db")
    
    # weather_predict는 dataframe
    weather_predict = pd.read_sql(f"SELECT * FROM weather_predict wp WHERE MD = {mmdd}", con, index_col=None)

    # 전처리 (원래는 one-hot 인코딩으로 처리했던 요일(범주형데이터)을 가내수공업으로 인코딩 해줬다. 더 좋은 방법이 있을까?)
    weather_predict = weather_predict.assign(day_Tuesday=[0], day_Monday=[0], day_Sunday=[0], day_Saturday=[0], day_Friday=[0], day_Thursday=[0], day_Wednesday=[0])
    days = ['Tuesday', 'Monday', 'Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday']	
    
    for i in days :
        if day == i :
            weather_predict[f'day_{i}'][0] = 1

    
    # M, D, MD 컬럼도 잘 만들어 줍니다. 
    m = int(mmdd[:2])
    d = int(mmdd[2:])

    weather_predict['M'] = weather_predict['M'][0] = m
    weather_predict['D'] = weather_predict['D'][0] = d

    # 컬럼 X형태로 정렬 혹시 몰라 다 복붙함..
    weather_predict = weather_predict.reindex(columns = ['averageTemperature', 'lowestTemperature',	'lowestTemperatureTime', 'highestTemperature', 'highestTemperatureTime', 'dailyRainfall', 'maximumWindSpeed',	'maximumWindSpeedTime', 'averageWindSpeed',	'maximumWindSpeedDirection', 'day_Tuesday',	'day_Monday', 'day_Sunday',	'day_Saturday', 'day_Friday', 'day_Thursday', 'day_Wednesday', 'M', 'D', 'MD'])

    weather_predict['MD'] = weather_predict['MD'].apply(pd.to_numeric)

    pred = model.predict(weather_predict)
######################################################
    # if 문으로 공항 혼잡 여부 반환하는거 추가해야함.  
    airport_status = '혼잡 혹은 원활 등으로 나올 수 있게 추가하기'

    con.close()
    return render_template('result.html', the_result=pred, airport_status = airport_status)
    

if __name__ == '__main__' :
    app.run(debug=True)


