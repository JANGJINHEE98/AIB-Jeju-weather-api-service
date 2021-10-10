import pandas as pd
import sqlite3

con = sqlite3.connect("/Users/zhenxi/Desktop/for_git/third_project/third_project_db.db")
cur = con.cursor()
weather_df = pd.read_sql("SELECT * FROM weather", con, index_col=None)
airport_df = pd.read_sql("SELECT * FROM airport", con, index_col=None)

# eda 
# 요일을 추가해 줄까요?

print(weather_df.isnull().sum())

