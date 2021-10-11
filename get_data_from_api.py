import requests
import json 
import pandas as pd
import xml.etree.ElementTree as et
import datetime
from dateutil.relativedelta import relativedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import sqlite3

from pandas import json_normalize

day1 = datetime.date(2020, 1, 1) # 코드 작성 시점 부터 900일 가량의 날씨 데이터 수집을 하려고 했으나, 인덱스 에러로 20200101부터로 수정

# 날씨를 얻는 함수 
def get_weather(date) :
    weather_key = '_787o5o7t5objr7b8o_rjct7rb3p7788'
    date = date.strftime('%Y%m%d')
    weather_url = f'https://open.jejudatahub.net/api/proxy/1aD5taat1attaa51Db1511b51ab9Da19/{weather_key}?searchDate={date}'
    raw_data = requests.get(weather_url)
    the_weather = json.loads(raw_data.text)
    return the_weather['data'][4]

weather_data_list = []
for i in range(900) :
    day1 = day1 - relativedelta(days=1)
    weather_data_list.append(get_weather(day1))

weather_json_data = weather_data_list
weather_df = json_normalize(weather_json_data) # json 파일을 dataframe 형식으로 바꿔줌

# print(weather_df)

day2 = datetime.date(2020, 1, 1) # day1 초기화, 편의상 day2라고 변수명 설정

def get_airport_info(date):
    date = date.strftime('%Y%m%d')
    url = 'http://openapi.airport.co.kr/service/rest/dailyExpectPassenger/dailyExpectPassenger'
    queryParams = '?' + \
        urlencode({ quote_plus('schDate') : date, 
        quote_plus('schHH') : '22',
        quote_plus('schAirport') : 'CJU', 
        quote_plus('schTof') : 'I', 
        quote_plus('serviceKey') : 'uzYSOme7OKws0nRWGgZbY34JV9C8b7aUyJRzxlD9lnNmbv2+AyiMZTck3saLblgw3kHZxMLByjsFAYRoN/JTBQ==' })

    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()

    root = et.fromstring(response_body)

    item_dict = {}

    for item in root.iter('item'):
        item_dict['airport'] = item.find('arp').text
        item_dict['date'] = item.find('sdt').text
        item_dict['pcg'] = item.find('pcg').text # pcg : 단체 손님
        item_dict['pct'] = item.find('pct').text # pct : 개인 손님
        item_dict['tof'] = item.find('tof').text # 
    return item_dict

airport_df = pd.DataFrame()
for i in range(900) :
    day2 = day2 - relativedelta(days=1)
    airport_df = airport_df.append(get_airport_info(day2), ignore_index=True)
    
# print(airport_df)

# [참고] 여기에서는 third_project_db에 데이터를 담았으나, 나중에 last_db로 수정됨.

con = sqlite3.connect("/Users/zhenxi/Desktop/for_git/third_project/third_project_db.db")
cur = con.cursor()
weather_df.to_sql('weather', con, if_exists='replace')
airport_df.to_sql('airport', con, if_exists='replace')
con.close()



