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
    # selected_date = calendar.find_element(By.CLASS_NAME, "today disabled day")

    selected_date = calendar.find_element(By.XPATH, "//td[contains(@class, 'active day')]")
    yesterday = datetime.today() - timedelta(days=1)
    yesterday = yesterday.day

    # Pobierz datę zaznaczonego elementu
    if(selected_date.text == str(yesterday)):
        print('git')
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

    df = pd.DataFrame({'hour': hours, 'da1_price': prices})
    df["Time"] = str(datetime.today().date()) + ' ' + df["hour"].astype(str) + ':00:00.000000 UTC'
    df.index = df["Time"]
    df.index = pd.to_datetime(df.index)
    df.drop(['hour','Time'], inplace=True, axis=1)
    df.to_csv("newest_prices.csv")
    time.sleep(5)
    return

url = "https://tge.pl/energia-elektryczna-rdn"

# chyba działa bez tego, wtf XD
edge_driver_path = 'edge_driver\\msedgedriver.exe'

driver = webdriver.Edge()
driver.get(url)

#Correct_date_click(driver)
Save_data_csv(driver)
# DZIAŁA
# table = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//table[@id='footable_kontrakty_godzinowe']/tbody"))
# )
# print(table.text)




# Pobierz dane z tabeli
# rows = table.find_elements(By.XPATH, "./table")
# for row in rows:
#     cells = row.find_elements(By.XPATH, "./td")
#     row_data = [cell.text for cell in cells]
#     print(row_data)

# try:
#     # Poczekaj, aż kalendarz będzie klikalny
#     calendar_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'day-picker-modern-button')]/button"))
#     )
    
#     # Kliknij w kalendarz
#     calendar_button.click()

#     # Poczekaj, aż pojawi się kalendarz
#     calendar = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//div[@class='day-picker']"))
#     )

#     # Znajdź wczorajszą datę i kliknij
#     yesterday_date = calendar.find_element(By.XPATH, "//div[@class='day-modifier']/preceding-sibling::div")
#     yesterday_date.click()

#     # Poczekaj, aż załaduje się tabela z danymi
#     table = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//table[@id='tablica']/tbody"))
#     )

#     # Pobierz dane z tabeli
#     rows = table.find_elements(By.XPATH, "./table")
#     for row in rows:
#         cells = row.find_elements(By.XPATH, "./td")
#         row_data = [cell.text for cell in cells]
#         print(row_data)

# except Exception as e:
#     print("Wystąpił błąd:", str(e))

# finally:
#     # Zamknij przeglądarkę
#     driver.quit()

# 0-1 406,00 3966,6 381,11 1109,5 388,95 69,3
# 1-2 405,54 3871,3 400,43 776,3 409,71 23
# 2-3 401,00 3739 400,44 557,6 400,89 153
# 3-4 398,70 3791,2 399,38 640,7 399,77 93
# 4-5 392,90 4040,6 390,83 699,3 397,65 23
# 5-6 403,14 4467,5 398,58 1163,9 407,80 23
# 6-7 500,00 5727,4 534,50 1260,2 510,00 10
# 7-8 585,00 4508,9 622,57 1072,4 585,00 30
# 8-9 610,00 5182 607,19 1234 610,00 41
# 9-10 605,00 5071,2 570,62 1734,8 - 0
# 10-11 600,00 5116 539,16 1867,7 540,00 7,9
# 11-12 600,00 5336 555,36 1870,8 578,22 76,7
# 12-13 600,00 5348,4 565,61 1890,7 580,00 15
# 13-14 600,00 5264,4 600,91 1499,5 - 0
# 14-15 600,00 5077,6 575,29 1667,7 580,00 40
# 15-16 596,27 4882,7 561,06 1045,1 580,00 40
# 16-17 600,00 4796,3 590,73 817,5 - 0
# 17-18 594,63 4435,7 560,50 1094,9 - 0
# 18-19 560,00 4109,9 514,37 636 - 0
# 19-20 540,00 3964,6 583,00 435,5 - 0
# 20-21 500,00 3798,3 500,54 412 504,61 24,9
# 21-22 450,00 3402,5 438,55 597,4 458,33 15
# 22-23 430,00 4349,2 440,57 1327,6 440,00 10
# 23-24 392,90 4384,4 392,84 1204,8 400,38 13