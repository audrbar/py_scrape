#! /Users/audrius/Documents/VCSPython/py_scrape/bin/python3

import os
import re
import pandas as pd
import seaborn as sns
from lxml import html
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

print('\n-------------------1. Scrape Data----------------------')
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://www.aruodas.lt/sklypai-pardavimui/")
time.sleep(5)
page = driver.page_source
print('- Done!')

print('\n----------2. Write to File and Read from it-----------')
# driver = webdriver.Chrome()
# file_path = os.path.abspath('aruodas_raw.html')
# file_url = f'file://{file_path}'
# print(file_url)
# driver.get(file_url)
print('- Not this time.')

print('\n--------------3. Read Data from Scraped HTML-------------')
locations = driver.find_elements(By.CLASS_NAME, 'list-adress-v2')
print('- Locations Obj (len:', len(locations), ')', locations)
area_overall = driver.find_elements(By.CLASS_NAME, 'list-AreaOverall-v2')
print('- Area Overall Obj (len:', len(area_overall), ')', area_overall)
intendance = driver.find_elements(By.CLASS_NAME, 'list-Intendances-v2')
print('- Intendance Obj (len:', len(intendance), ')', intendance)

print('\n------------------4. Make Data Lists------------------')
locations_list = []
for item in locations:
    locations_list.append(item.text.strip())
print('- Locations List (len:', len(locations_list), ')', locations_list)
area_overall_list = []
for item in area_overall:
    area_overall_list.append(item.text.strip())
print('- Area Overall List (len:', len(area_overall_list), ')', area_overall_list)
intendance_list = []
for item in intendance:
    intendance_list.append(item.text.strip())
print('- Intendance List (len:', len(intendance_list), ')', intendance_list)

print('\n-------------5. Create Awesome Data Frame-----------------')
df = pd.DataFrame({
    'Location': locations_list,
    'Intendance':intendance_list,
    'Area_Overall':area_overall_list
})
print('\n- Data Frame:\n', df.head(10))

print('\n---------6. Write Data Frame to file and Read it-----------')
# df.to_csv("aruodas_df.csv", index=False)
# df = pd.read_csv("aruodas_df.csv")
print('- Not this time.')

print('\n---------7. Prepare Data Frame for analysis--------------')
df = df.drop(df.head(2).index) # drop first n rows
df['Discount'] = df['Location'].str.split(pat='\n').str[2].str.strip()
df['Price (€)'] = df['Location'].str.split(pat='\n').str[-2].str.strip()
df['Price (€/a)'] = df['Location'].str.split(pat='\n').str[-1].str.strip()
df['Location'] = df['Location'].str.split(pat='\n').str[0].str.split(pat=',').str[0].str.strip()
df['Area_Overall'] = pd.to_numeric(df['Area_Overall'].astype('str'))
df['Price (€)'] = df['Price (€)'].str.split(pat='€').str[0].str.replace(r'\s+', '', regex=True).astype(int)
df['Price (€/a)'] = df['Price (€/a)'].str.split(pat='€').str[0].str.replace(r'\s+', '', regex=True).astype(int)
df['Discount'] = df['Discount'].str.replace(r'(^.*€.*$)', '0%', regex=True).str.replace(r'%', '', regex=True).str.split(' ').str[-1].str.replace(',', '.').astype(float)

print('\n----------------8. Explore Data Frame--------------------')
print('\n- Shape: ', df.shape)
print('\n- Head:\n', df.head())
print('\n- Describe:\n', df.describe())
print('\n- Columns:\n', df.columns)
print('\n- Dtypes:\n', df.dtypes)
print('\n- Is None?\n', df.isna().sum())
print('\n- Is Duplicated?\n', df.loc[df.duplicated()])
print('\n- Is Null?\n', df.isnull().any())

print('\n------------9. And magic begins: Draw Charts-------------')

# ------------------Draw Pie-----------------------------------
area_count = df["Location"].value_counts()
t_labels = list(area_count.index)
plt.figure(figsize=(8, 6))
plt.pie(area_count, labels=t_labels, autopct='%1.1f%%', startangle=130)
plt.title("Pasiulymu kiekis pagal vietove, vnt.")
plt.show()

# ------------------Draw Bar-----------------------------------
plt.figure(figsize=(10, 6))
plt.barh(df["Intendance"], df["Price (€/a)"], color='orange')
plt.title("Zemes paskirtis vs aro kaina")
plt.xlabel("Kaina (€/a)")
plt.ylabel("Zemes paskirtis")
plt.show()

# --------------------Draw Histogram----------------------------
price_pm_counts = df["Price (€/a)"]
plt.figure(figsize=(6, 6))
plt.hist(price_pm_counts)
plt.title("Pasiulymai vs. aro kaina")
plt.xlabel("Kaina (€/a)")
plt.ylabel("Pasiulymai (vnt.)")
plt.show()

# -------------------Draw Scatter-----------------------------
plt.figure(figsize=(10, 6))
plt.scatter(df['Price (€/a)'], df['Intendance'], c='blue')
plt.title("Aro kaina vs zemes paskirtis")
plt.xlabel("Kaina (€/a)")
plt.ylabel("Zemes paskirtis")
plt.show()

# ------------------Draw Scatter Seaborn---------------------
plt.figure(figsize=(10, 6))
ax = sns.scatterplot(x='Price (€/a)', y='Intendance', hue='Location', data=df)
ax.set_title('Aro kaina vs zemes paskirtis vs vietove')
plt.show()

# ------------------Draw Pair plot Seaborn-------------------
sns.pairplot(df)
plt.show()

# ------------------Draw Pair plot Seaborn HUE-------------------
sns.pairplot(df, hue="Location")
plt.show()
