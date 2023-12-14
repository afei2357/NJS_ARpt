import configparser
import pandas as pd
config = configparser.ConfigParser()
config.read(u'./config/headers.ini',encoding='utf-8')
aheader = config['Atable']['headers']
bheader = config['Btable']['headers']

df = pd.read_excel('./input/表A.xlsx')
print(list(df.columns) )

print(aheader)
print(list(df.columns) == aheader.split('|'))
