from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import pandas as pd


def Scrap_every_day(url, df, date, driver):
    driver.get(url)
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@id='footable_kontrakty_godzinowe']/tbody"))
    )
    hours = []
    prices = []
    rows = table.find_elements(By.XPATH, "./tr")
    for row in rows:
        cells = row.find_elements(By.XPATH, "./td")
        row_data = [cell.text for cell in cells]
        hours.append(str(row_data[0]).split("-")[0])
        prices.append(row_data[1])

    prices = [x.replace(',', '.') for x in prices]
    prices = [ float(x) for x in prices]
    df_current = pd.DataFrame({'hour': hours, 'da1_price': prices})
    df_current["date"] = str(date) + ' ' + df_current["hour"].astype(str) + ':00:00.000000 UTC'
    df = pd.concat([df, df_current])
    return df


def Create_date_list(past_date, current_date):
    # Calculate the difference between the two dates
    date_difference = current_date - past_date
    dates = []
    list = []
    # Iterate through the range of days and print each day
    for day in range(date_difference.days):
        current_day = past_date + timedelta(days=day)
        list.append(f'https://tge.pl/energia-elektryczna-rdn?dateShow={str(current_day.day)}-{str(current_day.month)}-{str(current_day.year)}&dateAction=')
        dates.append((current_day + timedelta(days=1)).date())

    return list, dates


def Start_price_scraping():
    dates = []
    driver = webdriver.Edge()
    now_date = datetime.now()
    date_start = now_date - timedelta(days=31)
    links, dates = Create_date_list(date_start, now_date)
    df = pd.DataFrame(columns=['hour', 'da1_price', 'date'])

    for date, link in zip(dates, links):
        df = Scrap_every_day(link, df, date, driver)

    df.index = df["date"]
    df.index = pd.to_datetime(df.index)
    df.drop(['hour','date'], inplace=True, axis=1)
    df.to_csv("data\\newest_prices.csv")
    driver.quit()
    return