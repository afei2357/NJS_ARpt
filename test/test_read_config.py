import configparser
import pandas as pd
config = configparser.ConfigParser()
config.read(u'./config/headers.ini',encoding='utf-8')
aheader = config['Atable']['headers']
bheader = config['Btable']['headers']

df = pd.read_excel('./input/表A.xlsx')
# print(list(df.columns) )
# print(aheader)
# print(list(df.columns) == aheader.split('|'))


import sqlite3
with sqlite3.connect('./db/database.db') as con:
    c = con.cursor()
    df = pd.read_sql('select * from patient_info' ,con=con)
    print(df)
    df.to_excel('out_info.xlsx',index=False)
