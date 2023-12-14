from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime, timedelta

def Start_day_filter(driver):
    data_od = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, '_VisioToolbarPortlet_WAR_visioneoportlet_data_od'))
    )
    data_od.click()

    date_start = datetime.now() - timedelta(days=30)

    year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-year'))
    )
    year.click()
    year_pick = year.find_element(By.CSS_SELECTOR, f'option[value="{str(date_start.year)}"]')
    year_pick.click()

    month = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-month'))
    )
    month.click()
    month_pick = month.find_element(By.CSS_SELECTOR, f'option[value="{str(date_start.month-1)}"]')
    month_pick.click()

    day = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//a[@class='ui-state-default'][text()='{str(date_start.day)}']"))
    )
    day.click()
    time.sleep(3)
    return 


def End_day_filter(driver):
    data_do = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, '_VisioToolbarPortlet_WAR_visioneoportlet_data_do'))
    )
    data_do.click()

    day_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//button[text()='Dziś']"))
    )
    day_button.click()
    time.sleep(3)
    return 


def Change_latest_filename(directory, new_name):
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        # Sortujemy pliki według daty modyfikacji
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

        if files:
            latest_file = files[0]
            new_path = os.path.join(directory, new_name)
            os.rename(os.path.join(directory, latest_file), new_path)

            print(f"Najnowszy plik został pomyślnie zmieniony na {new_name}")

        else:
            print("Brak plików w katalogu.")

    except Exception as e:
        print("Wystąpił błąd podczas zmiany nazwy pobranego pliku:", str(e))
    return


def Change_filter_and_download(driver):
    eksport_za_okres = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Eksport za okres"]'))
    )
    eksport_za_okres.click()

    Start_day_filter(driver)
    End_day_filter(driver)

    csv_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Eksport do CSV"]'))
    )
    csv_link.click()
    time.sleep(20)
    return


def Start_additional_data_scraping(nowa_nazwa_pliku = 'dane_kse.csv'):
    try:

        webdriver_path = 'edge_driver\\msedgedriver.exe'
        url = 'https://www.pse.pl/dane-systemowe/plany-pracy-kse/plan-koordynacyjny-5-letni/wielkosci-podstawowe'


        download_path = os.getcwd()
        download_path = os.path.join(download_path, 'data')

        edge_options = webdriver.EdgeOptions()
        edge_options.add_experimental_option('prefs', {'download.default_directory': download_path})

        driver = webdriver.Edge(options=edge_options)
        driver.get(url)

        Change_filter_and_download(driver)
        Change_latest_filename(download_path, nowa_nazwa_pliku)
        driver.quit()
    except Exception as e:
        print("Wystąpił błąd podczas scrapowania dodatkowych danych:", str(e))

    return