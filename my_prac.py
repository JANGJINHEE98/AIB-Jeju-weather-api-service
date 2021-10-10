from os import replace
import requests
import json 
import bs4
import pandas as pd
import xml.etree.ElementTree as et
import datetime
from dateutil.relativedelta import relativedelta
from requests.api import get
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import sqlite3
from pandas import json_normalize

# url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
# params ={'serviceKey' : 'uzYSOme7OKws0nRWGgZbY34JV9C8b7aUyJRzxlD9lnNmbv2+AyiMZTck3saLblgw3kHZxMLByjsFAYRoN/JTBQ==',
#  'pageNo' : '1',
#  'numOfRows' : '10', 
#   'dataType' : 'JSON', 
#   'dataCd' : 'ASOS', 
#   'dateCd' : 'DAY', 
#   'startDt' : '20100101', 
#   'endDt' : '20100103', 
#   'stnIds' : '184' }

# response = requests.get(url, params=params)
# the_weather = json.loads(response.text)
# the_weather = the_weather['response']['body']['items']['item']
# weather_df = json_normalize(the_weather)

# print(weather_df)
