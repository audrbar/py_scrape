#! /Users/audrius/Documents/VCSPython/py_scrape/bin/python3

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

pd.set_option('display.max_columns', None)


def scrape_data():
    print('Data scraping started...')
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.aruodas.lt/sklypai-pardavimui/")
    time.sleep(5)
    # page = driver.page_source
    print('Data were scraped.')

    locations = driver.find_elements(By.CLASS_NAME, 'list-adress-v2')
    area_overall = driver.find_elements(By.CLASS_NAME, 'list-AreaOverall-v2')
    purpose = driver.find_elements(By.CLASS_NAME, 'list-Intendances-v2')
    print('Data red from HTML.')

    locations_list = []
    for item in locations:
        locations_list.append(item.text.strip())
    area_overall_list = []
    for item in area_overall:
        area_overall_list.append(item.text.strip())
    purpose_list = []
    for item in purpose:
        purpose_list.append(item.text.strip())
    print('Lists were created.')

    df = pd.DataFrame({
        'Location': locations_list,
        'Purpose': purpose_list,
        'Area_Overall': area_overall_list
    })
    print('Data Frame was created.')

    df = df.drop(df.head(2).index)  # drop first n rows
    df['Discount'] = df['Location'].str.split(pat='\n').str[2].str.strip()
    df['Price_€'] = df['Location'].str.split(pat='\n').str[-2].str.strip()
    df['Price_€a'] = df['Location'].str.split(pat='\n').str[-1].str.strip()
    df['Settlement'] = df['Location'].str.split(pat=',').str[1].str.split(pat='\n').str[0].str.strip()
    df['Location'] = df['Location'].str.split(pat='\n').str[0].str.split(pat=',').str[0].str.strip()
    df['Area_Overall'] = pd.to_numeric(df['Area_Overall'].astype('str'))
    df['Price_€'] = df['Price_€'].str.split(pat='€').str[0].str.replace(r'\s+', '', regex=True).astype(int)
    df['Price_€a'] = df['Price_€a'].str.split(pat='€').str[0].str.replace(r'\s+', '', regex=True).astype(int)
    df['Discount'] = df['Discount'].str.replace(r'(^.*€.*$)', '0%', regex=True) \
        .str.replace(r'%', '', regex=True).str.split(' ').str[-1].str.replace(',', '.').astype(float)
    df_1 = df.drop(df[df['Settlement'] == 'NaN'].index)
    _df = df_1.fillna('Nenurodyta')
    print('Data Frame was cleared.')
    return _df


def compare_dataframes(scraped_data, db_data):
    columns = ('id', 'Location', 'Purpose', 'Area_Overall', 'Discount', 'Price_€', 'Price_€a', 'Settlement')
    df = pd.DataFrame(data=db_data, columns=columns)
    df_1 = df.drop(df[df['Settlement'] == 'NaN'].index)
    df_db = df_1.fillna('Nenurodyta')
    # df_db = df_1.replace(to_replace=np.nan, value='Nenurodyta')
    scraped_data['match'] = (df_db['Location'].isin(scraped_data['Location'])) & \
                            (df_db['Purpose'].isin(scraped_data['Purpose'])) & \
                            (df_db['Area_Overall'].isin(scraped_data['Area_Overall'])) & \
                            (df_db['Settlement'].isin(scraped_data['Settlement']))
    data_to_insert = scraped_data.loc[scraped_data['match'] == 0].drop(columns=['match'])

    return data_to_insert
