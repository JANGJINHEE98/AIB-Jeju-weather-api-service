import pandas as pd
import xml.etree.ElementTree as et
import datetime
from dateutil.relativedelta import relativedelta
import requests
import json 
import bs4
from requests.api import get
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

def plz(date):
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
        item_dict['tof'] = item.find('tof').text # 혼잡 여부 / I : 여유, Y : 혼잡
    
    return item_dict

# airport_df = pd.DataFrame()
# airport_df = airport_df.append(item_dict, ignore_index=True)


airport_df = pd.DataFrame()
for i in range(3) :
    now = datetime.date(2020, 1, 1) # 코드 작성 시점 부터 900일 가량의 날씨 데이터 수집을 하려고 했으나, 인덱스 에러로 20200101부터로 수정
    day_before_now = now - relativedelta(days=1)
    airport_df = airport_df.append(plz(day_before_now), ignore_index=True)
    
print(airport_df)
    
# date = 20200101

# url = 'http://openapi.airport.co.kr/service/rest/dailyExpectPassenger/dailyExpectPassenger'
# queryParams = '?' + \
#     urlencode({ quote_plus('schDate') : date, 
#     quote_plus('schHH') : '22',
#     quote_plus('schAirport') : 'CJU', 
#     quote_plus('schTof') : 'I', 
#     quote_plus('serviceKey') : 'uzYSOme7OKws0nRWGgZbY34JV9C8b7aUyJRzxlD9lnNmbv2+AyiMZTck3saLblgw3kHZxMLByjsFAYRoN/JTBQ==' })

# request = Request(url + queryParams)
# request.get_method = lambda: 'GET'
# response_body = urlopen(request).read()

# root = et.fromstring(response_body)


# for item in root.iter('item'):
#     item_dict = {}
#     item_dict['airport'] = item.find('arp').text
#     item_dict['date'] = item.find('sdt').text
#     item_dict['pcg'] = item.find('pcg').text # pcg : 단체 손님
#     item_dict['pct'] = item.find('pct').text # pct : 개인 손님
#     item_dict['tof'] = item.find('tof').text # 혼잡 여부 / I : 여유, Y : 혼잡
   
# print(item_dict)


# airport_df = pd.DataFrame()
# airport_df = airport_df.append(item_dict, ignore_index=True)