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

# ----------------------------Scrape Data--------------------
url = 'https://e-tar.lt/portal/lt/newLegalActs'
page = requests.get(url)
# print(page.content)
tree = html.fromstring(page.content)
print('----HTML Tree----\n', tree)
# ----------Read Data from Scraped HTML and create Data Table-------
td_title = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//td/a/text()')
del td_title[-1]
print('----Title----\n', len(td_title), td_title)
td_date_entry = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//td/span/text()')
print('Date_entry: ', len(td_date_entry), td_date_entry)
rows = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//tr')
print('----Table Rows----\n', rows)
table_data = []
for row in rows:
    cells = row.xpath('.//td/text()')
    table_data.append([cell.strip() for cell in cells])
print('----Table Data for DF-----\n: ', table_data)
# -------------------Create Data Frame and prepare data---------------------------
df_d = pd.DataFrame(table_data)
df = df_d.drop(df_d.columns[[7, 8]], axis=1)
df.drop(df.head(1).index, inplace=True) # drop first n rows
df.drop(df.tail(4).index,inplace=True) # drop last n rows
df.columns = ['ID', 'Legal_act_type', 'Author', 'Legal_act_id', 'Legal_act_number', 'Legal_act_date', 'Registry_date']
df['Date_entry'] = td_date_entry
df['Title'] = td_title
df['Author'] = df['Author'].str.replace('Priėmė\n                                    \n                                        ', '')
df['Legal_act_id'] = df['Legal_act_id'].str.replace('Identifikacinis kodas ', '')
df['Legal_act_date'] = pd.to_datetime(df['Legal_act_date'])
df['Registry_date'] = pd.to_datetime(df['Registry_date'])
df['Date_entry'] = pd.to_datetime(df['Date_entry'])
# ---------------Write DF to File and Read from it----------------
# df.to_csv("etar.csv", index=False)
# df = pd.read_csv("etar.csv")
# print(df)
# --------------------Explore Data Frame--------------------------
print('----Shape----\n', df.shape)
print('----Head----\n', df.head())
print('----Columns----\n', df.columns)
print('----Dtypes----\n', df.dtypes)
print('----Is None?----\n', df.isna().sum())
print('----Is Duplicated?----\n', df.loc[df.duplicated()])
# ---------------------Draw Pie---------------------------------
auth_counts = df["Author"].value_counts()
t_labels = list(auth_counts.index)
plt.figure(figsize=(8, 6))
plt.pie(auth_counts, labels=t_labels, autopct='%1.1f%%', startangle=130)
plt.title("Teises aktai pagal sudarytoja")
plt.show()

type_counts = df["Legal_act_type"].value_counts()
type_labels = list(type_counts.index)
plt.figure(figsize=(6, 6))
plt.pie(type_counts, labels=type_labels, autopct='%1.1f%%', startangle=130)
plt.title("Legal Act Types")
plt.show()

# ------------------------Draw Plot---------------------------------
# acts_counts = df["Legal_act_date"].dt.year.value_counts()
# plt.figure(figsize=(10, 6))
# plt.plot(df["Legal_act_date"], acts_counts, marker="o", linestyle="-", color="b")
# plt.title("Teises aktai pagal data")
# plt.xlabel("Data")
# plt.ylabel("Teises aktai")
# plt.grid(True)
# plt.show()