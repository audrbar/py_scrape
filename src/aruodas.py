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

# ----------------------------Scrape Data--------------------
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://www.aruodas.lt/sklypai-pardavimui/")
time.sleep(5)
page = driver.page_source
# -------------------------Read Data from File----------------
# driver = webdriver.Chrome()
# file_path = os.path.abspath('aruodas.html')
# file_url = f'file://{file_path}'
# print(file_url)
# driver.get(file_url)
# ---------------------Read Data from Scraped HTML-----------
locations = driver.find_elements(By.CLASS_NAME, 'list-adress-v2')
# print(addresses)
locations_list = []
for location in locations:
    locations_list.append(location.text)
del locations_list[:2]
temp = []
town_list = []
town_list_d = []

for item in locations_list:
    temp = item.split("\n")
    town_list_d.append(temp[0])

for item in town_list_d:
    temp = item.split(',')
    town_list.append(temp[0])
# print('Location: ', locations_list)
print('Town: ', town_list)

prices_d = driver.find_elements(By.CLASS_NAME, 'list-item-price-v2')
price_list = []
for item in prices_d:
    stripped = item.text.strip()
    stripped_s = stripped[:-2]
    price_list.append(stripped_s)
print('Prices: ', price_list)

prices_pm_d = driver.find_elements(By.CLASS_NAME, 'price-pm-v2')
price_pm_list = []
for item in prices_pm_d:
    stripped = item.text.strip()
    split = stripped.split('€')
    price_pm_list.append(split[0])
print('Prices_pm: ', price_pm_list)

area_d = driver.find_elements(By.CLASS_NAME, 'list-detail-v2')
area_list_d = []
for item in area_d:
    area_list_d.append(item.text)
area_list = area_list_d[0::2]
type_list = area_list_d[1::2]
print('Area: ', area_list)
print('Type: ', type_list)
# -------------Create Data Frame and write it to File-------------
df = pd.DataFrame({
    'Prices': price_list,
    'Prices_pm': price_pm_list,
    'Area': area_list,
    'Type': type_list,
    'Town': town_list
})
df.to_csv("aruodas_first.csv")
print(df)
# -----------Read Data Frame from File and Explore it-------------
df_d = pd.read_csv("aruodas_first.csv")
# print(df_d)
df = df_d.drop(df_d.columns[[0]], axis=1)
print('----Shape----\n', df.shape)
print('----Head----\n', df.head(5))
print('----Columns----\n', df.columns)
print('----Dtypes----\n', df.dtypes)
print('----Is None?----\n', df.isna().sum())
print('----Is Duplicated?----\n', df.loc[df.duplicated()])
# ------------Data Preparation-----------------------------------
df['Prices'] = df['Prices'].str.strip()
df['Prices_pm'] = df['Prices_pm'].str.strip()
df["Prices"] = df['Prices'].str.replace(r'\s+', '', regex=True)
df["Prices_pm"] = df['Prices_pm'].str.replace(r'\s+', '', regex=True)
df['Prices'] = df['Prices'].astype(int)
df['Prices_pm'] = df['Prices_pm'].astype(int)
# df['Prices_pm'] = df['Prices_pm']str.replace.astype(int)

print('----Dtypes refactored----\n', df.dtypes)
print('Data Frame Prepared:\n', df)
print('------------And magic begins: Charts----------------\n')
# ---------------------Draw Pie---------------------------------
town_counts = df["Town"].value_counts()
t_labels = list(town_counts.index)
plt.figure(figsize=(8, 6))
plt.pie(town_counts, labels=t_labels, autopct='%1.1f%%', startangle=130)
plt.title("Pasiulymu kiekis pagal vietove")
plt.show()
# ------------------Draw Bar-----------------------------------
plt.figure(figsize=(10, 6))
plt.barh(df["Type"], df["Prices"], color='orange')
plt.title("Zemes paskirtis vs objekto kaina")
plt.xlabel("Objekto kaina (Eur)")
plt.ylabel("Zemes paskirtis")
plt.show()
# --------------------Draw Histogram----------------------------
price_pm_counts = df["Prices_pm"]
plt.figure(figsize=(6, 6))
plt.hist(price_pm_counts)
plt.title("Pasiulymu kiekis pagal vieneto kaina")
plt.xlabel("Kaina uz ara (Eur)")
plt.ylabel("Kiekis (vnt.)")
plt.show()
# -------------------Draw Scatter-----------------------------
plt.figure(figsize=(10, 6))
plt.scatter(df['Prices'], df['Type'], c='blue')
plt.title("Vieneto kaina vs zemes paskirtis")
plt.xlabel("Objekto kaina (Eur)")
plt.ylabel("Zemes paskirtis")
plt.show()
# ------------------Draw Scatter Seaborn---------------------
plt.figure(figsize=(10, 6))
ax = sns.scatterplot(x='Prices_pm', y='Type', hue='Town', data=df)
ax.set_title('Vieneto kaina vs zemes paskirtis vs vietove')
plt.show()
# ------------------Draw Pair plot Seaborn-------------------
sns.pairplot(df)
plt.show()
