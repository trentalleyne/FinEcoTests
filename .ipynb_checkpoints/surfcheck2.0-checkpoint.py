import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of URLs to scrape
urls = [
    "https://www.windguru.cz/208690",
    "https://www.windguru.cz/62403",
    "https://www.windguru.cz/62164",
    "https://www.windguru.cz/62404"
]

# XPaths for elements
Xdates = '//*[@id="tabid_0_0_dates"]'
Xwind = '//*[@id="tabid_0_0_WINDSPD"]'
Xgusts = '//*[@id="tabid_0_0_GUST"]'
XwindDirection = '//*[@id="tabid_0_0_SMER"]'
Xswell = '//*[@id="tabid_0_0_HTSGW"]'
Xperiod = '//*[@id="tabid_0_0_PERPW"]'
XswellDirection = '//*[@id="tabid_0_0_DIRPW"]'

dfs = []  # List to store dataframes for each URL

for url in urls:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode to run Chrome without opening browser
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    try:
        # Wait for elements to load
        dates = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xdates))).text
        wind = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xwind))).text
        gusts = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xgusts))).text
        wind_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XwindDirection)))
        span_elements = WebDriverWait(wind_element, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/span[@title]')))
        swell = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xswell))).text
        period = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xperiod))).text
        swell_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XswellDirection)))
        span_elements_swell = WebDriverWait(swell_element, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/span[@title]')))

        # Extracting data
        dates = dates.split('\n')[1:]
        datesList = [date + " " + dates[i-1] for i, date in enumerate(dates, 1) if i % 2 != 0]

        windList = wind.split()
        gustsList = gusts.split()
        windDirections = [span_element.get_attribute('title') for span_element in span_elements]
        swellList = swell.split()
        periodList = period.split()
        swellDirections = [span_element.get_attribute('title') for span_element in span_elements_swell]

        # Creating dataframe
        df = pd.DataFrame(columns=datesList, index=['wind', 'gusts', 'windDirection', 'swell', 'period', 'swellDirection'])
        df.loc['wind'] = windList
        df.loc['gusts'] = gustsList
        df.loc['windDirection'] = windDirections
        df.loc['swell'] = swellList
        df.loc['period'] = periodList
        df.loc['swellDirection'] = swellDirections
        df.loc['wind'] = df.loc['wind'].astype(int)
        df.loc['gusts'] = df.loc['gusts'].astype(int)
        df.loc['swell'] = df.loc['swell'].astype(float)
        df.loc['period'] = df.loc['period'].astype(int)

        # Appending dataframe to list
        dfs.append(df)

    except Exception as e:
        print(f"Failed to scrape data from {url}: {str(e)}")

    driver.quit()

# Printing dataframes for each URL
for i, df in enumerate(dfs, 1):
    print(f"DataFrame for URL {i}:")
    print(df)
    print()

print("Possible days/times to look out for:")
for df in dfs:
    for col_index, col in enumerate(df):
        if df.loc['swell'][col_index] > 1.7 and df.loc['windDirection'][col_index].split()[0] in {'W', 'NW', 'SW', 'NNW', 'SSW', 'WNW', 'WSW'}:
            print(col)

# Wait for user input to exit
while True:
    user_input = input("Type 'exit' to quit: ")
    if user_input.lower() == 'exit':
        break

print("Program exited.")