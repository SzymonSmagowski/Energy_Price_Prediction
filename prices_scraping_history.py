from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import pandas as pd


def Save_data_csv(driver, name):
    date = datetime.today() - timedelta(days=14-int(name))
    try:
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
    except Exception as e:
        print("Wystąpił błąd podczas scrapowania cen: ", str(e))

    try:
        prices = [x.replace(',', '.') for x in prices]
        prices = [ float(x) for x in prices]
        df = pd.DataFrame({'hour': hours, 'da1_price': prices})
        df["Time"] = str(date.date()) + ' ' + df["hour"].astype(str) + ':00:00.000000 UTC'
        df.index = df["Time"]
        df.index = pd.to_datetime(df.index)
        df.drop(['hour','Time'], inplace=True, axis=1)
        df.to_csv(f"prices_{name}.csv")
    except Exception as e:
        print("Wystąpił błąd podczas zapisywania CSV: ", str(e))
    return


def Start_price_scraping():
    dates = ["https://tge.pl/energia-elektryczna-rdn?dateShow=23-11-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=24-11-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=25-11-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=26-11-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=27-11-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=28-11-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=29-11-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=30-11-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=01-12-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=02-12-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=03-12-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=04-12-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=05-12-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=06-12-2023&dateAction="
             ,"https://tge.pl/energia-elektryczna-rdn?dateShow=07-12-2023&dateAction="]
    url = "https://tge.pl/energia-elektryczna-rdn?dateShow=24-11-2023&dateAction="

    # chyba działa bez tego, wtf XD
    edge_driver_path = 'edge_driver\\msedgedriver.exe'
    i=0
    for date in dates:
        try:
            driver = webdriver.Edge()
            driver.get(date)
        except Exception as e:
            print("Wystąpił błąd podczas uruchamiania drivera selenium do Edge: ", str(e))
        
        Save_data_csv(driver, str(i))
        i+=1
    driver.quit()
    return

Start_price_scraping()