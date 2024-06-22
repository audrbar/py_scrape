#! /Users/audrius/Documents/VCSPython/py_scrape/bin/python3

import re
import pandas as pd
from lxml import html
import requests
import matplotlib.pyplot as plt

# ----------------------------Scrape Data------------------------------------
url = 'https://www.meteo.lt/prognozes/lietuvos-miestai/?area=vilnius'
page = requests.get(url)
# print(page.content)
tree = html.fromstring(page.content)
print('Tree: ', tree)
# ----------------------Read Data from Scraped HTML--------------------------
days = tree.xpath('//div[@class="days"]//div[@class="date"]/text()')
print('Days: ', days)
td_headers = tree.xpath('//div[@class="tablewrap"]//table//th/text()')
del td_headers[9:]
del td_headers[1]
del td_headers[3]
print('Headers', td_headers)
td_values = tree.xpath('//div[@class="tablewrap"]//table//td/text()')
# print(td_values)
rows = tree.xpath('//div[@class="tablewrap"]//table//tr')
# print(rows)
table_data = []
for row in rows:
    cells = row.xpath('.//td/text()')
    table_data.append([cell.strip() for cell in cells])
print('Table for data frame: ', table_data)
# --------------Create Data Frame and write it to File----------------
df = pd.DataFrame(table_data)
# print('Data Frame:\n', df)
# ----------------Preparing data for charts and save DF---------------
df_t = df.drop(df.columns[[1, 2, 4, 5, 6]], axis=1)
df_t.columns = td_headers
df_t.dropna(subset=['Laikas'], inplace=True)
print('Data Frame:\n', df_t)
df_t.to_csv("prognoze.csv", index=False)
# ------------------------Draw Chart---------------------------------
df_s = df_t.drop(df_t.index[23:])
plt.figure(figsize=(10, 6))
plt.plot(df_s["Laikas"], df_s["Temperatūra"], marker="o", linestyle="-", color="b")
plt.title("Temperatura per sav.")
plt.xlabel("Laikas")
plt.ylabel("Temp (C)")
plt.grid(True)
plt.show()
