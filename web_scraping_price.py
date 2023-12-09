from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import pandas as pd

def Correct_date_click(driver):
    calendar_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "icon-calendar"))
    )

    calendar_button.click()

    calendar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-condensed"))
    )
    
    time.sleep(5)

    selected_date = calendar.find_element(By.XPATH, "//td[contains(@class, 'active day')]")
    yesterday = datetime.today() - timedelta(days=1)
    yesterday = yesterday.day

    # Pobierz datę zaznaczonego elementu
    if(selected_date.text == str(yesterday)):
        # nie robimy nic jeśli jest wczorajsza data zaznaczona
        return
    else:
        # TODO sprawdz czy działa klikanie poprzedniej daty
        previous_date = calendar.find_element(By.XPATH, f"//*[ text() = '{yesterday}' ]")
        previous_date.click()
        # klikamy i czekamy aż załaduje tabelkę na dzień dzisiejszy
        time.sleep(5)
        return
    

def Save_data_csv(driver):
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
        df["date"] = str(datetime.today().date()) + ' ' + df["hour"].astype(str) + ':00:00.000000 UTC'
        df.index = df["date"]
        df.index = pd.to_datetime(df.index)
        df.drop(['hour','date'], inplace=True, axis=1)
        df.to_csv("data\\newest_prices.csv")
    except Exception as e:
        print("Wystąpił błąd podczas zapisywania CSV: ", str(e))
    return


def Start_price_scraping():
    url = "https://tge.pl/energia-elektryczna-rdn"

    # chyba działa bez tego, wtf XD
    edge_driver_path = 'edge_driver\\msedgedriver.exe'
    try:
        driver = webdriver.Edge()
        driver.get(url)
    except Exception as e:
        print("Wystąpił błąd podczas uruchamiania drivera selenium do Edge: ", str(e))
    try:
        Correct_date_click(driver)
    except Exception as e:
        print("Wystąpił błąd podczas ustawiania dobrej daty w kalendarzu: ", str(e))
        
    Save_data_csv(driver)
    driver.quit()
    return
