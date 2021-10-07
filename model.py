import pandas as pd
from pandas import Series, DataFrame
import sqlite3

con = sqlite3.connect("/Users/zhenxi/Desktop/for_git/third_project/third_project_db.db")
cur = con.cursor()
df = pd.read_sql("SELECT * FROM airport", con, index_col=None)
con.close()
print(df)
