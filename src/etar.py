#! /Users/audrius/Documents/VCSPython/py_scrape/bin/python3

import os
import re
import pandas as pd
import seaborn as sns
from lxml import html
import requests
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
pd.options.display.max_rows = 50
# print(sys.version)
print('Pandas version:', pd.__version__)
# ----------------------------Scrape Data--------------------
url = 'https://e-tar.lt/portal/lt/newLegalActs'
page = requests.get(url)
# print(page.content)
tree = html.fromstring(page.content)
print('----HTML Tree----\n', tree)
# ----------Read Data from Scraped HTML and create Data Table-------
td_title = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//td/a/text()')
print('----Title----\n', len(td_title), td_title)
td_date_entry_d = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//td/span/text()')
td_date_entry = td_date_entry_d + ['2024-06-22']
print('Date_entry: ', len(td_date_entry), td_date_entry)
rows = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//tr')
print('----Table Rows----\n', len(rows), rows)
table_data = []
for row in rows:
    cells = row.xpath('.//td/text()')
    if cells != []:
        table_data.append([cell.strip() for cell in cells])
print('----Table Data for DF-----\n', len(table_data))
for i in table_data:
    print(i)
# -------------------Create Data Frame and Prepare data---------------------------
df = pd.DataFrame(table_data)
df = df.drop(df.columns[[0, 7, 8]], axis=1)
# df.drop(df.head(1).index, inplace=True) # drop first n rows
# df.drop(df.tail(4).index,inplace=True) # drop last n rows
df.columns = ['Legal_act_type','Author','Legal_act_id','Legal_act_number','Legal_act_date','Registry_date']
df['Date_entry'] = td_date_entry
df['Title'] = td_title
df = df.rename(columns={'Legal_act_type':'Act_type', 'Author':'Act_issuer', 'Legal_act_id':'Act_identifier', 'Legal_act_number':'Act_number', 'Legal_act_date':'Act_date'})
df['Act_issuer'] = df['Act_issuer'].str.split(pat='\n').str[2].str.strip()
df['Act_identifier'] = df['Act_identifier'].str.replace('Identifikacinis kodas ', '')
df['Act_date'] = pd.to_datetime(df['Act_date'])
df['Registry_date'] = pd.to_datetime(df['Registry_date'])
df['Date_entry'] = pd.to_datetime(df['Date_entry'])
# ---------------Write DF to File and Read from it----------------
# df.to_csv("etar.csv", index=False)
# df = pd.read_csv("etar.csv")
# print(df)
# --------------------Explore Data Frame--------------------------
df['Act_number']
print('----Shape----\n', df.shape)
print('----Head----\n', df.head())
print('\n- Describe:\n', df.describe())
print('----Columns----\n', df.columns)
# print('----Column----\n', df.loc(6))
print('----Dtypes----\n', df.dtypes)
print('----Is Null?----\n', df.isnull().any())
# df = df.loc[~df['Act_type'].isna()] # Remove rows with NaN in Act_type
# df[df['Act_type'].isna()==1]
# df['Act_type'] = df['Act_type'].fillna(0)
# df[df['Act_type'].duplicated()==1]
# df[df['Act_type'].isin(['Del kazko', 'Del kitko'])]
# df.set_index(drop=True, inplace=True)
# df = df.set_index('ID')
# df = df[['Act_type', 'Act_issuer', 'Act_number', 'Act_date']] # Subsetting columns
# df = df.loc[df['Some_col'] > 1000] # Subsetting with loc
# df = df.query('Some_col > 1000') # Subsetting with query
# df.drop_duplicates()
print('----Is None?----\n', df.isna().sum())
print('----Is Duplicated?----\n', df.loc[df.duplicated()])
# ---------------------Draw Pie---------------------------------
auth_counts = df["Act_issuer"].value_counts()
t_labels = list(auth_counts.index)
plt.figure(figsize=(8, 6))
plt.pie(auth_counts, labels=t_labels, autopct='%1.1f%%', startangle=130)
plt.title("Teises aktai pagal sudarytoja")
plt.show()

type_counts = df["Act_type"].value_counts()
type_labels = list(type_counts.index)
plt.figure(figsize=(8, 6))
plt.pie(type_counts, labels=type_labels, autopct='%1.1f%%', startangle=130)
plt.title("Legal Act Types")
plt.show()

df['Act_date'].dt.date.value_counts().plot(figsize=(10, 6), bins=20, kind='hist')

# ------------------------Draw Plot---------------------------------
# acts_counts = df["Legal_act_date"].dt.year.value_counts()
# plt.figure(figsize=(10, 6))
# plt.plot(df["Legal_act_date"], acts_counts, marker="o", linestyle="-", color="b")
# plt.title("Teises aktai pagal data")
# plt.xlabel("Data")
# plt.ylabel("Teises aktai")
# plt.grid(True)
# plt.show()