from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def change_latest_filename(directory, new_name):
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


def Start_additional_data_scraping():
    try:

        webdriver_path = 'edge_driver\\msedgedriver.exe'
        url = 'https://www.pse.pl/dane-systemowe/plany-pracy-kse/plan-koordynacyjny-5-letni/wielkosci-podstawowe'


        download_path = os.getcwd()
        download_path = os.path.join(download_path, 'data')

        edge_options = webdriver.EdgeOptions()
        edge_options.add_experimental_option('prefs', {'download.default_directory': download_path})

        driver = webdriver.Edge(options=edge_options)
        driver.get(url)

        time.sleep(10)

        # csv_link = driver.find_element(By.CSS_SELECTOR, 'a[title="CSV"]')
        csv_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="CSV"]'))
            )

        csv_link.click()
        time.sleep(10)
    except Exception as e:
        print("Wystąpił błąd podczas scrapowania dodatkowych danych:", str(e))

    change_latest_filename(download_path, 'dane_kse.csv')
    return