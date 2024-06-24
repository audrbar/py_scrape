#! /Users/audrius/Documents/VCSPython/py_scrape/bin/python3

from lxml import html
import requests
import pandas as pd

url = 'https://www.meteo.lt/prognozes/lietuvos-miestai/?area=vilnius'
page = requests.get(url)
# print(page.content)

tree = html.fromstring(page.content)

# Savaites dienos
days = tree.xpath('//div[@class="days"]//div[@class="date"]/text()')
days_list = []
for i in days:
    days_list.append(i.strip())

# Duomenu lentele
table = tree.xpath('//div[@class="tablewrap"]/table')
data_list = []
for i in table:
    data_list.append(i.xpath('//td/text()'))

#  Panaikiname tarpus domenyse
data_list_stripped = []
for i in data_list:
    for j in i:
        data_list_stripped.append(j.strip())

# Ismetam tuscius stringus
filtered_list = [item for item in data_list_stripped if item]

# Sukuriam listus is sutvarkytu duomenu
laikas = []
temp = []
vejas = []
krituliai = []
slegis = []
dregme = []
jutamoji_temp = []

for i in range(0, len(filtered_list), 7):
    chunk = filtered_list[i:i+7]
    laikas.append(chunk[0])
    temp.append(chunk[1])
    vejas.append(chunk[2])
    krituliai.append(chunk[3])
    slegis.append(chunk[4])
    dregme.append(chunk[5])
    jutamoji_temp.append(chunk[6])
    # print(chunk)

# Sukuriame pandas lentele
df = pd.DataFrame({
    "Laikas": laikas,
    "Temp": temp,
    "Vejas": vejas,
    "Krituliai": krituliai,
    "Slegis": slegis,
    "Dregme": dregme,
    "Jut_temp": jutamoji_temp
})
print(df)