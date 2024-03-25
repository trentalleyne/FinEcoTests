import pandas as pd
import numpy as np
from numpy import nan

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://www.windguru.cz/208690"

Xdates = '//*[@id="tabid_0_0_dates"]'
Xwind = '//*[@id="tabid_0_0_WINDSPD"]'
Xgusts = '//*[@id="tabid_0_0_GUST"]'
XwindDirection = '//*[@id="tabid_0_0_SMER"]'
Xswell = '//*[@id="tabid_0_0_HTSGW"]'
Xperiod = '//*[@id="tabid_0_0_PERPW"]'
XswellDirection = '//*[@id="tabid_0_0_DIRPW"]'

options = Options()
options.add_argument("--headless=new")
service = webdriver.ChromeService()
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

try:
    dates = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xdates))).text
    #print(dates)
    wind = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xwind))).text
    #print(wind)
    gusts = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xgusts))).text
    #print(gusts)
    wind_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XwindDirection)))
    span_elements = WebDriverWait(wind_element, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/span[@title]')))
    windDirections = []
    for span_element in span_elements:
        span_title = span_element.get_attribute('title')
        windDirections.append(span_title)
    #print(windDirection)
    swell = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xswell))).text
    #print(swell)
    period = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xperiod))).text
    #print(period)
    
    swell_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XswellDirection)))
    span_elements = WebDriverWait(swell_element, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/span[@title]')))
    swellDirections = []
    for span_element in span_elements:
        span_title = span_element.get_attribute('title')
        swellDirections.append(span_title)
    #print(windDirection)
except:
        print("Something failed")
driver.quit()

dates = dates.split('\n')
dates = dates[1:]

datesList = []
counter = 0
for date in dates:
    if counter%2 != 0:
        datesList.append(date + " " + dates[counter-1])
    counter += 1
	
index = ['wind', 'gusts', 'windDirection', 'swell', 'period', 'swellDirection']

df = pd.DataFrame(columns = datesList, index=index)

windList = wind.split()

df.loc['wind'] = windList

gustsList = gusts.split()
df.loc['gusts'] = gustsList
df.loc['windDirection'] = windDirections
swell = swell.split()
df.loc['swell'] = swell

period = period.split()
df.loc['period'] = period

df.loc['swellDirection'] = swellDirections
df.loc['wind']=df.loc['wind'].astype(int)
df.loc['gusts']=df.loc['gusts'].astype(int)
df.loc['swell']=df.loc['swell'].astype(float)
df.loc['period']=df.loc['period'].astype(int)

print("")
print("possible days/times to look out for:")
for col_index, col in enumerate(df):
    #day = col.split()[1])
    if(df.loc['swell'][col_index] > 1.7 and (df.loc['windDirection'][col_index].split()[0] in {'W', 'NW', 'SW', 'NNW', 'SSW', 'WNW', 'WSW'})):
        print(col)
        
while True:
    user_input = input("type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break  # Exit the loop if the user types 'exit'
    else:
        print(" ")

print("Program exited.")