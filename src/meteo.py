#! /Users/audrius/Documents/VCSPython/py_scrape/bin/python3

import os
import re
import pandas as pd
from lxml import html
import requests
import matplotlib.pyplot as plt

# ----------------------------Scrape Data------------------------------------
url = 'https://www.meteo.lt'
page = requests.get(url)
# print(page.content)
tree = html.fromstring(page.content)
print(tree)
# ----------------------Read Data from Scraped HTML--------------------------
days = tree.xpath('//div[@class="day-wrap"]/h4/text()')
print(days)
date = tree.xpath('//div[@class="date"]/text()')
print(date)
temp = tree.xpath('//div[@class="day-wrap"]//div[@class="temprature"]/text()')
print(temp)
wind = tree.xpath('//div[@class="wind"]/text()')
print(wind)
# -----------------------Create Data Lists-----------------------------------
days_list = []
date_list = []
temp_list = []
wind_list = []
wind_speed = []
wind_speed_avg =[]
wind_dir = []
for i in days:
    days_list.append(i.strip())
print('Days: ', days_list)
for i in date:
    date_list.append(i.strip())
print('Dates: ', date_list)
for i in temp:
    value = re.match(r"^\d+", i.strip())
    temp_list.append(int(value.group())) # type: ignore
print('Temps: ', temp_list)
for i in wind:
    wind_list.append(i.strip())
print('Wind: ', wind_list)
for i in wind_list:
    split = i.split()
    if len(split) == 3:
        wind_speed.append(split[0])
        wind_dir.append(split[2])
print('Wind speed: ', wind_speed)
print('Wind dir: ', wind_dir)
for i, v in enumerate(wind_speed):
    wind_speed_avg.append((int(v[0]) + int(v[2])) / 2)
print('Wind speed avg: ', wind_speed_avg)
# --------------Create Data Frame and write it to File----------------
df = pd.DataFrame({
    "Data": date_list,
    "Sav_diena": days_list,
    "Temperatura (C)": temp_list,
    "Vejas_greitis": wind_speed,
    "Vejas_vidutinis": wind_speed_avg,
    "Vejas_kryptis": wind_dir
})
print(df)
# file_path = os.path.abspath('data')
# print(file_path)
df.to_csv("meteo.csv", index=False)
# ------------------------Draw Charts---------------------------------
plt.figure(figsize=(10, 6))
plt.plot(df["Data"], df["Temperatura (C)"], marker="o", linestyle="-", color="b")
plt.title("Temperatura per sav.")
plt.xlabel("Data")
plt.ylabel("Temp (C)")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 4))
plt.bar(df["Data"], df["Vejas_vidutinis"], color='r')
plt.title("Vidutinis vejo greitis per sav")
plt.xlabel("Data")
plt.ylabel("Vid vejo greitis (m/s)")
plt.grid(True)
plt.show()

wind_dir_counts = df["Vejas_kryptis"].value_counts()
w_labels = list(wind_dir_counts.index)
print(w_labels)
print(wind_dir_counts)
plt.figure(figsize=(6, 6))
plt.pie(wind_dir_counts, labels=w_labels, autopct='%1.1%', startangle=130)
plt.title("Vejo kryptis")
plt.show()
