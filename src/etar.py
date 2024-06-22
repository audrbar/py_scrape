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
pd.options.display.max_rows = 200
# --------------------------------Scrape Data---------------------------------
# options = webdriver.ChromeOptions()
# # options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)
# driver.get("https://e-tar.lt/portal/lt/newLegalActs")
# time.sleep(5)
# page = driver.page_source
# print(page)

url = 'https://e-tar.lt/portal/lt/newLegalActs'
page = requests.get(url)
# print(page.content)
tree = html.fromstring(page.content)
print(tree)
headers = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//th/span/text()')
del headers[7:]
print(headers)
td_values = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//td/text()')
print (td_values)
rows = tree.xpath('//div[@class="ui-datatable-tablewrapper"]//table//tr')
print(rows)
table_data = []
for row in rows:
    cells = row.xpath('.//td/text()')
    table_data.append([cell.strip() for cell in cells])
print(table_data)
df = pd.DataFrame(table_data)
# df.columns = headers
print(df.head(300).to_string())
print(df.isna().sum())
